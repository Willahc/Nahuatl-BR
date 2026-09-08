"""Bounded integrity rules for the Gate 3 pilot; no external source access.

The YAML projection reader accepts only the existing scalar/flow-map syntax
for requested fields. It fails closed on unsupported syntax; it is not a
general YAML parser. Unrelated descriptive registry fields are not interpreted.
"""

import json
import re
from collections import Counter

ABSENCE = {"UNKNOWN", "NOT_REVIEWED", "NOT_RECORDED", "NOT_APPLICABLE", "NOT_ATTESTED"}
RELATIONS = {"SUPPORTS", "CONTRADICTS", "QUALIFIES", "DERIVED_FROM"}
CLAIM_RELATIONS = {
    "has_historical_gloss": {"SUPPORTS", "DERIVED_FROM"},
    "has_pt_br_editorial_gloss": {"SUPPORTS", "DERIVED_FROM"},
    "has_reported_prosodic_notation": {"SUPPORTS", "DERIVED_FROM"},
}
UNSUPPORTED_STATES = {"DRAFT", "QUARANTINED"}


def defined(value):
    return isinstance(value, str) and bool(value.strip()) and value not in ABSENCE


def scalar(value):
    value = value.strip()
    if value.startswith('"'):
        result = json.loads(value)
        if not isinstance(result, str):
            raise ValueError("expected string scalar")
        return result
    if not value or any(c in value for c in "{}[]#&*!|>'\""):
        raise ValueError("unsupported YAML scalar")
    return value


def field(text, name, indent=0):
    matches = re.findall(r"^" + " " * indent + re.escape(name) + r":\s*(.+)$", text, re.M)
    if len(matches) != 1:
        raise ValueError(f"expected one {name} field")
    return matches[0].strip()


def flow_map(value):
    if not value.startswith("{") or not value.endswith("}"):
        raise ValueError("expected single-line YAML flow map")
    body = value[1:-1]
    token = re.compile(r'\s*([a-z_]+):\s*("(?:[^"\\]|\\.)*"|[^,{}\[\]\n]+)\s*(,|$)')
    result = {}
    offset = 0
    while offset < len(body):
        match = token.match(body, offset)
        if not match or match[1] in result:
            raise ValueError("unsupported or duplicate flow-map field")
        result[match[1]] = scalar(match[2])
        offset = match.end()
    return result


def load_metadata(root):
    registry = {}
    for path in sorted((root / "data/source_registry").glob("*.yml")):
        text = path.read_text(encoding="utf-8-sig")
        sid = scalar(field(text, "source_id"))
        if sid in registry:
            raise ValueError(f"DUPLICATE_ID: Source {sid}")
        scope = flow_map(field(text, "linguistic_scope"))
        if not all(defined(scope.get(k)) for k in ("language", "variety", "period")):
            raise ValueError(f"SOURCE_SCOPE: incomplete scope for {sid}")
        registry[sid] = {"scope": scope, "name": scalar(field(text, "name"))}
    policy = (root / "data/policies/classical_orthography_v1.yml").read_text(encoding="utf-8-sig")
    profile = scalar(field(policy, "policy_id")) + "@" + scalar(field(policy, "version"))
    if scalar(field(policy, "status")) != "APPROVED":
        raise ValueError("NORMALIZATION_PROFILE: profile not approved")
    profiles = {profile: scalar(field(policy, "language", indent=2))}
    return registry, profiles


def compatible_variety(lemma_variety, attestation, source):
    """Require locked historical scope, not lexical matching of a modern name.

    This pilot has no cross-variety attestation mechanism. Future comparative
    links require their own approved policy, without reusing this evidence rule.
    """
    scope = source["scope"]
    return (
        lemma_variety == "Classical Nahuatl"
        and attestation.get("variety", lemma_variety) == lemma_variety
        and scope["period"] in {"Classical/colonial", "Classical/early colonial"}
        and "nahuatl" in scope["variety"].casefold()
        and not any(word in scope["variety"].casefold() for word in ("modern", "mixed"))
    )


def validate_record(record, registry, profiles, errors):
    lid = record["lemma"]["id"]

    def error(category, detail):
        errors.append(f"{category}: {lid}: {detail}")

    if not defined(lid):
        error("INVALID_ID", "lemma_id")
    translations = [t for s in record.get("senses", []) for t in s.get("translations", [])]
    collections = {
        "form_id": record.get("forms", []),
        "sense_id": record.get("senses", []),
        "claim_id": record.get("claims", []),
        "attestation_id": record.get("attestations", []),
        "evidence_id": record.get("evidence", []),
        "translation_id": translations,
        "analysis_id": record.get("morphology", {}).get("analyses", []),
        "divergence_id": record.get("divergences", []),
    }
    ids = {}
    for key, objects in collections.items():
        values = [obj.get(key) for obj in objects]
        if any(not defined(v) for v in values):
            error("INVALID_ID", key)
        for value, count in Counter(values).items():
            if count > 1:
                error("DUPLICATE_ID", f"{key} {value}")
        ids[key] = {obj.get(key): obj for obj in objects}

    def reference(value, key):
        if not isinstance(value, str) or value not in ids[key]:
            error("UNRESOLVED_REFERENCE", f"{key}: {value}")
            return None
        return ids[key][value]

    def evidence_refs(value):
        if value == "NOT_APPLICABLE":
            return []
        if not isinstance(value, list):
            error("UNRESOLVED_REFERENCE", "evidence must be a list")
            return []
        resolved = []
        for item in value:
            eid = item.get("evidence_id") if isinstance(item, dict) else item
            obj = reference(eid, "evidence_id")
            if obj is not None:
                resolved.append(obj)
        return resolved

    def source_ref(obj):
        for key in ("source", "aggregator"):
            if key in obj and obj[key] not in registry:
                error("SOURCE_REFERENCE", f"{key}: {obj[key]}")

    def locator(obj):
        for key in ("locator", "underlying_locator"):
            if key == "locator" or key in obj:
                if not defined(obj.get(key)) and not defined(obj.get("locator_absence_reason")):
                    error("LOCATOR_JUSTIFICATION", key)

    # Work is a descriptive title in v1, not a foreign key. Check against the
    # registered Work title; Olmos registry explicitly names related vocabularies.
    for att in record.get("attestations", []):
        source_ref(att)
        source = registry.get(att.get("source"))
        if source and not compatible_variety(record["lemma"]["variety"], att, source):
            error("SOURCE_VARIETY_MISMATCH", str(att.get("source")))
        if not defined(att.get("work")):
            error("WORK_REFERENCE", "missing Work title")
        elif source:
            expected = source["name"].removesuffix(" and related vocabularies")
            if att["work"] != expected:
                error("WORK_REFERENCE", "Work differs from registered historical Work")
        locator(att)

    for evidence in record.get("evidence", []):
        source_ref(evidence)
        locator(evidence)
        att = reference(evidence.get("attestation_id"), "attestation_id")
        if att is not None and any(evidence.get(k) != att.get(k) for k in ("source", "aggregator", "locator", "url")):
            error("EVIDENCE_ATTESTATION_MISMATCH", evidence["evidence_id"])

    for form in record.get("forms", []):
        evs = evidence_refs(form.get("evidence", []))
        if form.get("layer") == "SOURCE_FORM":
            if not evs:
                error("SOURCE_FORM_CHAIN", "missing Evidence")
            for ev in evs:
                att = ids["attestation_id"].get(ev.get("attestation_id"))
                if att is None or form.get("value") != att.get("source_form"):
                    error("SOURCE_FORM_CHAIN", form["form_id"])
        profile = form.get("normalization_profile")
        if profile not in (None, "NOT_APPLICABLE") and profiles.get(profile) != record["lemma"]["variety"]:
            error("NORMALIZATION_PROFILE", str(profile))
        if form.get("layer") == "NORMALIZED_FORM" and defined(form.get("value")):
            if profiles.get(profile) != record["lemma"]["variety"]:
                error("NORMALIZATION_PROFILE", "defined NORMALIZED_FORM needs applicable profile")

    links = record.get("evidence_links", [])
    for link in links:
        reference(link.get("claim_id"), "claim_id")
        reference(link.get("evidence_id"), "evidence_id")
        if link.get("relation") not in RELATIONS:
            error("INVALID_EVIDENCE_RELATION", str(link.get("relation")))

    def provenance(obj):
        prov = obj.get("editorial_provenance", {})
        required = ("actor_role", "actor_id", "tool", "tool_version", "timestamp", "action",
                    "from_state", "to_state", "created_in_commit", "history_status", "review_status", "notes")
        if not all(isinstance(prov.get(k), str) and prov[k].strip() for k in required):
            error("EDITORIAL_PROVENANCE", "missing provenance fields")
        if prov.get("to_state") != obj.get("editorial_state"):
            error("EDITORIAL_PROVENANCE", "recorded state differs from object")

    for claim in record.get("claims", []):
        # Current subjects are typed by membership. Reject ambiguous local IDs
        # rather than inventing a global namespace for every object class.
        subject = claim.get("subject")
        candidates = int(subject == lid) + sum(subject in ids[k] for k in ("form_id", "sense_id"))
        if candidates != 1:
            error("UNRESOLVED_REFERENCE", "Claim.subject missing or ambiguous")
        relations = CLAIM_RELATIONS.get(claim.get("predicate"))
        if relations is None:
            error("CLAIM_POLICY", "predicate has no approved evidence policy")
        elif claim.get("editorial_state") not in UNSUPPORTED_STATES:
            if not any(link.get("claim_id") == claim["claim_id"]
                       and link.get("relation") in relations
                       and link.get("evidence_id") in ids["evidence_id"] for link in links):
                error("CLAIM_EVIDENCE_REQUIRED", claim["claim_id"])
        provenance(claim)

    for trans in translations:
        if not isinstance(trans.get("text"), str) or not trans["text"].strip():
            error("EMPTY_TRANSLATION", trans["translation_id"])
        reference(trans.get("derived_from"), "claim_id")
        if "evidence" in trans:
            evidence_refs(trans["evidence"])
        if trans.get("confidence") not in {"UNASSESSED", "LOW", "MEDIUM", "HIGH"}:
            error("TRANSLATION_CONFIDENCE", trans["translation_id"])
        provenance(trans)

    for analysis in record.get("morphology", {}).get("analyses", []):
        if not evidence_refs(analysis.get("evidence", [])):
            error("MORPHOLOGY_EVIDENCE_REQUIRED", analysis["analysis_id"])
    phon = record.get("phonological_information", {})
    for key in ("evidence", "vowel_length_evidence", "saltillo_evidence"):
        evidence_refs(phon.get(key, []))
    for key in ("vowel_length", "saltillo"):
        if defined(phon.get(key)) and not evidence_refs(phon.get(key + "_evidence", [])):
            error("PHONOLOGY_EVIDENCE_REQUIRED", key)
    for divergence in record.get("divergences", []):
        if "evidence" in divergence:
            evidence_refs(divergence["evidence"])
    for context in record.get("corpus_references", []):
        source_ref(context)
        locator(context)
        if not defined(context.get("work")):
            error("WORK_REFERENCE", "context Work missing")

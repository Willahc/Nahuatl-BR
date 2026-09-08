#!/usr/bin/env python3
"""Validate the bounded Gate 4 classical phonology proposal (read-only).

The validator enforces the Gate 4 evidence discipline on the 29 Claims,
28 Evidence records, 32 fixture cases, the 15-lemma integration sample, the
classical phonology policy and the audio concept model. It never writes to
data/, docs/, fixtures/, claims/ or evidence/; --check is the only mode and
exits non-zero on any critical failure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
from gate3_integrity import load_metadata

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "data" / "phonology" / "claims"
EVIDENCE_PATH = ROOT / "data" / "phonology" / "evidence.yml"
INTEGRATION_PATH = ROOT / "data" / "phonology" / "integration_sample.yml"
BASELINE_PATH = ROOT / "data" / "phonology" / "gate3_baseline.yml"
AUDIO_MODEL_PATH = ROOT / "data" / "phonology" / "audio_model.yml"
POLICY_PATH = ROOT / "data" / "policies" / "classical_phonology_v1.yml"
FIXTURES_PATH = ROOT / "data" / "fixtures" / "gate4_phonology_cases.yml"
LEMMA_DIR = ROOT / "data" / "pilot" / "lemmas"
SCAN_DIRS = (ROOT / "data", ROOT / "docs")
GATE_STATUS_PATH = ROOT / "docs" / "GATE_STATUS.md"

EXPECTED_CLAIMS = 29
EXPECTED_EVIDENCE = 28
EXPECTED_FIXTURES = 32
EXPECTED_INTEGRATION = 15
EXPECTED_LEMMAS = 50

EDITORIAL_STATES = {"DRAFT", "IN_REVIEW", "APPROVED", "PUBLISHED", "QUARANTINED", "REJECTED", "DEPRECATED"}
MODALITIES = {"OBSERVED", "REPORTED", "INFERRED", "RECONSTRUCTED", "EDITORIAL"}
CONFIDENCES = {"UNASSESSED", "LOW", "MEDIUM", "HIGH"}
MEDIATION_LEVELS = {"DIRECT_WITNESS", "HISTORICAL_EDITION", "MODERN_EDITION", "AGGREGATOR"}
CLAIM_TOPICS = {
    "PHONEME_INVENTORY", "VOWEL_LENGTH_CONTRAST", "SALTILLO_EXISTENCE", "SALTILLO_REALIZATION",
    "GRAPHEME_PHONEME_CORRESPONDENCE", "STRESS_RULE", "SYLLABLE_STRUCTURE", "PHONOTACTIC_CONSTRAINT",
    "ALLOPHONY", "MORPHOPHONOLOGICAL_PROCESS",
}
POLICY_LAYERS = {
    "ORTHOGRAPHIC_EVIDENCE", "PHONOLOGICAL_ANALYSIS", "PHONEMIC_RECONSTRUCTION", "PHONETIC_REALIZATION",
    "PEDAGOGICAL_PRONUNCIATION", "MODERN_VARIETY_PRONUNCIATION", "AUDIO_REALIZATION",
}
CERTAINTY_DIMENSIONS = {
    "CONTRAST_EXISTENCE", "PHONEMIC_INTERPRETATION", "PHONETIC_REALIZATION", "DISTRIBUTION",
    "HISTORICAL_RECONSTRUCTION", "PEDAGOGICAL_CONVENTION",
}
EVIDENCE_ROLES = {"DIRECT_CLASSICAL_EVIDENCE", "REPORTED_CLASSICAL_EVIDENCE", "SECONDARY_EVIDENCE", "MODERN_VARIETY_COMPARATIVE"}
VOWEL_LENGTH_STATES = {"SHORT", "LONG", "UNKNOWN", "NOT_APPLICABLE", "NOT_REVIEWED"}
SALTILLO_STATES = {"PRESENT", "ABSENT", "UNKNOWN", "NOT_APPLICABLE", "NOT_REVIEWED", "NOT_ATTESTED"}
DIRECT_WITNESS_SOURCES = {"A01", "A02", "A03", "A04"}
POLICY_SENTINELS = (
    "unmarked means SHORT",
    "unmarked means no saltillo",
    "orthography equals narrow IPA",
    "modern pronunciation is DIRECT_CLASSICAL_EVIDENCE",
    "GDN entry means inspected historical Witness",
    "all cu/uc are globally rewritten",
    "automatic mass IPA",
    "audio generation",
    "Execution Agent approval",
)
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".mp4", ".aac", ".opus", ".wma", ".m4b", ".aiff", ".aif", ".mid", ".midi"}

PHONEMIC_RE = re.compile(r"/[^\[\]/]+/")
PHONETIC_RE = re.compile(r"\[[^\[\]/]*\]")

KNOWN_APPROVAL_REFERENCES = {"ORCHESTRATOR_REVIEWER_GATE_4_PASS"}
GATE_4_CLOSED_RE = re.compile(r"Gate\s*4\s*:\s*PASS\s*/\s*CLOSED", re.IGNORECASE)


def load(path: Path):
    with path.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def require_string(obj, key, errors, category, label):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{category}: {label}: missing or empty {key}")


def check_provenance(claim, errors, label):
    prov = claim.get("editorial_provenance", {})
    required = ("actor_role", "actor_id", "tool", "tool_version", "timestamp", "action", "from_state", "to_state", "review_status")
    missing = [key for key in required if not isinstance(prov.get(key), str) or not prov[key].strip()]
    if missing:
        errors.append(f"PROVENANCE_STATE: {label}: missing provenance fields: {', '.join(missing)}")
        return
    if prov.get("to_state") != claim.get("editorial_state"):
        errors.append(f"PROVENANCE_STATE: {label}: recorded to_state differs from editorial_state")
    if prov.get("actor_role") == "EXECUTION_AGENT" and prov.get("review_status") != "NOT_REVIEWED":
        errors.append(f"PROVENANCE_STATE: {label}: EXECUTION_AGENT origin cannot claim human review")


def check_vowel_length(field, label, errors, lemma_scoped, token_rule=True):
    value = field.get("value")
    if value not in VOWEL_LENGTH_STATES:
        errors.append(f"VOWEL_LENGTH_EVIDENCE_REQUIRED: {label}: invalid state {value}")
        return
    ev = field.get("evidence") or []
    if not isinstance(ev, list) or not all(isinstance(eid, str) for eid in ev):
        errors.append(f"EVIDENCE_REFERENCE: {label}: evidence is not a list of ids")
        return
    if value in {"SHORT", "LONG"}:
        if not ev:
            errors.append(f"VOWEL_LENGTH_EVIDENCE_REQUIRED: {label}: marked {value} without evidence")
        elif token_rule and value == "SHORT" and not any(eid in lemma_scoped for eid in ev):
            errors.append(f"AUTO_SHORT_INFERENCE: {label}: unmarked-to-SHORT without token evidence")
    elif ev:
        errors.append(f"UNKNOWN_WITH_EVIDENCE: {label}: absent state {value} cannot carry evidence")


def check_saltillo(field, label, errors):
    value = field.get("value")
    if value not in SALTILLO_STATES:
        errors.append(f"SALTILLO_EVIDENCE_REQUIRED: {label}: invalid state {value}")
        return
    ev = field.get("evidence") or []
    if value in {"PRESENT", "ABSENT"}:
        if not ev:
            errors.append(f"SALTILLO_EVIDENCE_REQUIRED: {label}: marked {value} without evidence")
    elif ev:
        errors.append(f"UNKNOWN_WITH_EVIDENCE: {label}: absent state {value} cannot carry evidence")


def resolve_refs(refs, known, errors, category, label):
    if isinstance(refs, list) and all(isinstance(r, str) for r in refs):
        for ref in refs:
            if ref not in known:
                errors.append(f"{category}: {label}: unresolved {ref}")
    elif refs is not None:
        errors.append(f"{category}: {label}: references must be a list of ids")


def audio_scan(errors):
    found = []
    for base in SCAN_DIRS:
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
                found.append(str(path.relative_to(ROOT)))
    if found:
        errors.append(f"AUDIO_PRESENT: forbidden audio/media files: {', '.join(sorted(found))}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read-only validation (default)")
    parser.parse_args()
    errors: list[str] = []
    source_forms_by_lemma: dict[str, dict[str, str]] = {}

    try:
        registry, _profiles = load_metadata(ROOT)
    except Exception as exc:
        return fail([f"SOURCE_REFERENCE: registry load failed: {exc}"])

    source_ids = set(registry)
    modern_sources = {
        sid for sid, meta in registry.items()
        if sid.startswith("C") or "modern" in meta["scope"].get("variety", "").casefold()
    }

    lemma_paths = sorted(LEMMA_DIR.glob("*.yml"))
    if len(lemma_paths) != EXPECTED_LEMMAS:
        errors.append(f"SOURCE_FORM_INTEGRITY: expected {EXPECTED_LEMMAS} lemma files, found {len(lemma_paths)}")
    for path in lemma_paths:
        try:
            record = load(path)
        except Exception as exc:
            errors.append(f"SOURCE_FORM_INTEGRITY: {path.name}: unreadable: {exc}")
            continue
        lid = record.get("lemma", {}).get("id")
        source_forms_by_lemma[lid] = {
            f.get("form_id"): f.get("value") for f in record.get("forms", []) if f.get("layer") == "SOURCE_FORM"
        }
        for form in record.get("forms", []):
            if form.get("layer") == "SOURCE_FORM" and not isinstance(form.get("value"), str):
                errors.append(f"SOURCE_FORM_INTEGRITY: {lid}: SOURCE_FORM value is not a string")

    try:
        baseline = load(BASELINE_PATH)
    except Exception as exc:
        return fail([f"SOURCE_FORM_INTEGRITY: baseline unreadable: {exc}"])
    for lid, entry in baseline.get("lemmas", {}).items():
        if source_forms_by_lemma.get(lid, {}) != entry.get("source_forms", {}):
            errors.append(f"SOURCE_FORM_MUTATION: {lid}: canonical SOURCE_FORM differs from gate3_baseline")

    try:
        evidence_doc = load(EVIDENCE_PATH)
    except Exception as exc:
        return fail([f"SCHEMA_ERROR: evidence.yml unreadable: {exc}"])
    evidence = evidence_doc.get("evidence", [])
    if len(evidence) != EXPECTED_EVIDENCE:
        errors.append(f"EVIDENCE_REFERENCE: expected {EXPECTED_EVIDENCE} Evidence records, found {len(evidence)}")
    evidence_by_id: dict[str, dict] = {}
    lemma_scoped_ids: dict[str, set[str]] = {}
    for record in evidence:
        eid = record.get("evidence_id")
        if not isinstance(eid, str) or not eid:
            errors.append("EVIDENCE_REFERENCE: Evidence without evidence_id")
            continue
        if eid in evidence_by_id:
            errors.append(f"DUPLICATE_EVIDENCE_ID: {eid}")
        evidence_by_id[eid] = record
        sid = record.get("source_id")
        if sid not in source_ids:
            errors.append(f"SOURCE_REFERENCE: {eid}: unknown Source ID {sid}")
        if record.get("mediation_level") not in MEDIATION_LEVELS:
            errors.append(f"EVIDENCE_REFERENCE: {eid}: invalid mediation level")
        role = record.get("evidence_role")
        if role not in EVIDENCE_ROLES:
            errors.append(f"EVIDENCE_REFERENCE: {eid}: invalid evidence_role {role}")
        if not isinstance(record.get("direct_witness_inspected"), bool):
            errors.append(f"DIRECT_WITNESS_INSPECTION: {eid}: direct_witness_inspected must be boolean")
        investigated = record.get("direct_witness_inspected") is True
        if role == "DIRECT_CLASSICAL_EVIDENCE":
            if sid not in DIRECT_WITNESS_SOURCES:
                errors.append(f"MODERN_AS_DIRECT_EVIDENCE: {eid}: {sid} cannot be DIRECT_CLASSICAL_EVIDENCE")
            if not investigated:
                errors.append(f"DIRECT_WITNESS_INSPECTION: {eid}: DIRECT_CLASSICAL_EVIDENCE requires inspected Witness")
        if sid in modern_sources and role == "DIRECT_CLASSICAL_EVIDENCE":
            errors.append(f"MODERN_AS_DIRECT_EVIDENCE: {eid}: modern-variety Source cannot be DIRECT_CLASSICAL_EVIDENCE")
        if role == "MODERN_VARIETY_COMPARATIVE" and sid not in modern_sources:
            errors.append(f"MODERN_AS_DIRECT_EVIDENCE: {eid}: comparative role on a non-modern Source")
        if record.get("mediation_level") == "DIRECT_WITNESS" and (not investigated or sid not in DIRECT_WITNESS_SOURCES):
            errors.append(f"DIRECT_WITNESS_INSPECTION: {eid}: DIRECT_WITNESS mediation without inspected historical Witness")
        require_string(record, "locator", errors, "EVIDENCE_REFERENCE", eid)
        require_string(record, "accessed_at", errors, "EVIDENCE_REFERENCE", eid)
        lid = record.get("lemma_id")
        if lid is not None:
            if lid not in baseline.get("lemmas", {}):
                errors.append(f"EVIDENCE_REFERENCE: {eid}: unknown lemma_id {lid}")
            allowed = set(source_forms_by_lemma.get(lid, {}).values())
            for form in record.get("source_forms") or []:
                if form not in allowed:
                    errors.append(f"EVIDENCE_REFERENCE: {eid}: source_form {form!r} not in canonical lemma forms")
            lemma_scoped_ids.setdefault(lid, set()).add(eid)
            require_string(record, "pilot_attestation_id", errors, "EVIDENCE_REFERENCE", eid)
            require_string(record, "access_basis", errors, "EVIDENCE_REFERENCE", eid)
            require_string(record, "capture_accessed_at", errors, "EVIDENCE_REFERENCE", eid)
            if record.get("gate4_online_entry_reinspection") is not False:
                errors.append(f"DIRECT_WITNESS_INSPECTION: {eid}: per-token evidence cannot claim reinspection now")

    claim_paths = sorted(CLAIMS_DIR.glob("*.yml"))
    if len(claim_paths) != EXPECTED_CLAIMS:
        errors.append(f"CLAIM_COUNT: expected {EXPECTED_CLAIMS} Claims, found {len(claim_paths)}")
    claims_by_id: dict[str, dict] = {}
    for path in claim_paths:
        try:
            claim = load(path)
        except Exception as exc:
            errors.append(f"CLAIM_COUNT: {path.name}: unreadable: {exc}")
            continue
        cid = claim.get("claim_id")
        if cid != path.stem:
            errors.append(f"CLAIM_ID: {cid} stored under filename {path.stem}.yml")
        if not isinstance(cid, str) or cid in claims_by_id:
            errors.append(f"DUPLICATE_CLAIM_ID: {cid}")
        if cid:
            claims_by_id[cid] = claim
        for key, vocab, category in (
            ("topic", CLAIM_TOPICS, "CLAIM_TOPIC"),
            ("layer", POLICY_LAYERS, "CLAIM_LAYER"),
            ("certainty_dimension", CERTAINTY_DIMENSIONS, "CLAIM_CERTAINTY"),
            ("modality", MODALITIES, "CLAIM_MODALITY"),
            ("confidence", CONFIDENCES, "CLAIM_CONFIDENCE"),
            ("editorial_state", EDITORIAL_STATES, "CLAIM_EDITORIAL_STATE"),
        ):
            if claim.get(key) not in vocab:
                errors.append(f"{category}: {cid}: invalid {key} {claim.get(key)!r}")
        scope = claim.get("scope", {})
        require_string(scope, "variety", errors, "CLAIM_SCOPE", cid)
        require_string(scope, "period", errors, "CLAIM_SCOPE", cid)
        if scope.get("variety") != "Classical Nahuatl":
            errors.append(f"CLAIM_SCOPE: {cid}: variety is not Classical Nahuatl")
        require_string(claim, "statement", errors, "CLAIM_SCOPE", cid)
        evidence_refs = claim.get("evidence") or []
        if claim.get("editorial_state") not in {"DRAFT", "QUARANTINED"} and not evidence_refs:
            errors.append(f"CLAIM_EVIDENCE_REQUIRED: {cid}: non-draft Claim without Evidence")
        resolve_refs(evidence_refs, evidence_by_id, errors, "EVIDENCE_REFERENCE", cid)
        resolve_refs(claim.get("counterevidence") or [], evidence_by_id, errors, "EVIDENCE_REFERENCE", f"{cid} counterevidence")
        ipa = claim.get("phonemic_ipa")
        if ipa is not None and not (isinstance(ipa, str) and PHONEMIC_RE.fullmatch(ipa)):
            errors.append(f"PHONEMIC_IPA_FORMAT: {cid}: phonemic_ipa must be a single /.../ string, got {ipa!r}")
        check_provenance(claim, errors, cid)

    try:
        policy = load(POLICY_PATH)
    except Exception as exc:
        return fail([f"SCHEMA_ERROR: classical_phonology_v1.yml unreadable: {exc}"])
    if policy.get("policy_id") != "classical_phonology_v1":
        errors.append("POLICY_STATUS: policy_id is not classical_phonology_v1")
    require_string(policy, "version", errors, "POLICY_STATUS", "classical_phonology_v1")
    policy_status = policy.get("status")
    if policy_status not in {"DRAFT", "APPROVED"}:
        errors.append(f"POLICY_STATUS: status must be DRAFT or APPROVED, found {policy_status!r}")
    if policy_status == "APPROVED":
        approval_ref = policy.get("approval_reference")
        if approval_ref not in KNOWN_APPROVAL_REFERENCES:
            errors.append(f"POLICY_STATUS: APPROVED policy requires a known approval_reference, found {approval_ref!r}")
        for key in ("approved_scope", "not_approved_as"):
            value = policy.get(key)
            if not (isinstance(value, list) and all(isinstance(item, str) and item for item in value)):
                errors.append(f"POLICY_STATUS: APPROVED policy requires non-empty {key}")
        try:
            gate_status_text = GATE_STATUS_PATH.read_text(encoding="utf-8-sig")
        except OSError:
            gate_status_text = ""
        if not GATE_4_CLOSED_RE.search(gate_status_text):
            errors.append("POLICY_STATUS: APPROVED policy requires Gate 4 CLOSED in docs/GATE_STATUS.md")
    if policy.get("scope", {}).get("variety") != "Classical Nahuatl":
        errors.append("POLICY_STATUS: policy scope variety is not Classical Nahuatl")
    excluded = set(policy.get("scope", {}).get("excluded", []))
    for name in ("Hueyapan", "Mecayapan"):
        if name not in excluded:
            errors.append(f"POLICY_STATUS: excluded scope must keep {name}")
    resolve_refs(policy.get("references") or [], evidence_by_id, errors, "SOURCE_REFERENCE", "policy references")
    if not policy.get("open_decisions"):
        errors.append("POLICY_STATUS: open_decisions must remain non-empty")
    punished = set(policy.get("prohibited_inferences") or [])
    for sentinel in POLICY_SENTINELS:
        if sentinel not in punished:
            errors.append(f"POLICY_STATUS: prohibited inference lost from policy: {sentinel!r}")

    return finish(errors, evidence_by_id, claims_by_id, baseline, evidence, lemma_scoped_ids, source_ids)


def finish(errors, evidence_by_id, claims_by_id, baseline, evidence, lemma_scoped_ids, source_ids):
    if errors:
        return fail(errors)

    try:
        integration = load(INTEGRATION_PATH)
        fixtures = load(FIXTURES_PATH)
        audio_model = load(AUDIO_MODEL_PATH)
    except Exception as exc:
        return fail([f"SCHEMA_ERROR: {exc}"])

    errors = []
    metric_claims = []
    items = integration.get("items", [])
    if len(items) != EXPECTED_INTEGRATION:
        errors.append(f"INTEGRATION_CAP: expected {EXPECTED_INTEGRATION} integration items, found {len(items)}")
    if integration.get("max_lemmas") != EXPECTED_INTEGRATION:
        errors.append(f"INTEGRATION_CAP: max_lemmas {integration.get('max_lemmas')} differs from lock {EXPECTED_INTEGRATION}")
    fixtures_by_id = {}
    for case in fixtures.get("cases", []):
        cid = case.get("case_id")
        if cid in fixtures_by_id:
            errors.append(f"DUPLICATE_FIXTURE_ID: {cid}")
        fixtures_by_id[cid] = case

    seen_lemmas = set()
    for item in items:
        lid = item.get("lemma_id")
        seen_lemmas.add(lid)
        label = f"integration {lid}"
        case_id = item.get("case_id")
        fixture = fixtures_by_id.get(case_id)
        if fixture is None:
            errors.append(f"INTEGRATION_REFERENCE: {label}: unknown case_id {case_id}")
        elif fixture.get("lemma_id_if_available") != lid or fixture.get("source_form") != item.get("source_form"):
            errors.append(f"INTEGRATION_REFERENCE: {label}: disconnected from fixture {case_id}")
        if lid not in baseline.get("lemmas", {}):
            errors.append(f"INTEGRATION_REFERENCE: {label}: lemma not in Gate 3 baseline")
        base_sources = baseline.get("lemmas", {}).get(lid, {}).get("source_forms", {})
        if lid in baseline.get("lemmas", {}):
            if item.get("source_form_id") not in base_sources:
                errors.append(f"SOURCE_FORM_MUTATION: {label}: unknown source_form_id")
            elif base_sources.get(item.get("source_form_id")) != item.get("source_form"):
                errors.append(f"SOURCE_FORM_MUTATION: {label}: source_form differs from baseline")
        for key, vocab, category in (
            ("editorial_state", EDITORIAL_STATES, "CLAIM_EDITORIAL_STATE"),
            ("modality", MODALITIES, "CLAIM_MODALITY"),
            ("confidence", CONFIDENCES, "CLAIM_CONFIDENCE"),
            ("layer", POLICY_LAYERS, "CLAIM_LAYER"),
        ):
            if item.get(key) not in vocab:
                errors.append(f"{category}: {label}: invalid {key}")
        resolve_refs(item.get("evidence") or [], evidence_by_id, errors, "EVIDENCE_REFERENCE", label)
        resolve_refs(item.get("claim_ids") or [], claims_by_id, errors, "INTEGRATION_REFERENCE", label)
        check_vowel_length(item.get("vowel_length", {}), f"{label} vowel_length", errors,
                           lemma_scoped_ids.get(lid, set()))
        check_saltillo(item.get("saltillo", {}), f"{label} saltillo", errors)
        for key in ("phonemic_ipa", "phonetic_ipa"):
            value = item.get(key)
            if value is None or value == "NOT_REVIEWED":
                continue
            if key == "phonemic_ipa":
                if not (isinstance(value, str) and PHONEMIC_RE.fullmatch(value)):
                    errors.append(f"PHONEMIC_IPA_FORMAT: {label}: phonemic_ipa must be /.../, got {value!r}")
            else:
                if not (isinstance(value, str) and PHONETIC_RE.fullmatch(value)):
                    errors.append(f"PHONETIC_IPA_FORMAT: {label}: phonetic_ipa must be [...] , got {value!r}")
                if "[" not in value or not (item.get("evidence") and item.get("confidence")):
                    errors.append(f"PHONETIC_REALIZATION_GUARD: {label}: phonetic_ipa requires Evidence and Confidence")
        require_string(item, "notes", errors, "INTEGRATION_REFERENCE", label)
        if item.get("vowel_length", {}).get("value") in {"SHORT", "LONG"}:
            metric_claims.append((lid, item.get("vowel_length", {}).get("value")))
    if len(seen_lemmas) != len(integration.get("items", [])):
        errors.append("INTEGRATION_CAP: duplicate lemma_id in integration sample")

    if len(fixtures.get("cases", [])) != EXPECTED_FIXTURES:
        errors.append(f"FIXTURE_REFERENCE: expected {EXPECTED_FIXTURES} fixture cases, found {len(fixtures.get('cases', []))}")
    for case in fixtures.get("cases", []):
        cid = case.get("case_id")
        if case.get("source") not in source_ids:
            errors.append(f"SOURCE_REFERENCE: {cid}: unknown Source")
        if case.get("mediation_level") not in MEDIATION_LEVELS:
            errors.append(f"FIXTURE_REFERENCE: {cid}: invalid mediation level")
        require_string(case, "source_form", errors, "FIXTURE_REFERENCE", cid)
        require_string(case, "locator", errors, "FIXTURE_REFERENCE", cid)
        require_string(case, "phenomenon", errors, "FIXTURE_REFERENCE", cid)
        require_string(case, "analysis_candidate", errors, "FIXTURE_REFERENCE", cid)
        require_string(case, "open_question", errors, "FIXTURE_REFERENCE", cid)
        require_string(case, "notes", errors, "FIXTURE_REFERENCE", cid)
        resolve_refs(case.get("evidence") or [], evidence_by_id, errors, "EVIDENCE_REFERENCE", cid)
        if not (case.get("evidence") or []):
            errors.append(f"FIXTURE_EVIDENCE: {cid}: fixture case without Evidence")
        if case.get("orthographic_evidence", {}).get("preserved_codepoints") is not True:
            errors.append(f"FIXTURE_EVIDENCE: {cid}: preserved_codepoints must be true")
        lid = case.get("lemma_id_if_available")
        if lid != "NOT_APPLICABLE":
            if lid not in baseline.get("lemmas", {}):
                errors.append(f"FIXTURE_REFERENCE: {cid}: unknown lemma_id {lid}")
            fid = case.get("orthographic_evidence", {}).get("source_form_id")
            base_sources = baseline.get("lemmas", {}).get(lid, {}).get("source_forms", {})
            if fid is None or base_sources.get(fid) != case.get("source_form"):
                errors.append(f"SOURCE_FORM_MUTATION: {cid}: source_form does not match lemma baseline")
        for key, allowed in (("phonemic_candidate", PHONEMIC_RE), ("phonetic_candidate", PHONETIC_RE)):
            value = case.get(key)
            if value is not None and value != "NOT_REVIEWED":
                if not (isinstance(value, str) and allowed.fullmatch(value)):
                    errors.append(f"PHONEMIC_IPA_FORMAT: {cid}: bad {key} {value!r}")
        if case.get("vowel_length"):
            check_vowel_length(case.get("vowel_length"), f"fixture {cid} vowel_length", errors, set(), token_rule=False)
        if case.get("saltillo"):
            check_saltillo(case.get("saltillo"), f"fixture {cid} saltillo", errors)
        for key in ("vowel_length", "saltillo"):
            if case.get(key):
                resolve_refs(case.get(key).get("evidence") or [], evidence_by_id, errors, "EVIDENCE_REFERENCE", f"{cid} {key}")

    if audio_model.get("status") != "CONCEPT_ONLY":
        errors.append(f"AUDIO_PRESENT: audio model status must remain CONCEPT_ONLY, found {audio_model.get('status')!r}")
    if audio_model.get("recordings") not in (None, []):
        errors.append("AUDIO_PRESENT: audio model must carry no recording instances")
    audio_scan(errors)

    if errors:
        return fail(errors)
    metrics = {
        "schema": "gate4-validation-v1",
        "claims_total": len(claims_by_id),
        "evidence_total": len(evidence_by_id),
        "fixtures_total": len(fixtures.get("cases", [])),
        "integration_lemma_count": len(integration.get("items", [])),
        "integration_unique_lemmas": len(seen_lemmas),
        "claims_by_topic": dict(sorted(Counter(c.get("topic") for c in claims_by_id.values()).items())),
        "claims_by_modality": dict(sorted(Counter(c.get("modality") for c in claims_by_id.values()).items())),
        "claims_by_confidence": dict(sorted(Counter(c.get("confidence") for c in claims_by_id.values()).items())),
        "claims_by_layer": dict(sorted(Counter(c.get("layer") for c in claims_by_id.values()).items())),
        "claims_editorial_states": dict(sorted(Counter(c.get("editorial_state") for c in claims_by_id.values()).items())),
        "evidence_by_role": dict(sorted(Counter(e.get("evidence_role") for e in evidence).items())),
        "evidence_by_mediation": dict(sorted(Counter(e.get("mediation_level") for e in evidence).items())),
        "integration_marked_segments": dict(sorted(Counter(dict(metric_claims)).items())),
    }
    print("GATE 4 VALIDATION: PASS")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


def fail(errors):
    print("GATE 4 VALIDATION: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        result = main()
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result = fail([f"SCHEMA_ERROR: {exc}"])
    raise SystemExit(result)
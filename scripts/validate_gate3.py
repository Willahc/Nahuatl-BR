#!/usr/bin/env python3
"""Validate the bounded Gate 3 pilot and derive its metrics.

The parser intentionally supports only the JSON-compatible YAML emitted by the
pilot. YAML 1.2 is a superset of JSON, so no third-party dependency is needed.
This is validation/measurement tooling, not an ingestion pipeline.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEMMA_DIR = ROOT / "data" / "pilot" / "lemmas"
REGISTRY_DIR = ROOT / "data" / "source_registry"
INDEX_PATH = ROOT / "data" / "pilot" / "pilot_index.yml"
METRICS_PATH = ROOT / "data" / "pilot" / "pilot_metrics.json"

EDITORIAL_STATES = {"DRAFT", "IN_REVIEW", "APPROVED", "PUBLISHED", "QUARANTINED", "REJECTED", "DEPRECATED"}
MODALITIES = {"OBSERVED", "REPORTED", "INFERRED", "RECONSTRUCTED", "EDITORIAL"}
CONFIDENCES = {"UNASSESSED", "LOW", "MEDIUM", "HIGH"}
LAYERS = {"SOURCE_FORM", "DIPLOMATIC_FORM", "NORMALIZED_FORM", "PEDAGOGICAL_FORM", "SEARCH_KEY", "PHONOLOGICAL_REPRESENTATION"}
MEDIATION_LEVELS = {"DIRECT_WITNESS", "HISTORICAL_EDITION", "MODERN_EDITION", "AGGREGATOR"}
DIVERGENCE_TYPES = {"SEMANTIC_VARIATION", "POLYSEMY_CANDIDATE", "HOMONYMY_CANDIDATE", "FRAME_VARIATION", "SOURCE_GRANULARITY_DIFFERENCE", "TRUE_CONTRADICTION", "LEXICAL_IDENTITY_UNRESOLVED"}


def load(path: Path):
    with path.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def main() -> int:
    errors: list[str] = []
    paths = sorted(LEMMA_DIR.glob("*.yml"))
    if len(paths) != 50:
        errors.append(f"expected 50 lemma files, found {len(paths)}")
    records = []
    for path in paths:
        try:
            records.append((path, load(path)))
        except Exception as exc:
            errors.append(f"{path.name}: unreadable JSON-compatible YAML: {exc}")

    source_ids = set()
    for path in REGISTRY_DIR.glob("*.yml"):
        first = path.read_text(encoding="utf-8").splitlines()[0]
        if first.startswith("source_id:"):
            source_ids.add(first.split(":", 1)[1].strip().strip('"'))

    ids = [r["lemma"]["id"] for _, r in records]
    for duplicate, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate lemma id: {duplicate}")

    claims_total = 0
    modalities: Counter[str] = Counter()
    confidences: Counter[str] = Counter()
    att_sources: Counter[str] = Counter()
    index_rows = []

    for path, record in records:
        lid = record.get("lemma", {}).get("id", path.stem)
        lemma = record.get("lemma", {})
        if lemma.get("variety") != "Classical Nahuatl":
            errors.append(f"{lid}: variety is not Classical Nahuatl")
        if lemma.get("status") not in EDITORIAL_STATES:
            errors.append(f"{lid}: invalid lemma editorial state")

        forms = record.get("forms", [])
        source_forms = [f for f in forms if f.get("layer") == "SOURCE_FORM"]
        if not source_forms:
            errors.append(f"{lid}: no SOURCE_FORM")
        for form in forms:
            if form.get("layer") not in LAYERS:
                errors.append(f"{lid}: form without valid representation layer")
            if form.get("layer") == "SEARCH_KEY" and form.get("evidence") not in ("NOT_APPLICABLE", [], None):
                errors.append(f"{lid}: SEARCH_KEY used as evidence")
            if form.get("layer") == "PEDAGOGICAL_FORM" and any(c in str(form.get("value", "")) for c in "āēīōĀĒĪŌ") and not form.get("evidence"):
                errors.append(f"{lid}: pedagogical macron without evidence")

        senses = record.get("senses", [])
        translations = [t for s in senses for t in s.get("translations", [])]
        if not translations:
            errors.append(f"{lid}: no PT-BR translation")
        for trans in translations:
            if trans.get("language") != "pt-BR" or trans.get("modality") != "EDITORIAL":
                errors.append(f"{lid}: PT-BR translation is not EDITORIAL")
            if trans.get("editorial_state") not in EDITORIAL_STATES:
                errors.append(f"{lid}: invalid translation editorial state")

        claims = record.get("claims", [])
        claims_total += len(claims)
        claim_ids = set()
        for claim in claims:
            cid = claim.get("claim_id")
            claim_ids.add(cid)
            if claim.get("modality") not in MODALITIES:
                errors.append(f"{lid}/{cid}: Claim without valid modality")
            if claim.get("confidence") not in CONFIDENCES:
                errors.append(f"{lid}/{cid}: Claim without valid confidence")
            if claim.get("editorial_state") not in EDITORIAL_STATES:
                errors.append(f"{lid}/{cid}: invalid editorial state")
            modalities[claim.get("modality", "MISSING")] += 1
            confidences[claim.get("confidence", "MISSING")] += 1

        attestations = record.get("attestations", [])
        if not attestations:
            errors.append(f"{lid}: no historical Attestation")
        for att in attestations:
            sid = att.get("source")
            if not sid:
                errors.append(f"{lid}: Attestation without Source")
            elif sid not in source_ids:
                errors.append(f"{lid}: unknown Source ID {sid}")
            if not att.get("work"):
                errors.append(f"{lid}: Attestation without Work")
            locator = att.get("locator")
            if not locator or locator == "UNKNOWN":
                if not att.get("locator_absence_reason"):
                    errors.append(f"{lid}: empty Locator without justification")
            if "Hueyapan" in json.dumps(att, ensure_ascii=False):
                errors.append(f"{lid}: Hueyapan used as Classical evidence")
            mediation = att.get("mediation_level")
            if mediation not in MEDIATION_LEVELS:
                errors.append(f"{lid}: Attestation without valid mediation level")
            if mediation == "DIRECT_WITNESS" and (att.get("aggregator") or not att.get("direct_witness_inspected")):
                errors.append(f"{lid}: aggregator-mediated Attestation falsely labeled DIRECT_WITNESS")
            att_sources[sid or "MISSING"] += 1
        att_source_values = {a.get("source_form") for a in attestations}
        for form in source_forms:
            if form.get("value") not in att_source_values:
                errors.append(f"{lid}: SOURCE_FORM differs from every linked Attestation")

        evidence_ids = {e.get("evidence_id") for e in record.get("evidence", [])}
        for link in record.get("evidence_links", []):
            if link.get("claim_id") not in claim_ids:
                errors.append(f"{lid}: EvidenceLink points to unknown Claim")
            if link.get("evidence_id") not in evidence_ids:
                errors.append(f"{lid}: EvidenceLink points to unknown Evidence")
            if link.get("relation") == "CONTRADICTS":
                comparison = link.get("semantic_comparison", {})
                required = ("same_subject", "same_predicate", "same_sense", "same_context")
                if comparison.get("classification") != "TRUE_CONTRADICTION" or not all(comparison.get(key) is True for key in required):
                    errors.append(f"{lid}: CONTRADICTS lacks a structurally comparable TRUE_CONTRADICTION assessment")

        phon = record.get("phonological_information", {})
        if phon.get("saltillo") not in {"UNKNOWN", "NOT_REVIEWED", "NOT_ATTESTED"} and not phon.get("evidence"):
            errors.append(f"{lid}: saltillo filled without evidence")

        divergences = record.get("divergences", [])
        for divergence in divergences:
            if divergence.get("classification") not in DIVERGENCE_TYPES:
                errors.append(f"{lid}: invalid divergence classification")
        unique_historical = {a.get("source") for a in attestations if a.get("source") in {"A01", "A02", "A03", "A04"}}
        row = {
            "lemma_id": lid,
            "display_form": lemma.get("display_form"),
            "sources_count": len(unique_historical),
            "attestations_count": len(attestations),
            "has_pt_br": bool(translations),
            "has_context_reference": bool(record.get("corpus_references")),
            "has_context_text_inspected": any(c.get("context_text_inspected") is True for c in record.get("corpus_references", [])),
            "has_vowel_length_evidence": bool(phon.get("vowel_length_evidence")),
            "has_saltillo_evidence": bool(phon.get("saltillo_evidence")),
            "has_morphology": bool(record.get("morphology", {}).get("analyses")),
            "has_true_contradiction": any(d.get("classification") == "TRUE_CONTRADICTION" for d in divergences),
            "has_semantic_variation": any(d.get("classification") in {"SEMANTIC_VARIATION", "POLYSEMY_CANDIDATE", "HOMONYMY_CANDIDATE", "SOURCE_GRANULARITY_DIFFERENCE"} for d in divergences),
            "has_frame_variation": any(d.get("classification") == "FRAME_VARIATION" for d in divergences),
            "has_lexical_identity_unresolved": any(d.get("classification") == "LEXICAL_IDENTITY_UNRESOLVED" for d in divergences),
            "has_historical_attestation": bool(attestations),
            "has_direct_witness_attestation": any(a.get("mediation_level") == "DIRECT_WITNESS" for a in attestations),
            "has_aggregator_mediated_attestation": any(a.get("mediation_level") == "AGGREGATOR" for a in attestations),
            "review_status": lemma.get("status"),
        }
        index_rows.append(row)

    index = {"pilot_id": "gate3_classical_nahuatl_50", "generated_by": "scripts/validate_gate3.py", "lemmas": index_rows}
    metrics = {
        "total_lemmas": len(records),
        "with_pt_br": sum(r["has_pt_br"] for r in index_rows),
        "with_historical_attestation": sum(r["has_historical_attestation"] for r in index_rows),
        "with_direct_witness_attestation": sum(r["has_direct_witness_attestation"] for r in index_rows),
        "with_aggregator_mediated_attestation": sum(r["has_aggregator_mediated_attestation"] for r in index_rows),
        "with_two_historical_sources": sum(r["sources_count"] >= 2 for r in index_rows),
        "with_context_reference": sum(r["has_context_reference"] for r in index_rows),
        "with_context_text_inspected": sum(r["has_context_text_inspected"] for r in index_rows),
        "with_vowel_length_evidence": sum(r["has_vowel_length_evidence"] for r in index_rows),
        "with_saltillo_evidence": sum(r["has_saltillo_evidence"] for r in index_rows),
        "with_morphology": sum(r["has_morphology"] for r in index_rows),
        "with_conflicting_claims": sum(r["has_true_contradiction"] for r in index_rows),
        "with_semantic_variation": sum(r["has_semantic_variation"] for r in index_rows),
        "with_frame_variation": sum(r["has_frame_variation"] for r in index_rows),
        "with_lexical_identity_unresolved": sum(r["has_lexical_identity_unresolved"] for r in index_rows),
        "with_unknown_fields": sum("UNKNOWN" in json.dumps(rec, ensure_ascii=False) or "NOT_REVIEWED" in json.dumps(rec, ensure_ascii=False) for _, rec in records),
        "claims_total": claims_total,
        "claims_by_modality": dict(sorted(modalities.items())),
        "claims_by_confidence": dict(sorted(confidences.items())),
        "attestations_total": sum(att_sources.values()),
        "attestations_by_source": dict(sorted(att_sources.items())),
        "attestations_by_mediation": dict(sorted(Counter(a.get("mediation_level", "MISSING") for _, rec in records for a in rec.get("attestations", [])).items())),
    }
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors:
        print("GATE 3 VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("GATE 3 VALIDATION: PASS")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

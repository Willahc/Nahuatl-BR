#!/usr/bin/env python3
"""Deterministic Gate 5 research preview data exporter (read-only by default).

Builds preview/public/data/nahuatl-br.json from canonical data only
(data/pilot/lemmas, data/phonology, data/source_registry, data/policies,
docs/GATE_STATUS.md). The output contains no timestamps, no audio, no raw
corpus transcription and never uses C01/C02/C03 as sources. --check compares
the in-memory build with the committed file without writing.

Usage:
    python scripts/build_preview_data.py --write   # regenerate the committed file
    python scripts/build_preview_data.py --check   # compare (default, read-only)
"""

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.pipeline.gates import is_modern_source
from src.pipeline.models import PIPELINE_VERSION
from src.pipeline.loader import (
    load_gate3_baseline,
    load_gate_status,
    load_policy_orthography,
    load_policy_phonology,
    load_source_registry,
)

PREVIEW_DATA = _ROOT / "preview" / "public" / "data" / "nahuatl-br.json"
EXCLUDED_MODERN_SOURCES = {"C01", "C02", "C03"}


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def _non_absent(value):
    if isinstance(value, str):
        return value.upper() not in {"UNKNOWN", "NOT_REVIEWED", "NOT_APPLICABLE", "NOT_ATTESTED", "NOT_RECORDED"}
    return bool(value)


def _source_sort_key(sid: str):
    letter = sid[:1]
    digits = sid[1:]
    return (letter, int(digits) if digits.isdigit() else digits)


def build_preview_data(root: Path) -> dict:
    registry = load_source_registry(root)
    orthography = load_policy_orthography(root)
    phonology = load_policy_phonology(root)
    baseline = load_gate3_baseline(root)
    gate_status = load_gate_status(root)

    lemma_dir = root / "data" / "pilot" / "lemmas"
    claims_dir = root / "data" / "phonology" / "claims"
    evidence_doc = _load_json(root / "data" / "phonology" / "evidence.yml")
    integration = _load_json(root / "data" / "phonology" / "integration_sample.yml")

    lemma_paths = sorted(lemma_dir.glob("*.yml"))
    claim_ids = sorted(path.stem for path in claims_dir.glob("*.yml"))
    evidence_by_id = {rec.get("evidence_id"): rec for rec in evidence_doc.get("evidence", [])}
    integration_by_lemma = {}
    for item in integration.get("items", []):
        integration_by_lemma[item.get("lemma_id")] = item

    lemmas_out = []
    for path in lemma_paths:
        rec = _load_json(path)
        head = rec.get("lemma", {})
        lid = head.get("id")

        source_forms = []
        normalized_form = None
        pedagogical_form = "UNKNOWN"
        search_keys = []
        for form in rec.get("forms", []):
            layer = form.get("layer")
            value = form.get("value")
            if layer == "SOURCE_FORM":
                source_forms.append(value)
            elif layer == "NORMALIZED_FORM":
                normalized_form = value
            elif layer == "PEDAGOGICAL_FORM":
                pedagogical_form = value
            elif layer == "SEARCH_KEY":
                search_keys.append(value)

        interpretations = []
        pt_br = []
        for sense in rec.get("senses", []):
            if _non_absent(sense.get("interpretation")):
                interpretations.append(sense.get("interpretation"))
            for translation in sense.get("translations", []):
                if translation.get("language") == "pt-BR" and _non_absent(translation.get("text")):
                    pt_br.append(translation.get("text"))

        historical_glosses = []
        for claim in rec.get("claims", []):
            if claim.get("predicate") == "has_historical_gloss" and _non_absent(claim.get("value")):
                historical_glosses.append(claim.get("value"))

        phon_info = rec.get("phonological_information", {}) or {}
        phonology_out = {
            "vowel_length": phon_info.get("vowel_length", "NOT_REVIEWED"),
            "saltillo": phon_info.get("saltillo", "NOT_REVIEWED"),
            "status": phon_info.get("status", "NOT_REVIEWED"),
            "notes": [],
        }
        for evidence in phon_info.get("vowel_length_evidence", []) or []:
            if _non_absent(evidence.get("note")):
                phonology_out["notes"].append(evidence["note"])

        integration_item = integration_by_lemma.get(lid)
        if integration_item is not None:
            proposal = {
                "profile": integration.get("profile"),
                "editorial_state": integration_item.get("editorial_state"),
                "modality": integration_item.get("modality"),
                "confidence": integration_item.get("confidence"),
                "vowel_length": (integration_item.get("vowel_length", {}) or {}).get("value"),
                "saltillo": (integration_item.get("saltillo", {}) or {}).get("value"),
                "phonemic_ipa": integration_item.get("phonemic_ipa"),
                "phonetic_ipa": integration_item.get("phonetic_ipa"),
                "claim_ids": integration_item.get("claim_ids", []),
                "notes": integration_item.get("notes"),
            }
            phonology_out["analysis_candidate"] = proposal

        sources = []
        seen_source_ids = set()
        for attestation in rec.get("attestations", []):
            sid = attestation.get("source")
            record = {
                "source_id": sid,
                "work": attestation.get("work"),
                "locator": attestation.get("locator"),
                "url": attestation.get("url"),
                "mediation_level": attestation.get("mediation_level"),
                "direct_witness_inspected": attestation.get("direct_witness_inspected"),
            }
            sources.append(record)
            if sid:
                seen_source_ids.add(sid)

        references = []
        for reference in rec.get("corpus_references", []):
            references.append({
                "source": reference.get("source"),
                "work": reference.get("work"),
                "locator": reference.get("locator"),
                "url": reference.get("url"),
                "use": reference.get("use"),
            })

        claims_affecting_lemma = [cid for cid in claim_ids if cid.startswith(lid)]

        lemmas_out.append({
            "id": lid,
            "display_form": head.get("display_form"),
            "variety": head.get("variety"),
            "status": head.get("status"),
            "forms": {
                "source_forms": source_forms,
                "normalized_form": normalized_form,
                "pedagogical_form": pedagogical_form,
                "search_keys": search_keys,
            },
            "interpretations": interpretations,
            "pt_br_editorial": pt_br,
            "historical_glosses": historical_glosses,
            "phonology": phonology_out,
            "sources": sources,
            "references": references,
            "notes": rec.get("notes"),
            "claim_ids": claims_affecting_lemma,
        })

    sources_out = {}
    for sid in sorted(registry.ingredients(), key=_source_sort_key):
        entry = registry.get(sid)
        if is_modern_source(entry):
            continue
        sources_out[sid] = {
            "name": entry.get("name"),
            "institution": entry.get("institution", "NOT_RECORDED"),
            "url": entry.get("url"),
            "recommended_role": entry.get("recommended_role", "NOT_RECORDED"),
        }

    status_out = {}
    for row in gate_status:
        status_out[row.get("gate")] = {
            "status": row.get("status"),
            "closure": row.get("closure"),
        }

    return {
        "schema": "nahuatl-br-preview-v1",
        "pipeline_version": PIPELINE_VERSION,
        "generated_by": "scripts/build_preview_data.py",
        "generated_at": "NOT_RECORDED",
        "orthography_profile": f"{orthography['policy'].get('policy_id')}@{orthography['policy'].get('version')}",
        "phonology_profile": f"classical_phonology_v1@{phonology.get('version')}",
        "gate_status": status_out,
        "counts": {
            "lemmas": len(lemmas_out),
            "sources": len(sources_out),
            "claims_total": len(claim_ids),
            "evidence_total": len(evidence_by_id),
            "integration_items": len(integration.get("items", [])),
        },
        "sources": sources_out,
        "lemmas": lemmas_out,
    }


def _check() -> int:
    errors = []
    built = build_preview_data(_ROOT)
    if not PREVIEW_DATA.exists():
        return 1 if _fail([f"EXPORT: missing {PREVIEW_DATA.relative_to(_ROOT)} (run with --write)"]) else 0
    committed = _load_json(PREVIEW_DATA)
    if committed.get("schema") != built.get("schema"):
        errors.append(f"EXPORT: schema drift {committed.get('schema')!r}")
    if committed.get("counts", {}).get("lemmas") != 50:
        errors.append(f"EXPORT: expected exactly 50 lemmas, found {committed.get('counts', {}).get('lemmas')}")
    if committed.get("generated_at") != "NOT_RECORDED":
        errors.append("EXPORT: generated_at must be NOT_RECORDED (deterministic build)")
    used_modern_ids = set(committed.get("sources", {}))
    for sid in ("C01", "C02", "C03"):
        if sid in used_modern_ids:
            errors.append(f"EXPORT: modern Source {sid} must not appear as a preview source")
    if committed != built:
        if not (isinstance(committed, dict) and isinstance(built, dict)):
            errors.append("EXPORT: committed file structure mismatch")
        else:
            key_mismatch = [k for k in built.keys() if built.get(k) != committed.get(k)]
            errors.append(f"EXPORT: committed file is not reproducible from canonical data (keys differing: {', '.join(key_mismatch) or 'nested'})")
    if errors:
        return _fail(errors)
    print("GATE 5 EXPORT: PASS (deterministic preview data)")
    return 0


def _fail(errors):
    print("GATE 5 EXPORT: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write preview/public/data/nahuatl-br.json")
    parser.add_argument("--check", action="store_true", help="compare committed file with in-memory build (default)")
    args = parser.parse_args()
    if args.write:
        PREVIEW_DATA.parent.mkdir(parents=True, exist_ok=True)
        data = build_preview_data(_ROOT)
        PREVIEW_DATA.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"GATE 5 EXPORT: wrote {PREVIEW_DATA.relative_to(_ROOT)}")
        return 0
    return _check()


if __name__ == "__main__":
    try:
        result = main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        result = _fail([f"EXPORT: {exc}"])
    raise SystemExit(result)
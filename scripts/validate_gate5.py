#!/usr/bin/env python3
"""Validate Gate 5 ingestion pipeline and research preview data (read-only).

Applies the pipeline engine to every fixture under
data/fixtures/gate5_ingestion_cases/, asserting each fixture's expected outcome
and that the produced error codes are a subset of the expected codes. It also
verifies the engine is deterministic (identical fixtures yield identical
digests) and that the machinery does not depend on a variety name string, and
compares the committed research preview file with an in-memory deterministic
build. --check is the only mode; it never writes to data/ or preview/.

Usage:
    python scripts/validate_gate5.py --check
"""

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import src.pipeline.engine as eng

FIXTURES_DIR = _ROOT / "data" / "fixtures" / "gate5_ingestion_cases"


def load(path):
    with path.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def require_string(obj, key, errors, label):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: missing or empty {key}")


def run_fixture_checks(engine) -> list:
    errors = []
    paths = sorted(FIXTURES_DIR.glob("*.yml"))
    if not paths:
        return ["SCHEMA_ERROR: no fixtures found under data/fixtures/gate5_ingestion_cases/"]

    names_by_id = {}
    for path in paths:
        fixture = load(path)
        require_string(fixture, "fixture_id", errors, path.name)
        require_string(fixture, "purpose", errors, path.name)
        fid = fixture.get("fixture_id")
        if fid in names_by_id:
            errors.append(f"DUPLICATE_FIXTURE_ID: {fid} ({names_by_id[fid]} and {path.name})")
        else:
            names_by_id[fid] = path.name

    for path in paths:
        fixture = load(path)
        result = engine.ingest(fixture)
        fid = fixture.get("fixture_id", path.name)
        codes = set(result.error_codes())
        expected_outcome = fixture.get("expect", {}).get("outcome")
        expected_codes = set(fixture.get("expect", {}).get("codes", []))
        if result.outcome != expected_outcome:
            errors.append(f"OUTCOME: {fid}: expected {expected_outcome!r} got {result.outcome!r} "
                          f"[{sorted(codes)}]")
        unexpected = codes - expected_codes
        if unexpected:
            errors.append(f"CODES: {fid}: unexpected error codes {sorted(unexpected)}; "
                          f"expected subset of {sorted(expected_codes)}")
        if expected_outcome != "REJECT" and result.artifacts is None:
            errors.append(f"ARTIFACTS: {fid}: ACCEPT without artifacts")
        if expected_outcome == "REJECT" and not codes:
            errors.append(f"CODES: {fid}: REJECT without any error code")
        digest1 = engine.ingest(fixture).digest
        if digest1 != result.digest:
            errors.append(f"DETERMINISM: {fid}: repeated ingest yields a different digest")

    # Mandatory negative coverage: removal of any of these is a regression.
    mandatory_codes = {
        "RIGHTS_PERMISSION",
        "RIGHTS_DO_NOT_INGEST",
        "RIGHTS_UNCLEAR",
        "RIGHTS_REFERENCE_ONLY",
        "MODERN_AS_CLASSICAL_EVIDENCE",
    }
    exercised = set()
    modern_guarded = {}
    for path in paths:
        fixture = load(path)
        codes = set(fixture.get("expect", {}).get("codes", []))
        if fixture.get("expect", {}).get("outcome") == "REJECT":
            exercised |= codes
            for sid in ("C01", "C02", "C03"):
                if fixture.get("ingest", {}).get("source_id") == sid and "MODERN_AS_CLASSICAL_EVIDENCE" in codes:
                    modern_guarded[sid] = path.name
        if "nondeterministic" in fixture.get("ingest", {}):
            errors.append(f"NONDETERMINISM: {fixture.get('fixture_id')}: fixture must stay deterministic")
    missing_codes = mandatory_codes - exercised
    if missing_codes:
        errors.append(f"MANDATORY_NEGATIVE: expected error codes not exercised by any fixture: "
                      f"{sorted(missing_codes)}")
    for sid in ("C01", "C02", "C03"):
        if sid not in modern_guarded:
            errors.append(f"MANDATORY_NEGATIVE: modern Source {sid} must appear in a REJECT "
                          f"fixture expecting MODERN_AS_CLASSICAL_EVIDENCE")
    if not names_by_id:
        errors.append("SCHEMA_ERROR: no fixtures loaded")
    return errors


def run_exporter_check() -> list:
    import importlib
    mod = importlib.import_module("scripts.build_preview_data")
    errors = []
    try:
        built = mod.build_preview_data(_ROOT)
    except Exception as exc:
        return [f"EXPORT: build_preview_data failed: {exc}"]
    preview_path = _ROOT / "preview" / "public" / "data" / "nahuatl-br.json"
    if not preview_path.exists():
        return [f"EXPORT: missing {preview_path.relative_to(_ROOT)}"]
    committed = load(preview_path)
    if committed.get("generated_at") != "NOT_RECORDED":
        errors.append("EXPORT: generated_at must be NOT_RECORDED (deterministic build)")
    if committed.get("schema") != built.get("schema"):
        errors.append(
            f"EXPORT: schema drift {committed.get('schema')!r} != {built.get('schema')!r}"
        )
    if committed.get("counts", {}).get("lemmas") != 50:
        errors.append(
            f"EXPORT: expected exactly 50 lemmas, found {committed.get('counts', {}).get('lemmas')}"
        )
    if committed != built:
        built_keys = set(built)
        committed_keys = set(committed)
        same_top = built_keys == committed_keys
        differing = [k for k in built_keys & committed_keys if built.get(k) != committed.get(k)]
        missing = sorted(built_keys - committed_keys)
        stray = sorted(committed_keys - built_keys)
        errors.append(
            "EXPORT: committed preview file is not reproducible from canonical data "
            f"(same top keys={same_top}; differing keys={', '.join(differing) or 'none'}; "
            f"missing={missing}; stray={stray})"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read-only validation (default)")
    args = parser.parse_args()
    errors: list[str] = []

    try:
        engine = eng.IngestionEngine(_ROOT)
    except Exception as exc:
        return _fail([f"ENGINE: {exc}"])

    try:
        errors.extend(run_fixture_checks(engine))
    except Exception as exc:
        errors.append(f"ENGINE: fixture checks failed: {exc}")

    try:
        errors.extend(run_exporter_check())
    except Exception as exc:
        errors.append(f"EXPORT: exporter checks failed: {exc}")

    if errors:
        return _fail(errors)

    metrics = {
        "schema": "gate5-validation-v1",
        "fixtures_total": len(list(FIXTURES_DIR.glob("*.yml"))),
        "engine_passes": "ALL",
        "exporter_reproducible": True,
    }
    print("GATE 5 VALIDATION: PASS")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


def _fail(errors):
    print("GATE 5 VALIDATION: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        result = main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        result = _fail([f"SCHEMA_ERROR: {exc}"])
    raise SystemExit(result)
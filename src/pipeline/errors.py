"""Stable Gate 5 pipeline error codes and the stage name vocabulary.

Consumers (validator, fixtures, tests) reference these constants; no code
depends on the presence of a particular language name in any registry value.
"""

from __future__ import annotations

STAGES = (
    "SOURCE_RESOLUTION",
    "RIGHTS_GATE",
    "VARIETY_GATE",
    "BASELINE_GUARD",
    "NORMALIZATION",
    "CLAIM_BUILD",
    "FINAL_ASSEMBLY",
)

# Stage prefix -> suffix mapping documented in docs/15 and docs/16.
CODES = {
    "SOURCE_REFERENCE": "source id not registered in data/source_registry/",
    "SOURCE_COMPONENT": "component not registered for the given Source",
    "UNKNOWN_INGESTION_CLASS": "no declared ingestion class (fails closed)",
    "RIGHTS_PERMISSION": "ingestion blocked: MANUAL_PERMISSION_REQUIRED",
    "RIGHTS_UNCLEAR": "ingestion blocked: RIGHTS_UNCLEAR",
    "RIGHTS_DO_NOT_INGEST": "ingestion blocked: DO_NOT_INGEST",
    "RIGHTS_REFERENCE_ONLY": "ingestion blocked: CAN_REFERENCE admits REFERENCE_ONLY use",
    "MODERN_AS_CLASSICAL_EVIDENCE": "modern-variety Source cannot back a Classical lemma",
    "UNSUPPORTED_VARIETY": "lemma variety outside the current ingestion scope",
    "LOCATOR_REQUIRED": "missing Locator without a declared locator_absence_reason",
    "LOCATOR_JUSTIFICATION": "Locator marked UNKNOWN without justification",
    "SOURCE_FORM_MUTATION": "captured SOURCE_FORM differs from the Gate 3 baseline",
    "UNKNOWN_SOURCE_FORM_ID": "source_form_id unknown for a baseline lemma",
    "DUPLICATE_ENTRY": "same lemma + source + source_form captured twice",
    "UNKNOWN_NORMALIZATION_RULE": "rule_id not defined in the approved policy",
    "RULE_CONDITION_UNSATISFIED": "policy rule requires a condition the dry-run cannot meet",
    "LOSSY_UNDECLARED": "lossy transformation without a declared lossy acknowledgment",
    "LOSSY_MISDECLARED": "declared lossiness disagrees with the policy rule",
    "UNSUPPORTED_FORM": "requested derived layer not supported by the pipeline",
    "PHONOLOGY_AUTOGENERATION": "automatic phonological/IPA generation is prohibited",
    "AUTO_SHORT_INFERENCE": "SHORT inferred without token Evidence (absence is not SHORT)",
    "SALTILLO_EVIDENCE_REQUIRED": "marked saltillo value without Evidence",
    "ILLEGAL_EDITORIAL_STATE": "requested Claim state must be DRAFT for pipeline origin",
    "CLAIM_EVIDENCE_REQUIRED": "Claim without a resolvable Evidence reference",
    "UNRESOLVED_EVIDENCE": "Claim references an Evidence id not generated or supplied",
    "CLAIM_POLICY": "predicate or Claim shape violates the approved policy",
    "CONTEXT_ORIGIN": "Claim/Evidence origin not declared as PIPELINE",
    "DIRECT_WITNESS_INSPECTION": "DIRECT_WITNESS mediation requires an inspected historical Witness",
    "AGGREGATOR_MEDIATION": "AGGREGATOR mediation requires a mediator Source id",
    "NON_DETERMINISTIC_INPUT": "input requests nondeterministic behavior; rejected",
    "SCHEMA_ERROR": "request failed structural validation",
}


def describe(code: str) -> str:
    return CODES.get(code, "unknown code")
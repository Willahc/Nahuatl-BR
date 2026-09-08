"""Pipeline domain vocabulary and small typed containers.

Values are plain JSON-compatible dicts plus a JSON string for hashing, so the
engine's output is trivially serializable and deterministic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

ABSENCE = {"UNKNOWN", "NOT_REVIEWED", "NOT_RECORDED", "NOT_APPLICABLE", "NOT_ATTESTED"}

MODALITIES = {"OBSERVED", "REPORTED", "INFERRED", "RECONSTRUCTED", "EDITORIAL"}
CONFIDENCES = {"UNASSESSED", "LOW", "MEDIUM", "HIGH"}
EDITORIAL_STATES = {"DRAFT", "IN_REVIEW", "APPROVED", "PUBLISHED", "QUARANTINED", "REJECTED", "DEPRECATED"}
LAYERS = {"SOURCE_FORM", "DIPLOMATIC_FORM", "NORMALIZED_FORM", "PEDAGOGICAL_FORM", "SEARCH_KEY", "PHONOLOGICAL_REPRESENTATION"}
DERIVED_LAYERS = {"DIPLOMATIC_FORM", "NORMALIZED_FORM", "PEDAGOGICAL_FORM", "SEARCH_KEY"}
MEDIATION_LEVELS = {"DIRECT_WITNESS", "HISTORICAL_EDITION", "MODERN_EDITION", "AGGREGATOR"}
INGESTION_CLASSES = {
    "CAN_INGEST", "CAN_INGEST_WITH_ATTRIBUTION", "CAN_REFERENCE",
    "MANUAL_PERMISSION_REQUIRED", "RIGHTS_UNCLEAR", "DO_NOT_INGEST",
}
EVIDENCE_ROLES = {"DIRECT_CLASSICAL_EVIDENCE", "REPORTED_CLASSICAL_EVIDENCE", "SECONDARY_EVIDENCE", "MODERN_VARIETY_COMPARATIVE"}
CLAIM_PREDICATES = {"has_historical_gloss", "has_pt_br_editorial_gloss", "has_reported_prosodic_notation"}
SOURCE_USES = {"EVIDENCE_CAPTURE", "SEARCH_ONLY", "REFERENCE_ONLY"}
VOWEL_LENGTH_STATES = {"SHORT", "LONG", "UNKNOWN", "NOT_APPLICABLE", "NOT_REVIEWED"}
SALTILLO_STATES = {"PRESENT", "ABSENT", "UNKNOWN", "NOT_APPLICABLE", "NOT_REVIEWED", "NOT_ATTESTED"}

PIPELINE_VERSION = "1.0.0"
PIPELINE_ORIGIN = "PIPELINE"
PIPELINE_TOOL = "nahuatl-br-gate5-pipeline"
DIRECT_WITNESS_SOURCES = {"A01", "A02", "A03", "A04"}


@dataclass
class ErrorRecord:
    code: str
    stage: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "stage": self.stage, "detail": self.detail}


def stable_digest(*parts: Any) -> str:
    """Deterministic content digest for IDs and idempotence checks."""
    import hashlib

    payload = json.dumps(list(parts), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass
class IngestionResult:
    case_id: str
    outcome: str
    errors: list[ErrorRecord] = field(default_factory=list)
    artifacts: dict[str, Any] | None = None
    stages: list[str] = field(default_factory=list)
    digest: str = ""

    def error_codes(self) -> list[str]:
        return [error.code for error in self.errors]

    def to_json(self) -> str:
        return json.dumps(
            {
                "case_id": self.case_id,
                "outcome": self.outcome,
                "errors": [e.as_dict() for e in self.errors],
                "artifacts": self.artifacts,
                "stages": self.stages,
                "digest": self.digest,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
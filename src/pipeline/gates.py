"""Rights gate and Variety gate for Gate 5 ingestion.

Decisions use only structured metadata from data/source_registry/ (component
ingestion classes, linguistic scope and features). No code depends on a
specific variety name; C01, C02 and C03 are rejected because their registered
scope/features mark them modern (and their components lack usable ingestion
classes), which is checked by fixtures and by the validator's mandatory
negative coverage.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import INGESTION_CLASSES, SOURCE_USES
from .loader import SourceRegistry


@dataclass(frozen=True)
class GateVerdict:
    accepted: bool
    code: str | None = None
    detail: str = ""


class RightsGate:
    """Resolve component ingestion class and decide capture eligibility.

    - CAN_INGEST / CAN_INGEST_WITH_ATTRIBUTION: accepted for capture.
    - CAN_REFERENCE: accepted only for REFERENCE_ONLY use.
    - MANUAL_PERMISSION_REQUIRED / RIGHTS_UNCLEAR / DO_NOT_INGEST: blocked.
    - Unknown or missing class: fails closed (UNKNOWN_INGESTION_CLASS).
    """

    def __init__(self, registry: SourceRegistry):
        self.registry = registry

    def _resolve(self, source_id: str, component_id: str) -> str | None:
        entry = self.registry.get(source_id)
        if entry is None:
            return None
        declared = entry.get("ingestion_class")
        if isinstance(declared, str):
            return declared
        if isinstance(declared, dict):
            return declared.get(component_id)
        return None

    def evaluate(self, source_id: str, component_id: str, use: str) -> GateVerdict:
        if source_id not in self.registry:
            return GateVerdict(False, "SOURCE_REFERENCE", f"unregistered Source {source_id}")
        if use not in SOURCE_USES:
            return GateVerdict(False, "SCHEMA_ERROR", f"unknown Source use {use!r}")
        klass = self._resolve(source_id, component_id)
        if klass is None:
            return GateVerdict(
                False,
                "UNKNOWN_INGESTION_CLASS",
                f"no ingestion class for {source_id}/{component_id}",
            )
        if klass not in INGESTION_CLASSES:
            return GateVerdict(False, "UNKNOWN_INGESTION_CLASS", f"unknown class {klass!r}")
        if klass == "CAN_INGEST":
            return GateVerdict(True, None, "capture allowed")
        if klass == "CAN_INGEST_WITH_ATTRIBUTION":
            return GateVerdict(
                True,
                None,
                "capture allowed with attribution (001: instrumentation requires attribution fields)",
            )
        if klass == "CAN_REFERENCE":
            if use == "REFERENCE_ONLY":
                return GateVerdict(True, None, "reference/attribution use allowed")
            return GateVerdict(
                False,
                "RIGHTS_REFERENCE_ONLY",
                "CAN_REFERENCE does not admit lexical capture",
            )
        return GateVerdict(
            False,
            {
                "MANUAL_PERMISSION_REQUIRED": "RIGHTS_PERMISSION",
                "RIGHTS_UNCLEAR": "RIGHTS_UNCLEAR",
                "DO_NOT_INGEST": "RIGHTS_DO_NOT_INGEST",
            }[klass],
            f"ingestion blocked by component class {klass}",
        )


def is_modern_source(entry: dict) -> bool:
    """Modern determination from registered metadata (never from a name string)."""
    features = entry.get("linguistic_features", {}) or {}
    if features.get("modern_variety") is True:
        return True
    scope = entry.get("linguistic_scope", {}) or {}
    variety = (scope.get("variety") or "").casefold()
    period = (scope.get("period") or "").casefold()
    if "modern" in variety:
        return True
    if period in {"modern", "modern_recording"}:
        return True
    return False


class VarietyGate:
    """Keep Modern Variety evidence out of a Classical Nahuatl lemma record."""

    SUPPORTED_LEMMA_VARIETY = "Classical Nahuatl"

    def evaluate(self, lemma_variety: str, source_id: str, entry: dict | None) -> GateVerdict:
        if lemma_variety != self.SUPPORTED_LEMMA_VARIETY:
            return GateVerdict(
                False,
                "UNSUPPORTED_VARIETY",
                f"ingestion scope covers {self.SUPPORTED_LEMMA_VARIETY} only",
            )
        if entry is None:
            return GateVerdict(False, "SOURCE_REFERENCE", f"unregistered Source {source_id}")
        if is_modern_source(entry):
            return GateVerdict(
                False,
                "MODERN_AS_CLASSICAL_EVIDENCE",
                "modern-variety Source cannot back a Classical lemma record",
            )
        return GateVerdict(True, None, "variety compatible")
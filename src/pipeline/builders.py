"""Deterministic builders for DRAFT Claim/Evidence/Attestation candidates.

All pipeline-generated candidates carry:

- editorial_state DRAFT and origin PIPELINE (rule 11 in AGENTS.md: IA/tool
  suggestions never constitute primary linguistic evidence);
- a provenance block recording actor, tool, action, from/to state and that no
  human review occurred;
- stable content-derived IDs, so identical inputs yield identical artifacts.

No candidate is ever auto-promoted to IN_REVIEW/APPROVED/PUBLISHED.
"""

from __future__ import annotations

import json
from typing import Any

from .models import (
    CONFIDENCES,
    DIRECT_WITNESS_SOURCES,
    EVIDENCE_ROLES,
    MODALITIES,
    PIPELINE_ORIGIN,
    PIPELINE_TOOL,
    PIPELINE_VERSION,
    stable_digest,
)

PROVENANCE_TEMPLATE = {
    "actor_role": "EXECUTION_AGENT",
    "actor_id": PIPELINE_TOOL,
    "tool": PIPELINE_TOOL,
    "tool_version": PIPELINE_VERSION,
    "timestamp": "NOT_RECORDED",
    "action": "GATE5_PIPELINE_GENERATION",
    "from_state": "NOT_APPLICABLE",
    "to_state": "DRAFT",
    "created_in_commit": "NOT_COMMITTED",
    "history_status": "GATE5_DRY_RUN",
    "review_status": "NOT_REVIEWED",
    "notes": "Automated pipeline candidate: origin PIPELINE; never primary linguistic evidence; human review required before adoption.",
}


def _provenance() -> dict[str, str]:
    return dict(PROVENANCE_TEMPLATE)


def digest_short(*parts: Any) -> str:
    return stable_digest(*parts)[:12]


def build_evidence_id(lemma_id: str, source_id: str, source_form: str) -> str:
    return "PEV-" + digest_short("evidence", lemma_id, source_id, source_form)


def build_attestation_id(lemma_id: str, source_id: str, source_form: str) -> str:
    return "PAT-" + digest_short("attestation", lemma_id, source_id, source_form)


def build_claim_id(predicate: str, lemma_id: str, value: str) -> str:
    return "PCL-" + digest_short("claim", predicate, lemma_id, value)


def evidence_role_for(mediation: str, source_id: str, inspected: bool) -> str:
    if mediation == "DIRECT_WITNESS" and source_id in DIRECT_WITNESS_SOURCES and inspected:
        return "DIRECT_CLASSICAL_EVIDENCE"
    return "REPORTED_CLASSICAL_EVIDENCE"


def build_evidence(
    lemma_id: str,
    source_ref: dict[str, Any],
    attestation_id: str,
    mediation: str,
    inspected: bool,
) -> dict[str, Any]:
    source_form = source_ref["source_form"]
    role = evidence_role_for(mediation, source_ref["source_id"], inspected)
    record = {
        "evidence_id": build_evidence_id(lemma_id, source_ref["source_id"], source_form),
        "type": "LEXICAL_ENTRY_REFERENCE",
        "source": source_ref["source_id"],
        "locator": source_ref.get("locator", "UNKNOWN"),
        "url": source_ref.get("url", "NOT_RECORDED"),
        "accessed_at": source_ref.get("accessed_at", "NOT_RECORDED"),
        "attestation_id": attestation_id,
        "evidence_role": role,
        "mediation_level": mediation,
        "direct_witness_inspected": inspected,
        "origin": PIPELINE_ORIGIN,
        "editorial_state": "DRAFT",
        "editorial_provenance": _provenance(),
    }
    if source_ref.get("aggregator"):
        record["aggregator"] = source_ref["aggregator"]
        record["mediator_note"] = "aggregator used for discovery and point reference only"
    return record


def build_attestation(
    lemma_id: str,
    source_ref: dict[str, Any],
    registry_name: str,
) -> dict[str, Any]:
    source_form = source_ref["source_form"]
    record = {
        "attestation_id": build_attestation_id(lemma_id, source_ref["source_id"], source_form),
        "source": source_ref["source_id"],
        "work": registry_name,
        "edition": source_ref.get("edition", "representative component of the registered Work"),
        "witness": source_ref.get("witness", "registry digital surrogate; exemplar NOT_REVIEWED"),
        "locator": source_ref.get("locator", "UNKNOWN"),
        "locator_absence_reason": source_ref.get("locator_absence_reason", "NOT_APPLICABLE"),
        "source_form": source_form,
        "original_gloss": source_ref.get("original_gloss", "UNKNOWN"),
        "url": source_ref.get("url", "NOT_RECORDED"),
        "mediation_level": source_ref.get("mediation_level", "HISTORICAL_EDITION"),
        "direct_witness_inspected": bool(source_ref.get("direct_witness_inspected")),
        "origin": PIPELINE_ORIGIN,
        "editorial_state": "DRAFT",
    }
    if source_ref.get("aggregator"):
        record["aggregator"] = source_ref["aggregator"]
    if source_ref.get("underlying_locator"):
        record["underlying_locator"] = source_ref["underlying_locator"]
    return record


def build_claim(
    predicate: str,
    lemma_id: str,
    value: str,
    modality: str,
    confidence: str,
    evidence_ids: list[str],
) -> dict[str, Any]:
    if predicate not in {
        "has_historical_gloss",
        "has_pt_br_editorial_gloss",
        "has_reported_prosodic_notation",
    }:
        raise ValueError(f"CLAIM_POLICY: predicate {predicate} not approved")
    if modality not in MODALITIES:
        raise ValueError(f"CLAIM_POLICY: modality {modality}")
    if confidence not in CONFIDENCES:
        raise ValueError(f"CLAIM_POLICY: confidence {confidence}")
    state = "DRAFT"
    record = {
        "claim_id": build_claim_id(predicate, lemma_id, value),
        "subject": lemma_id,
        "predicate": predicate,
        "value": json.dumps(value, ensure_ascii=False),
        "modality": modality,
        "confidence": confidence,
        "editorial_state": state,
        "origin": PIPELINE_ORIGIN,
        "claim_source_origin": PIPELINE_ORIGIN,
        "evidence": list(evidence_ids),
        "editorial_provenance": _provenance(),
    }
    return record
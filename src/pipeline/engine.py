"""Gate 5 ingestion engine (deterministic, dry-run by default).

The engine applies the stages in a fixed order. Results are deterministic: the
same request plus the same policy versions and source registry produces the
same JSON artifact digest. The engine writes nothing; callers decide whether a
future canonical writer may persist output.
"""

from __future__ import annotations

from typing import Any

from .models import ErrorRecord, IngestionResult, MEDIATION_LEVELS, PIPELINE_ORIGIN, stable_digest
from .loader import SourceRegistry, load_gate3_baseline, load_policy_orthography, load_source_registry
from .gates import RightsGate, VarietyGate
from .normalize import DerivationError, DerivationRecord, OrthographyNormalizer, REVIEW_GATED_RULES
from .builders import build_attestation, build_claim, build_evidence, digest_short

STAGE_ORDER = (
    "SOURCE_RESOLUTION",
    "RIGHTS_GATE",
    "VARIETY_GATE",
    "BASELINE_GUARD",
    "NORMALIZATION",
    "CLAIM_BUILD",
    "FINAL_ASSEMBLY",
)

DEFAULT_FORMS = ("DIPLOMATIC_FORM", "NORMALIZED_FORM", "PEDAGOGICAL_FORM", "SEARCH_KEY")
PHONOLOGY_LAYER_KEYS = {
    "PHONOLOGICAL_REPRESENTATION",
    "PHONETIC_REPRESENTATION",
    "PHONEMIC_PRONUNCIATION",
    "PHONETIC_PRONUNCIATION",
}
PREDICATE_RELATION = {
    "has_historical_gloss": "SUPPORTS",
    "has_pt_br_editorial_gloss": "DERIVED_FROM",
    "has_reported_prosodic_notation": "SUPPORTS",
}
ABSENT_VALUES = {"UNKNOWN", "NOT_REVIEWED", "NOT_ATTESTED", "NOT_RECORDED", "NOT_APPLICABLE"}

REQUIRED_INGEST = {"lemma_variety", "lemma_id", "source_id", "component_id", "use", "entries"}


class IngestionEngine:
    def __init__(
        self,
        root=None,
        registry: SourceRegistry | None = None,
        orthography_policy: dict[str, Any] | None = None,
        baseline: dict[str, Any] | None = None,
    ):
        from pathlib import Path

        path = Path(root) if root is not None else None
        self.registry = registry if registry is not None else load_source_registry(path)
        self.orthography = (
            orthography_policy if orthography_policy is not None else load_policy_orthography(path)
        )
        self.baseline = baseline if baseline is not None else load_gate3_baseline(path)
        self.rights = RightsGate(self.registry)
        self.variety = VarietyGate()
        self.normalizer = OrthographyNormalizer(self.orthography)

    # ------------------------------------------------------------------ utils
    def _add(self, result: IngestionResult, stage: str, code: str, detail: str) -> None:
        result.errors.append(ErrorRecord(code, stage, detail))

    def _record_layer(self, lemma_id: str, source_form_id: str, source_form: str,
                      layer: str, declared_lossy: bool) -> dict[str, Any] | ErrorRecord:
        derivation = self.normalizer.transform(source_form, layer, declared_lossy)
        if isinstance(derivation, DerivationError):
            return ErrorRecord(derivation.code, "NORMALIZATION", derivation.detail)
        base = source_form_id or lemma_id
        return {
            "form_id": f"{base}-{layer_dict[layer]}-{digest_short(layer, source_form)}",
            "layer": layer,
            "value": derivation.result,
            "normalization_profile": derivation.profile,
            "origin": PIPELINE_ORIGIN,
            "derivation_steps": derivation.steps,
            "lossy": derivation.lossy,
        }

    # ----------------------------------------------------------------- ingest
    def ingest(self, request: dict[str, Any]) -> IngestionResult:
        case_id = str(request.get("case_id") or "anonymous")
        ingest = request.get("ingest")
        if isinstance(ingest, dict):
            result = self._run(case_id, ingest)
        else:
            result = IngestionResult(case_id=case_id, outcome="REJECT")
            self._add(result, "SOURCE_RESOLUTION", "SCHEMA_ERROR", "missing ingest block")
        result.digest = stable_digest(result.to_json())
        return result

    def _run(self, case_id: str, ingest: dict[str, Any]) -> IngestionResult:
        result = IngestionResult(case_id=case_id, outcome="ACCEPT")
        result.stages = list(STAGE_ORDER)
        errors = result.errors

        missing = [key for key in REQUIRED_INGEST if key not in ingest]
        if missing:
            self._add(result, "SOURCE_RESOLUTION", "SCHEMA_ERROR", f"missing ingest fields {missing}")
            result.outcome = "REJECT"
            return result
        if ingest.get("nondeterministic") is True:
            self._add(result, "SOURCE_RESOLUTION", "NON_DETERMINISTIC_INPUT",
                      "input requests nondeterministic behavior")

        lemma_variety = ingest["lemma_variety"]
        lemma_id = ingest["lemma_id"]
        source_id = ingest["source_id"]
        component_id = ingest["component_id"]
        use = ingest["use"]
        entries = ingest["entries"]
        capture = use == "EVIDENCE_CAPTURE"
        requested_forms = ingest.get("requested_forms") if capture else []
        if requested_forms is None:
            requested_forms = list(DEFAULT_FORMS)
        declared_lossy = bool(ingest.get("declared_lossy"))

        for layer in requested_forms:
            if layer == "SOURCE_FORM":
                continue
            if layer in PHONOLOGY_LAYER_KEYS:
                self._add(result, "NORMALIZATION", "PHONOLOGY_AUTOGENERATION",
                          f"automatic generation of {layer} is prohibited")
            elif layer not in {"DIPLOMATIC_FORM", "NORMALIZED_FORM", "PEDAGOGICAL_FORM", "SEARCH_KEY"}:
                self._add(result, "NORMALIZATION", "UNSUPPORTED_FORM", f"unsupported layer {layer!r}")

        # --- SOURCE_RESOLUTION ---------------------------------------------
        entry_meta = self.registry.get(source_id)
        if entry_meta is None:
            self._add(result, "SOURCE_RESOLUTION", "SOURCE_REFERENCE", f"unknown Source {source_id}")
        mediator = ingest.get("mediator")
        if mediator is not None and mediator not in self.registry:
            self._add(result, "SOURCE_RESOLUTION", "SOURCE_REFERENCE", f"unknown aggregator {mediator}")
        mediation = ingest.get("mediation_level", "HISTORICAL_EDITION")
        if mediation not in MEDIATION_LEVELS:
            self._add(result, "SOURCE_RESOLUTION", "SCHEMA_ERROR",
                      f"invalid mediation_level {mediation!r}")
        if mediation == "AGGREGATOR" and not (mediator and str(mediator).strip()):
            self._add(result, "SOURCE_RESOLUTION", "AGGREGATOR_MEDIATION",
                      "AGGREGATOR mediation requires a mediator Source id")
        inspected = bool(ingest.get("direct_witness_inspected"))
        if mediation == "DIRECT_WITNESS" and (source_id not in {"A01", "A02", "A03", "A04"} or not inspected):
            self._add(result, "SOURCE_RESOLUTION", "DIRECT_WITNESS_INSPECTION",
                      "DIRECT_WITNESS requires an inspected historical Witness")
        locator = ingest.get("locator")
        locator_absence_reason = ingest.get("locator_absence_reason")
        if not (locator and str(locator).strip()) and not (locator_absence_reason and str(locator_absence_reason).strip()):
            self._add(result, "SOURCE_RESOLUTION", "LOCATOR_REQUIRED",
                      "missing Locator without locator_absence_reason")

        # --- RIGHTS_GATE and VARIETY_GATE ----------------------------------
        if entry_meta is not None:
            verdict = self.rights.evaluate(source_id, component_id, use)
            if not verdict.accepted:
                self._add(result, "RIGHTS_GATE", verdict.code, verdict.detail)
            verdict = self.variety.evaluate(lemma_variety, source_id, entry_meta)
            if not verdict.accepted:
                self._add(result, "VARIETY_GATE", verdict.code, verdict.detail)

        # --- BASELINE_GUARD (SOURCE_FORM immutability) ----------------------
        base = self.baseline.get("lemmas", {}).get(lemma_id)
        seen_forms: set[str] = set()
        for entry in entries:
            source_form = entry.get("source_form", "")
            source_form_id = entry.get("source_form_id") or ""
            if source_form in seen_forms:
                self._add(result, "BASELINE_GUARD", "DUPLICATE_ENTRY",
                          f"duplicate capture of {source_form!r}")
            seen_forms.add(source_form)
            if base is None or not source_form_id:
                continue
            canonical = base.get("source_forms", {}).get(source_form_id)
            if canonical is None:
                self._add(result, "BASELINE_GUARD", "UNKNOWN_SOURCE_FORM_ID",
                          f"unknown source_form_id {source_form_id}")
            elif canonical != source_form:
                self._add(result, "BASELINE_GUARD", "SOURCE_FORM_MUTATION",
                          f"source_form {source_form!r} differs from baseline {canonical!r}")

        # --- NORMALIZATION --------------------------------------------------
        artifact_forms: list[dict[str, Any]] = []
        artifact_search_keys: list[dict[str, Any]] = []
        executed_rules: dict[str, list[str]] = {}
        for entry in entries if capture else []:
            source_form = entry.get("source_form", "")
            source_form_id = entry.get("source_form_id") or ""
            for layer in ("DIPLOMATIC_FORM", "NORMALIZED_FORM"):
                if layer not in requested_forms:
                    continue
                recorded = self._record_layer(lemma_id, source_form_id, source_form, layer, declared_lossy)
                if isinstance(recorded, ErrorRecord):
                    errors.append(recorded)
                else:
                    artifact_forms.append(recorded)
                    executed_rules.setdefault(layer, []).extend(
                        step["rule_id"] for step in recorded["derivation_steps"])
            if "PEDAGOGICAL_FORM" in requested_forms:
                pedagogic = ingest.get("pedagogical", {}) or {}
                artifact_forms.append({
                    "form_id": f"{source_form_id or lemma_id}-FP-{digest_short('fp', source_form)}",
                    "layer": "PEDAGOGICAL_FORM",
                    "value": pedagogic.get("value", "UNKNOWN"),
                    "normalization_profile": self.normalizer.profile,
                    "origin": PIPELINE_ORIGIN,
                    "evidence": pedagogic.get("evidence", []),
                    "note": "editorial pedagogical value; macron or h requires independent Evidence",
                })
            if "SEARCH_KEY" in requested_forms:
                derivation = self.normalizer.transform(source_form, "SEARCH_KEY", declared_lossy)
                if isinstance(derivation, DerivationError):
                    errors.append(ErrorRecord(derivation.code, "NORMALIZATION", derivation.detail))
                else:
                    alias_notes = []
                    alias = ingest.get("saltillo_alias") or {}
                    if alias.get("evidence_id"):
                        alias_derivation = self.normalizer.transform(
                            source_form, "SEARCH_KEY", declared_lossy, alias=True)
                        if isinstance(alias_derivation, DerivationError):
                            errors.append(ErrorRecord(alias_derivation.code, "NORMALIZATION", alias_derivation.detail))
                        else:
                            alias_notes.append(
                                f"{alias_derivation.result} (fold_saltillo alias via search-saltillo-001)")
                    artifact_search_keys.append({
                        "form_id": f"{source_form_id or lemma_id}-SK-{digest_short('sk', source_form)}",
                        "layer": "SEARCH_KEY",
                        "value": derivation.result,
                        "normalization_profile": derivation.profile,
                        "origin": PIPELINE_ORIGIN,
                        "search_keys": [derivation.result],
                        "aliases": alias_notes,
                        "steps": derivation.steps,
                        "lossy": derivation.lossy,
                    })
                    executed_rules.setdefault("SEARCH_KEY", []).extend(
                        step["rule_id"] for step in derivation.steps)
                for layer in ("DIPLOMATIC_FORM", "NORMALIZED_FORM", "SEARCH_KEY"):
                    executed_rules[layer] = list(dict.fromkeys(executed_rules.get(layer, [])))

        # transform_spec audit
        for spec in ingest.get("transform_spec", []) or []:
            rule_id = spec.get("rule_id")
            target_layer = spec.get("layer")
            if rule_id not in self.normalizer.rules:
                self._add(result, "NORMALIZATION", "UNKNOWN_NORMALIZATION_RULE",
                          f"transform_spec rule {rule_id!r} not defined in policy")
            elif rule_id in REVIEW_GATED_RULES:
                self._add(result, "NORMALIZATION", "RULE_CONDITION_UNSATISFIED",
                          f"transform_spec rule {rule_id!r} requires source-specific review")
            elif rule_id not in executed_rules.get(target_layer, []):
                self._add(result, "NORMALIZATION", "SCHEMA_ERROR",
                          f"transform_spec rule {rule_id!r} was not executed for {target_layer}")

        # --- CLAIM_BUILD ----------------------------------------------------
        claims_out: list[dict[str, Any]] = []
        evidence_out: list[dict[str, Any]] = []
        attestations_out: list[dict[str, Any]] = []
        links_out: list[dict[str, Any]] = []
        generated_evidence_ids: set[str] = set()
        known_evidence_ids: set[str] = set(ingest.get("known_evidence") or [])

        for entry in entries if capture else []:
            source_form = entry.get("source_form", "")
            source_ref = {
                "source_id": source_id,
                "source_form": source_form,
                "locator": locator or "UNKNOWN",
                "url": ingest.get("url", "NOT_RECORDED"),
                "accessed_at": ingest.get("accessed_at", "NOT_RECORDED"),
                "original_gloss": entry.get("original_gloss", "UNKNOWN"),
                "edition": ingest.get("edition"),
                "witness": ingest.get("witness"),
                "mediation_level": mediation,
                "direct_witness_inspected": inspected,
            }
            if mediator:
                source_ref["aggregator"] = mediator
            if locator_absence_reason:
                source_ref["locator_absence_reason"] = locator_absence_reason
            if ingest.get("underlying_locator"):
                source_ref["underlying_locator"] = ingest["underlying_locator"]
            attestation = build_attestation(
                lemma_id, source_ref,
                str(entry_meta.get("name", "")) if entry_meta else source_id)
            attestations_out.append(attestation)
            evidence = build_evidence(
                lemma_id, source_ref, attestation["attestation_id"], mediation, inspected)
            evidence_out.append(evidence)
            generated_evidence_ids.add(evidence["evidence_id"])

        claim_requests = ingest.get("claims")
        if claim_requests is None:
            claim_requests = [
                {
                    "predicate": "has_historical_gloss",
                    "value": entry.get("original_gloss", "UNKNOWN"),
                    "modality": "REPORTED",
                    "confidence": "HIGH",
                }
                for entry in entries
                if entry.get("original_gloss") not in ABSENT_VALUES
            ]
        if isinstance(claim_requests, dict):
            claim_requests = [claim_requests]
        for claim_request in claim_requests:
            predicate = claim_request.get("predicate")
            value = claim_request.get("value", "")
            modality = claim_request.get("modality", "REPORTED")
            confidence = claim_request.get("confidence", "MEDIUM")
            if predicate not in PREDICATE_RELATION:
                self._add(result, "CLAIM_BUILD", "CLAIM_POLICY", f"predicate {predicate!r} not approved")
                continue
            if claim_request.get("requested_state", "DRAFT") != "DRAFT":
                self._add(result, "CLAIM_BUILD", "ILLEGAL_EDITORIAL_STATE",
                          "pipeline Claims must be DRAFT; auto-promotion is prohibited")
            if claim_request.get("origin", PIPELINE_ORIGIN) != PIPELINE_ORIGIN:
                self._add(result, "CLAIM_BUILD", "CONTEXT_ORIGIN",
                          "Claim origin must be PIPELINE")
            if "evidence" in claim_request and not claim_request["evidence"]:
                self._add(result, "CLAIM_BUILD", "CLAIM_EVIDENCE_REQUIRED",
                          f"{predicate} Claim declared without Evidence")
                continue
            claim_evidence = list(claim_request.get("evidence") or [])
            bad_refs = [ref for ref in claim_evidence
                        if ref not in generated_evidence_ids and ref not in known_evidence_ids]
            if bad_refs:
                self._add(result, "CLAIM_BUILD", "UNRESOLVED_EVIDENCE",
                          f"Claim references unknown Evidence {sorted(bad_refs)}")
            if not claim_evidence:
                claim_evidence = sorted(generated_evidence_ids)
            try:
                claim = build_claim(predicate, lemma_id, value, modality, confidence, claim_evidence)
            except ValueError as exc:
                self._add(result, "CLAIM_BUILD", "CLAIM_POLICY", str(exc))
                continue
            claims_out.append(claim)
            for ev_id in claim_evidence:
                links_out.append({
                    "claim_id": claim["claim_id"],
                    "evidence_id": ev_id,
                    "relation": PREDICATE_RELATION[predicate],
                })

        # --- phonology hints guard -------------------------------------------
        hints = ingest.get("phonology_hints") or {}
        vowel = hints.get("vowel_length") or {}
        saltillo = hints.get("saltillo") or {}
        if vowel.get("value") == "SHORT" and not vowel.get("evidence"):
            self._add(result, "CLAIM_BUILD", "AUTO_SHORT_INFERENCE",
                      "SHORT inferred without token Evidence (absence is not SHORT)")
        if vowel.get("value") == "LONG" and not vowel.get("evidence"):
            self._add(result, "CLAIM_BUILD", "SCHEMA_ERROR", "LONG requires Evidence")
        if saltillo.get("value") in {"PRESENT", "ABSENT"} and not saltillo.get("evidence"):
            self._add(result, "CLAIM_BUILD", "SALTILLO_EVIDENCE_REQUIRED",
                      "marked saltillo value without Evidence")
        for intrusive in ("phonetic_ipa", "phonemic_ipa", "pronunciation", "phonetic_pronunciation"):
            if intrusive in hints:
                self._add(result, "CLAIM_BUILD", "PHONOLOGY_AUTOGENERATION",
                          f"automatic {intrusive} generation is prohibited")

        result.outcome = "ACCEPT" if not errors else "REJECT"
        if result.outcome == "ACCEPT":
            result.artifacts = {
                "schema": "nahuatl-br-gate5-ingestion-v1",
                "pipeline_version": "1.0.0",
                "lemma": {
                    "id": lemma_id,
                    "variety": lemma_variety,
                },
                "source": {
                    "source_id": source_id,
                    "component_id": component_id,
                    "mediator": mediator,
                    "mediation_level": mediation,
                    "direct_witness_inspected": inspected,
                },
                "forms": artifact_forms,
                "search_keys": artifact_search_keys,
                "claims": claims_out,
                "evidence": evidence_out,
                "attestations": attestations_out,
                "evidence_links": links_out,
                "provenance": {
                    "created_by": "EXECUTION_AGENT",
                    "tool": "src/pipeline",
                    "pipeline_version": "1.0.0",
                    "mode": "DRY_RUN",
                    "registry_projection": "data/source_registry",
                    "orthography_profile": self.normalizer.profile,
                    "origin": PIPELINE_ORIGIN,
                },
            }
        return result


def run_fixture(engine: IngestionEngine, fixture: dict[str, Any]) -> IngestionResult:
    return engine.ingest(fixture)


layer_dict = {
    "DIPLOMATIC_FORM": "FD",
    "NORMALIZED_FORM": "FN",
}
"""Deterministic orthographic derivation under classical_orthography_v1.

Every transformation is executed only when the approved policy defines the
rule (normalization_rules.rule_id) and records its rule_id, input, output and
lossy flag. Rules that the policy gates behind source-specific review are never
auto-applied by the dry run; referencing them is rejected.

SEARCH_KEY is retrieval-only. search-diacritic-001 maps only the policy's
controlled macron vowels; all other marks remain intact. Historical source
forms are preserved, and key equality never establishes linguistic identity.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from typing import Any

ESTABLISHED_HYPHENS = frozenset(
    {"-", "\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2043", "\u2212"}
)
REVIEW_GATED_RULES = frozenset(
    {
        "rincon-cedilla-001",
        "rincon-initial-y-001",
        "rincon-semivowel-i-001",
        "rincon-semivowel-u-001",
        "rincon-qu-cu-001",
    }
)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _fold_diacritics(text: str) -> str:
    return text.translate(str.maketrans("āēīōĀĒĪŌ", "aeioAEIO"))


def _is_punctuation(char: str) -> bool:
    return unicodedata.category(char).startswith("P")


def _strip_peripheral_punctuation(text: str) -> str:
    start = 0
    end = len(text)
    while start < end and _is_punctuation(text[start]):
        start += 1
    while end > start and _is_punctuation(text[end - 1]):
        end -= 1
    return text[start:end]


def _remove_hyphens(text: str) -> str:
    return "".join(ch for ch in text if ch not in ESTABLISHED_HYPHENS)


def _remove_pedagogical_h(text: str) -> str:
    return text.replace("h", "")


RULE_IMPLEMENTATIONS = {
    "editorial-nfc-001": _nfc,
    "search-lower-001": lambda value: value.lower(),
    "search-diacritic-001": _fold_diacritics,
    "search-punct-001": _strip_peripheral_punctuation,
    "search-hyphen-001": _remove_hyphens,
    "search-saltillo-001": _remove_pedagogical_h,
}

LAYER_RULES = {
    "DIPLOMATIC_FORM": ("editorial-nfc-001",),
    "NORMALIZED_FORM": ("editorial-nfc-001",),
    "SEARCH_KEY": (
        "editorial-nfc-001",
        "search-lower-001",
        "search-diacritic-001",
        "search-punct-001",
        "search-hyphen-001",
    ),
    "SEARCH_KEY_SALTILLO_ALIAS": (
        "editorial-nfc-001",
        "search-lower-001",
        "search-diacritic-001",
        "search-punct-001",
        "search-hyphen-001",
        "search-saltillo-001",
    ),
}


@dataclass
class DerivationError:
    code: str
    detail: str


@dataclass
class DerivationRecord:
    layer: str
    profile: str
    steps: list[dict[str, Any]] = field(default_factory=list)
    result: str = ""
    lossy: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "profile": self.profile,
            "steps": self.steps,
            "result": self.result,
            "lossy": self.lossy,
        }


class OrthographyNormalizer:
    def __init__(self, policy: dict[str, Any]):
        self.policy = policy
        self.rules = policy["rules"]
        self.profile = (
            f"{policy['policy']['policy_id']}@{policy['policy']['version']}"
        )

    def _apply(self, rule_id: str, text: str) -> str | DerivationError:
        if rule_id not in self.rules:
            return DerivationError(
                "UNKNOWN_NORMALIZATION_RULE", f"rule {rule_id!r} not defined in approved policy"
            )
        if rule_id in REVIEW_GATED_RULES:
            return DerivationError(
                "RULE_CONDITION_UNSATISFIED",
                f"rule {rule_id!r} requires source-specific review the dry run cannot perform",
            )
        implementation = RULE_IMPLEMENTATIONS.get(rule_id)
        if implementation is None:
            return DerivationError(
                "RULE_CONDITION_UNSATISFIED",
                f"no automatic implementation authorized for rule {rule_id!r}",
            )
        return implementation(text)

    def transform(
        self,
        text: str,
        layer: str,
        declared_lossy: bool | None = None,
        alias: bool = False,
    ) -> DerivationRecord | DerivationError:
        target = "SEARCH_KEY_SALTILLO_ALIAS" if alias else layer
        sequence = LAYER_RULES.get(target)
        if sequence is None:
            return DerivationError("UNSUPPORTED_FORM", f"no derivation for layer {layer!r}")
        steps: list[dict[str, Any]] = []
        current = text
        any_lossy = False
        for rule_id in sequence:
            rule = self.rules.get(rule_id)
            outcome = self._apply(rule_id, current)
            if isinstance(outcome, DerivationError):
                return outcome
            policy_lossy = bool(rule and rule.get("lossy"))
            steps.append(
                {
                    "rule_id": rule_id,
                    "input": current,
                    "output": outcome,
                    "lossy": policy_lossy,
                    "policy_lossy": policy_lossy,
                }
            )
            any_lossy = any_lossy or policy_lossy
            current = outcome

        if layer in {"SEARCH_KEY", "SEARCH_KEY_SALTILLO_ALIAS"}:
            if declared_lossy is not True:
                return DerivationError(
                    "LOSSY_UNDECLARED",
                    f"{layer} is a lossy retrieval layer; declare lossy acknowledgment",
                )
        for step in steps:
            rule = self.rules.get(step["rule_id"])
            if rule is not None and bool(rule.get("lossy")) != step["policy_lossy"]:
                return DerivationError("LOSSY_MISDECLARED", f"policy lossy flag drift for {step['rule_id']}")
        return DerivationRecord(
            layer=layer,
            profile=self.profile,
            steps=[{k: v for k, v in step.items() if k != "policy_lossy"} for step in steps],
            result=current,
            lossy=any_lossy,
        )
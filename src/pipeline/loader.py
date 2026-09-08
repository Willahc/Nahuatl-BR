"""Projection loader for canonical Gate 5 inputs.

Uses the same fail-closed philosophy as scripts/gate3_integrity.py but is
self-contained and lives with the pipeline: it parses only the registry fields
the pipeline needs, treats unsupported syntax as an error, and never mixes the
registry projection with the JSON-compatible canonical records (pilot lemmas,
policies, phonology claims, fixtures, baseline).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT_DEFAULT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = "data/source_registry"

_QUOTED = re.compile(r'^"((?:[^"\\]|\\.)*)"$')


def _decode_scalar(text: str) -> Any:
    text = text.strip()
    if not text:
        raise ValueError("empty scalar")
    if text.startswith('"'):
        match = _QUOTED.match(text)
        if not match:
            raise ValueError("unterminated quoted scalar")
        value = json.loads(text)
        if not isinstance(value, str):
            raise ValueError("quoted scalar is not a string")
        return value
    if text in {"true", "false"}:
        return text == "true"
    if text == "null":
        return None
    if any(c in text for c in "{}[]#&*!|>'\"\n"):
        raise ValueError(f"unsupported YAML scalar {text!r}")
    return text


def _split_tokens(body: str) -> list[str]:
    tokens: list[str] = []
    depth = 0
    quote: str | None = None
    start = 0
    i = 0
    while i < len(body):
        char = body[i]
        if quote is not None:
            if char == "\\":
                i += 1
            elif char == quote:
                quote = None
        elif char in {'"', "'"}:
            quote = char
        elif char in "[{(":
            depth += 1
        elif char in "]})":
            depth -= 1
        elif char == "," and depth == 0:
            tokens.append(body[start:i])
            start = i + 1
        i += 1
    tokens.append(body[start:])
    return tokens


def _map_tokens(body: str) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for token in _split_tokens(body):
        stripped = token.strip()
        if not stripped:
            continue
        key_match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:(.*)$", stripped, re.S)
        if not key_match:
            raise ValueError(f"expected key: value token, got {stripped!r}")
        key, value = key_match.group(1), key_match.group(2).strip()
        if not value:
            raise ValueError(f"empty value for key {key}")
        parsed.append((key, value))
    return parsed


def _list_tokens(body: str) -> list[str]:
    items: list[str] = []
    for token in _split_tokens(body):
        stripped = token.strip()
        if stripped:
            items.append(stripped)
    return items


def flow_map(value: str) -> dict[str, Any]:
    value = value.strip()
    if not (value.startswith("{") and value.endswith("}")):
        raise ValueError("expected single-line flow map")
    result: dict[str, Any] = {}
    for key, raw in _map_tokens(value[1:-1]):
        if key in result:
            raise ValueError(f"duplicate flow-map field {key}")
        result[key] = _decode_value(raw)
    return result


def _decode_value(raw: str) -> Any:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [_decode_scalar(part) for part in _list_tokens(raw[1:-1])]
    if raw.startswith("{") and raw.endswith("}"):
        return flow_map(raw)
    return _decode_scalar(raw)


def field_text(text: str, name: str, indent: int = 0) -> str:
    matches = re.findall(r"^" + " " * indent + re.escape(name) + r":\s*(.+)$", text, re.M)
    if len(matches) != 1:
        raise ValueError(f"expected one {name} field")
    return matches[0].strip()


def ingestion_class_map(value: str) -> dict[str, str] | str:
    value = value.strip()
    if value.startswith("{"):
        parsed = flow_map(value)
        if not all(isinstance(v, str) for v in parsed.values()):
            raise ValueError("ingestion_class values must be strings")
        return {k: v for k, v in parsed.items()}  # type: ignore[return-value]
    return _decode_scalar(value)  # type: ignore[return-value]


def canonical_load(path: Path) -> dict[str, Any]:
    """Load JSON-compatible YAML/JSON canonical records (pilot, claims, fixtures)."""
    with path.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def _parse_block(lines: list[tuple[int, str]], idx: int, indent: int) -> Any:
    if idx >= len(lines):
        return {}, idx
    _, first = lines[idx]
    if first.startswith("-") and indent == lines[idx][0]:
        return _parse_seq(lines, idx, indent)
    return _parse_map(lines, idx, indent)


def _parse_map(lines: list[tuple[int, str]], idx: int, indent: int) -> Any:
    node: dict[str, Any] = {}
    while idx < len(lines):
        cur_indent, line = lines[idx]
        if cur_indent < indent:
            break
        if cur_indent != indent:
            raise ValueError(f"unexpected indentation at {line!r}")
        key, sep, rest = line.partition(":")
        if not sep or not key.strip():
            break
        key = key.strip()
        rest = rest.strip()
        if rest:
            node[key] = _decode_value(rest)
            idx += 1
        else:
            node[key], idx = _parse_block(lines, idx + 1, indent + 2)
    return node, idx


def _parse_seq(lines: list[tuple[int, str]], idx: int, indent: int) -> Any:
    seq: list[Any] = []
    while idx < len(lines):
        cur_indent, line = lines[idx]
        if cur_indent < indent:
            break
        if cur_indent != indent or not line.startswith("- "):
            raise ValueError(f"expected sequence item, got {line!r}")
        item = line[2:].strip()
        if not item:
            value, idx = _parse_block(lines, idx + 1, indent + 2)
            seq.append(value)
        elif item.startswith("{") and item.endswith("}"):
            seq.append(flow_map(item))
            idx += 1
        elif re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", item):
            key, _, rest = item.partition(":")
            rest = rest.strip()
            entry: dict[str, Any] = {}
            if rest:
                entry[key.strip()] = _decode_value(rest)
                idx += 1
            else:
                entry[key.strip()], idx = _parse_block(lines, idx + 1, indent + 2)
            seq.append(entry)
        else:
            seq.append(_decode_scalar(item))
            idx += 1
    return seq, idx


def load_yaml_lite(text: str) -> dict[str, Any]:
    """Subset parser for the flow-style YAML used by data/policies/*.

    Supports indentation maps, block/flow sequences and flow maps/lists
    (the style already used across source_registry and policies). It rejects
    unsupported constructs instead of guessing.
    """
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))
    node, _ = _parse_block(lines, 0, 0)
    if not isinstance(node, dict):
        raise ValueError("expected a top-level mapping")
    return node


class SourceRegistry:
    """Structured projection of data/source_registry plus inventory of IDs."""

    def __init__(self, entries: dict[str, dict[str, Any]], path: Path):
        self.entries = entries
        self.path = path

    def __contains__(self, source_id: str) -> bool:
        return source_id in self.entries

    def get(self, source_id: str) -> dict[str, Any] | None:
        return self.entries.get(source_id)

    def ingredients(self) -> list[str]:
        return sorted(self.entries)


def load_source_registry(root: Path = ROOT_DEFAULT) -> SourceRegistry:
    registry: dict[str, dict[str, Any]] = {}
    registry_dir = root / REGISTRY_DIR
    paths = sorted(registry_dir.glob("*.yml"))
    if not paths:
        raise ValueError("no source registry files found")
    for path in paths:
        text = path.read_text(encoding="utf-8-sig")
        source_id = str(_decode_scalar(field_text(text, "source_id")))
        if source_id in registry:
            raise ValueError(f"DUPLICATE_ID: Source {source_id}")
        scope = flow_map(field_text(text, "linguistic_scope"))
        for required in ("language", "variety", "period"):
            if not isinstance(scope.get(required), str) or not scope[required].strip():
                raise ValueError(f"SOURCE_SCOPE: incomplete scope for {source_id}")
        features: dict[str, Any] = {}
        if "linguistic_features" in text:
            features = flow_map(field_text(text, "linguistic_features"))
        entry: dict[str, Any] = {
            "source_id": source_id,
            "name": _decode_scalar(field_text(text, "name")),
            "linguistic_scope": scope,
            "linguistic_features": features,
        }
        if "ingestion_class" in text:
            entry["ingestion_class"] = ingestion_class_map(field_text(text, "ingestion_class"))
        for optional in ("url", "accessed_at", "institution", "rights_status", "recommended_role", "scholarly_relevance"):
            if re.search(rf"^{re.escape(optional)}:\s*(\S.*)$", text, re.M):
                entry[optional] = _decode_value(field_text(text, optional))
        registry[source_id] = entry
    return SourceRegistry(registry, registry_dir)


def load_policy_orthography(root: Path = ROOT_DEFAULT) -> dict[str, Any]:
    path = root / "data" / "policies" / "classical_orthography_v1.yml"
    policy = load_yaml_lite(path.read_text(encoding="utf-8-sig"))
    if policy.get("status") != "APPROVED":
        raise ValueError("NORMALIZATION_PROFILE: orthography profile not approved")
    rules = [
        rule for rule in policy.get("normalization_rules", [])
        if isinstance(rule, dict) and rule.get("rule_id")
    ]
    by_rule = {rule["rule_id"]: rule for rule in rules}
    if len(by_rule) != len(rules):
        raise ValueError("NORMALIZATION_PROFILE: duplicate rule_id in policy")
    return {"path": path, "policy": policy, "rules": by_rule}


def load_policy_phonology(root: Path = ROOT_DEFAULT) -> dict[str, Any]:
    path = root / "data" / "policies" / "classical_phonology_v1.yml"
    return canonical_load(path)


def load_gate3_baseline(root: Path = ROOT_DEFAULT) -> dict[str, Any]:
    return canonical_load(root / "data" / "phonology" / "gate3_baseline.yml")


def load_gate_status(root: Path = ROOT_DEFAULT) -> list[dict[str, str]]:
    text = (root / "docs" / "GATE_STATUS.md").read_text(encoding="utf-8-sig")
    rows = []
    for match in re.finditer(r"^Gate\s+(\d+)\s*:\s*(\S+)\s*/\s*(\S+)\s*$", text, re.M):
        rows.append({"gate": match.group(1), "status": match.group(2), "closure": match.group(3)})
    return rows
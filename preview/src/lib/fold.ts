import type { LemmaDto } from "./types";

// Query-only subset of classical_orthography_v1@1.0.0:
// editorial-nfc-001, search-lower-001, search-diacritic-001.
// Keys come from the exporter; the UI never derives linguistic SEARCH_KEYs.
export function fold(text: string): string {
  const macrons: Record<string, string> = { "ā": "a", "ē": "e", "ī": "i", "ō": "o" };
  return text.normalize("NFC").toLowerCase().replace(/[āēīō]/g, (v) => macrons[v]);
}

export function searchLemmas(lemmas: LemmaDto[], query: string): LemmaDto[] {
  const literal = query.trim().normalize("NFC").toLowerCase();
  if (!literal) return lemmas;
  const key = fold(query.trim());
  return lemmas.filter((lemma) => {
    if (lemma.forms.search_keys.some((value) => value.includes(key))) return true;
    // Literal representations preserve historical marks, including ö in L0050.
    // Editorial text uses case-insensitive literal matching, without accent folding.
    return [
      ...lemma.forms.source_forms,
      lemma.forms.normalized_form ?? "",
      lemma.forms.pedagogical_form ?? "",
      lemma.display_form ?? "",
      ...lemma.interpretations,
      ...lemma.pt_br_editorial,
      ...lemma.historical_glosses.flat(),
    ].some((value) => value.normalize("NFC").toLowerCase().includes(literal));
  });
}

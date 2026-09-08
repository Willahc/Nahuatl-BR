import type { LemmaDto, PreviewData } from "./types";
import { foldMatch } from "./fold";

let cache: PreviewData | null = null;

const dataUrl = `${import.meta.env.BASE_URL}data/nahuatl-br.json`;

export async function loadPreview(): Promise<PreviewData> {
  const response = await fetch(dataUrl);
  if (!response.ok) {
    throw new Error(`falha ao carregar ${dataUrl} (HTTP ${response.status})`);
  }
  cache = (await response.json()) as PreviewData;
  return cache;
}

export function previewCache(): PreviewData | null {
  return cache;
}

export function searchLemmas(lemmas: LemmaDto[], query: string): LemmaDto[] {
  const q = query.trim();
  if (!q) {
    return lemmas;
  }
  return lemmas.filter((lemma) => {
    const texts = [
      ...lemma.forms.source_forms,
      ...lemma.forms.search_keys,
      lemma.forms.normalized_form ?? "",
      lemma.forms.pedagogical_form ?? "",
      lemma.display_form ?? "",
      ...lemma.interpretations,
      ...lemma.pt_br_editorial,
      ...lemma.historical_glosses,
    ];
    return foldMatch(texts, q);
  });
}

export function lemmaById(lemmas: LemmaDto[], id: string): LemmaDto | undefined {
  const key = id.trim().toUpperCase();
  return lemmas.find((lemma) => lemma.id.toUpperCase() === key);
}
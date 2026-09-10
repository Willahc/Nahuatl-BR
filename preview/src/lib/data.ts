import type { LemmaDto, PreviewData } from "./types";
export { searchLemmas } from "./fold";

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

export function lemmaById(lemmas: LemmaDto[], id: string): LemmaDto | undefined {
  const key = id.trim().toUpperCase();
  return lemmas.find((lemma) => lemma.id.toUpperCase() === key);
}
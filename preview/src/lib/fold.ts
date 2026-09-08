export function fold(text: string): string {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

export function foldMatch(haystack: string[], query: string): boolean {
  const q = fold(query.trim());
  if (!q) return true;
  return haystack.some((value) => fold(value).includes(q));
}
# Gate 4 — Dossiê do Saltillo

## Questão

O que a notação colonial central reporta sobre o contraste glotal ("saltillo"),
sua realização e as convenções didáticas modernas — sem transformar hipótese em
fato e sem preencher lacunas lexicais.

## Claims envolvidos

- G4C005 (`SALTILLO_EXISTENCE`, REPORTED, HIGH): "A notação histórica reporta
  contraste glotal." Evidence: G4E002 (Carochi via GDN), G4E003 (Launey).
- G4C006 (`SALTILLO_REALIZATION`, RECONSTRUCTED, MEDIUM): `/ʔ/` é a reconstrução
  preferida para o recorte central aqui delimitado. Evidence: G4E006 (Canger) e
  G4E003; contra-evidência registrada: G4E006 (Canger, que se opõe a
  generalizar para todas as regiões coloniais).
- G4C007 (`SALTILLO_REALIZATION`, REPORTED, MEDIUM): Canger sustenta fricção
  glotal regional já colonial, contra origem global oclusiva. Evidence: G4E006.
  Karttunen 1983, Lockhart 2001 e Andrews 1975 são citados de segundo nível
  (via Canger); páginas integrais não inspecionadas.
- G4C008 (`GRAPHEME_PHONEME_CORRESPONDENCE`, EDITORIAL, HIGH): `h` pedagógico é
  convenção, não medição fonética. Evidence: G4E002.
- G4C009 (`SALTILLO_REALIZATION`, EDITORIAL, HIGH): a recomendação didática de
  `h` por Launey não fixa toda realização histórica. Evidence: G4E003, G4E006.

## Evidência

- `G4E001` (Rincón via GDN): quantidade em `chichi` por entrada distinta —
  relevante à separação de sentidos, não à realização do saltillo.
- `G4E002` (Carochi via GDN): notação de quantidade/saltillo, intervenção
  editorial e incerteza tipográfica (`nohuian`/`nohuiän`).
- `G4E003` (Launey, pp. 4–8): saltillo e acento/vocativo; `cochî` (saltillo
  final, plural) em G4F032.
- `G4E006` (Canger, pp. 244–245): "La h se cambia en saltillo"; hipótese
  regional do fechamento glotal e crítica à generalização pan-colonial.
- `G4E007` (Canger, pp. 246–247 e 251): plural com saltillo/reduplicação
  (`ko:-koyo-’`, G4F031).

Nenhuma Evidence atual usa `DIRECT_CLASSICAL_EVIDENCE`; todas declaram
`direct_witness_inspected: false`. O lock é `docs/12_GATE_4_PHONOLOGY_EVIDENCE_LOCK.md`.

## Posição do modelo

1. O contraste é **reportado** pela notação (G4C005), não atestado por medição.
2. A realização é **reconstruída** (`/ʔ/` central, MEDIUM) e objeto de
   **contra-evidência documentada** (G4C006). Existem análises paralelas —
   oclusiva central vs. fricção glotal regional — preservadas como registros
   simultâneos (G4C006 e G4C007), sem fusão silenciosa.
3. Convenção pedagógica (`h`) é distinta de realização histórica (G4C008,
   G4C009): usar `h` em lições não autoriza preencher saltillo lexical em
   lemmas.
4. Ausência de diacrítico não é evidência de ausência de saltillo
   (`UNKNOWN` mantém o estado; ver policy `classical_phonology_v1`).
5. Dados de variedades modernas (Hueyapan/Mecayapan) mudam de escopo e não são
   usados como prova clássica direta (G4C028); D01/D02 são síntese secundária.

## Validação

`validate_gate4.py` rejeita saltillo `PRESENT`/`ABSENT` sem Evidence, dado moderno
como `DIRECT_CLASSICAL_EVIDENCE`, e marca ausente tratada como ausência de
saltillo. Teste negativo: `tests/test_gate4_validator.py::test_T01`.

## Pendências para revisão externa

- Confirmar se `/ʔ/` ou a leitura fricativa regional deve liderar para cada
  localidade do recorte central.
- Inspeção independente de testemunhos (Rincón, Carochi) e páginas integrais de
  Karttunen/Lockhart/Andrews.
- Preencher saltillo lexical de lemmas só com Evidence por-token.
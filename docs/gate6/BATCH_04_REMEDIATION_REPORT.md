# Batch 04 — remediação após FAIL externo

Estado: PASS_AFTER_REMEDIATION / AWAITING_EXTERNAL_REVIEW após validação técnica.
Último checkpoint aceito externamente: 3 / 200; total físico: 250 DRAFT/IN_REVIEW.

## Causa raiz

O ledger foi lido no Windows PowerShell sem `-Encoding utf8` e regravado
repetidamente. Isso reinterpretou bytes UTF-8 usando a codificação legada e
propagou texto corrompido pelo pipeline. A tentativa anterior de corrigir uma
linha repetiu o problema. Também havia erros independentes de transcrição e
tradução. Os validators verificavam estrutura e replay, mas aceitavam texto
corrompido coerente com a entrada. O PASS anterior não provava fidelidade visual.

## Reinspeção e reconstrução

50/50 entradas comparadas com a imagem JCB manifest page 300, colunas a/b.
Imagem original inspecionada e ampliações locais da mesma imagem; hashes e URL
nos registros. Nenhum OCR foi usado. O ledger foi escrito diretamente em UTF-8
com apply_patch e reaberto com decodificação UTF-8 estrita. Nenhum auto-decode,
ftfy ou substituição heurística foi aplicado. Cada registro foi regenerado pelo
Gate 5, preservando L0201–L0250 e recalculando IDs e digest derivados.

Glosas são excertos curtos contíguos; quebras tipográficas são reunidas e os
separadores de entrada ficam fora do headword. O s longo é preservado como ſ;
ligaturas tipográficas ct são representadas pelas duas letras, sem modernizar
grafia. A abreviação em “depoſicion” foi evitada mediante excerto mais curto.
Confidence MEDIUM e NEEDS_SEMANTIC_REVIEW continuam explícitos.

L0202 e entradas com expressão, prefixação editorial da fonte ou remissão
(especialmente L0245) ainda exigem revisão de identidade lexical. Fidelidade
de transcrição não confirma independência lexical nem aprova Claims.

## Controles preventivos

Gate 6 verifica assinaturas de mojibake e controles, incluindo strings JSON
escapadas, sem alterar conteúdo; caracteres históricos não-ASCII continuam
válidos. O scan abrange todos os ledgers, registros canônicos, coverage,
duplicidades, Preview e relatórios de lote. O CI chama esse controle por
--check-current. Concordância 1:1 do ledger Batch 04 e regressões editoriais
L0241–L0243 são obrigatórias nos dois modos de checkpoint.

## Contagens reproduzíveis

As categorias de correção se sobrepõem; não devem ser somadas. A lista por ID
permite verificar a união de registros alterados e os registros inalterados.
TRUE_MOJIBAKE identifica assinaturas do detector; ç, ſ, ñ e acentos observados
são LEGITIMATE_HISTORICAL_TEXT. Não há exceções de mojibake liberadas nos dados.

## Validação local

103 testes unittest: PASS. Gates 3/4/5: PASS. Gate 6 checkpoint 4 e
--check-current: PASS. Exporter reproduzível, audit_publication e
audit_preview_dist: PASS. npm ci, npm test e npm run build: PASS.
L0001–L0200 não foram alterados. A verificação remota e o smoke no navegador
serão informados na entrega; aprovação externa continua pendente.

```json
{
  "baseline_comparison_commit": "8f33f82aeba8c0691e9ac6b5b19d57b03916e192",
  "records_inspected": 50,
  "source_form_corrections": 14,
  "historical_gloss_corrections": 50,
  "pt_br_corrections": 35,
  "semantic_domain_corrections": 18,
  "records_with_encoding_corrections": 23,
  "records_unchanged": 0,
  "unresolved_transcription": 0,
  "true_mojibake_remaining": 0,
  "duplicate_candidates": 32,
  "reviewed_ledger_sha256": "5e7a3c4783aeb9af2e009f4ca7247f88229c578730473dc41d6ee51f756747c7"
}
```

| ID | Campos corrigidos | Reinspeção |
|---|---|---|
| L0201 | source_form, historical_gloss, domain | COMPLETE |
| L0202 | source_form, historical_gloss, pt_br, domain | COMPLETE |
| L0203 | historical_gloss, pt_br, domain | COMPLETE |
| L0204 | source_form, historical_gloss, pt_br | COMPLETE |
| L0205 | historical_gloss, pt_br | COMPLETE |
| L0206 | historical_gloss, pt_br | COMPLETE |
| L0207 | historical_gloss, domain | COMPLETE |
| L0208 | source_form, historical_gloss, domain | COMPLETE |
| L0209 | historical_gloss, domain | COMPLETE |
| L0210 | historical_gloss | COMPLETE |
| L0211 | historical_gloss, pt_br, domain | COMPLETE |
| L0212 | historical_gloss, pt_br | COMPLETE |
| L0213 | historical_gloss, pt_br, domain | COMPLETE |
| L0214 | historical_gloss, pt_br | COMPLETE |
| L0215 | historical_gloss, pt_br, domain | COMPLETE |
| L0216 | source_form, historical_gloss, pt_br, domain | COMPLETE |
| L0217 | source_form, historical_gloss, pt_br | COMPLETE |
| L0218 | historical_gloss, pt_br, domain | COMPLETE |
| L0219 | historical_gloss, pt_br | COMPLETE |
| L0220 | historical_gloss, pt_br, domain | COMPLETE |
| L0221 | historical_gloss, domain | COMPLETE |
| L0222 | historical_gloss, pt_br | COMPLETE |
| L0223 | historical_gloss, pt_br | COMPLETE |
| L0224 | historical_gloss, pt_br | COMPLETE |
| L0225 | historical_gloss | COMPLETE |
| L0226 | source_form, historical_gloss, pt_br | COMPLETE |
| L0227 | historical_gloss | COMPLETE |
| L0228 | historical_gloss, pt_br | COMPLETE |
| L0229 | source_form, historical_gloss, pt_br, domain | COMPLETE |
| L0230 | source_form, historical_gloss, pt_br, domain | COMPLETE |
| L0231 | historical_gloss, pt_br | COMPLETE |
| L0232 | historical_gloss, pt_br | COMPLETE |
| L0233 | historical_gloss | COMPLETE |
| L0234 | source_form, historical_gloss | COMPLETE |
| L0235 | historical_gloss | COMPLETE |
| L0236 | historical_gloss | COMPLETE |
| L0237 | source_form, historical_gloss, pt_br | COMPLETE |
| L0238 | historical_gloss, pt_br | COMPLETE |
| L0239 | source_form, historical_gloss | COMPLETE |
| L0240 | source_form, historical_gloss, pt_br, domain | COMPLETE |
| L0241 | historical_gloss, pt_br | COMPLETE |
| L0242 | historical_gloss, pt_br | COMPLETE |
| L0243 | historical_gloss, pt_br | COMPLETE |
| L0244 | historical_gloss, pt_br, domain | COMPLETE |
| L0245 | historical_gloss, pt_br, domain | COMPLETE |
| L0246 | historical_gloss, pt_br | COMPLETE |
| L0247 | historical_gloss | COMPLETE |
| L0248 | source_form, historical_gloss | COMPLETE |
| L0249 | historical_gloss, pt_br | COMPLETE |
| L0250 | historical_gloss, pt_br | COMPLETE |

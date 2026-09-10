# Gate 6 — BATCH 05 REPORT

## Status do Checkpoint
- Checkpoint: **PASS**
- Batch: **05** (L0251–L0300)
- Estado do Batch: **PASS / AWAITING_EXTERNAL_REVIEW**
- Lemmas no lote: 50
- Total acumulado no corpus: **300**
- Gate 6: **IN_PROGRESS / SOURCE_EVIDENCE_PATH_RESOLVED**
- Gate 7: **NOT_STARTED**

## Inspeção Visual e Testemunho
- **Fonte principal**: A01 — Alonso de Molina (1571), *Vocabulario en lengua mexicana y castellana*, parte II (mexicana-castellana).
- **Testemunho**: John Carter Brown Library, cota `1-SIZE B571 .M722v`.
- **Componente**: `jcb_1571_images`.
- **Direitos**: CC BY 4.0, com atribuição explícita (*Courtesy of the John Carter Brown Library*).
- **Inspeção**: Inspeção visual direta (`direct_witness_inspected = true`, `VISUALLY_INSPECTED`).
- **Papel do OCR**: `LOCATOR_ASSIST_ONLY`. OCR nunca é evidência primária nem substitui a transcrição visual. Discrepâncias de OCR (erros de `ſ`/`f`/`s`, ligaturas tipográficas e quebras de linha) foram resolvidas pela primazia da imagem.

### Páginas e Canvases Inspecionados
1. **Página 280** (manifest page 280 / canvas 280):
   - Canvas ID: `https://americana.jcblibrary.org/iiif/presentation/canvas/jcbcap-991031815189706966-vocabularioenlen00moli/manifest__442984__26711183/canvas.json`
   - IIIF Image URL: `https://jcb.lunaimaging.com/luna/servlet/iiif/JCB~3~3~21781~115907151page279/full/2000,/0/default.jpg`
   - SHA-256 da imagem: `48330252fbbc882dd0e2653b2de87258aa7f9bca407f8de327c7cb2cee43d30a`
   - Entradas selecionadas: 25 (coluna a: 17; coluna b: 8)
2. **Página 290** (manifest page 290 / canvas 290):
   - Canvas ID: `https://americana.jcblibrary.org/iiif/presentation/canvas/jcbcap-991031815189706966-vocabularioenlen00moli/manifest__442984__26711193/canvas.json`
   - IIIF Image URL: `https://jcb.lunaimaging.com/luna/servlet/iiif/JCB~3~3~21781~115907151page289/full/2000,/0/default.jpg`
   - SHA-256 da imagem: `118138998feef967968bc7437a5e555a67a03d02111acd8078288f102836d683`
   - Entradas selecionadas: 25 (coluna a: 21; coluna b: 4)

- **Total de páginas inspecionadas**: 2
- **Entradas por página**: Página 280: 25; Página 290: 25
- **Candidatos considerados**: 50
- **Aceitos**: 50
- **Rejeitados**: 0
- **Transcrições não resolvidas**: 0

## Concentração Lexical e Distribuição
- **Concentração alfabética**: Seção `Ca-` (Página 280): 25/50 (50%); Seção `Ce-` (Página 290): 25/50 (50%).
- **Concentração por família/radical (headword family)**:
  - Página 280: maior família com 4 entradas (8% do lote).
  - Página 290: maior família com 5 entradas (10% do lote).
  - Nenhuma família atinge o limiar de 80%.
  - Warning `LEXICAL_FAMILY_CONCENTRATION`: **NÃO EMITIDO (PASS)**.
- **Distribuição de domínios semânticos (50 novos lemmas)**:
  - `corpo`: 7
  - `natureza`: 6
  - `percepção`: 5
  - `quantidade`: 5
  - `ações`: 4
  - `espaço`: 4
  - `pessoas`: 4
  - `plantas`: 4
  - `propriedades`: 4
  - `objetos`: 3
  - `animais`: 2
  - `sociedade`: 2
  - `tempo`: 2
  - `alimentos`: 1
  - `comunicação`: 1
  - `movimento`: 1
  - `parentesco`: 1
  - `relações`: 1
  - Total de domínios no lote: 18 distintos.

## Identidade Lexical e Duplicatas
- Todos os 50 candidatos foram comparados contra L0001–L0250 antes da admissão.
- Colisões com L0001–L0250: **0**. Nenhum duplicate confirmado ou colisão de SOURCE_FORM com o corpus pré-existente.
- **Contagem total de candidatos a duplicata**: 32 pares em 300 lemmas.
- **Razão de duplicatas**: 32 / 300 = 0,1067 (10,67%), abaixo do teto de 0,15 (15%).
- Warning `HIGH_DUPLICATE_REVIEW_LOAD`: **NÃO EMITIDO (null)**.
- **Status de identidade dos 32 pares**:
  - `LEXICAL_IDENTITY_UNRESOLVED`: 32
  - `ORTHOGRAPHIC_COLLISION`: 0
  - `POSSIBLE_SAME_LEXEME`: 0
  - `POSSIBLE_HOMONYM`: 0
  - `CONFIRMED_DISTINCT`: 0
  - `CONFIRMED_DUPLICATE`: 0
- Nenhum merge automático executado (`automatic_merge = false`).

## Evidência e Cobertura Editorial
- **Novos lemmas**: L0251–L0300 (50 registros canônicos).
- **Attestations**: 348 no corpus (50 novas no Batch 05, todas A01/jcb_1571_images).
- **Evidence**: 348 no corpus (50 novas no Batch 05).
- **Claims**: 629 no corpus (100 novas no Batch 05: 50 `has_historical_gloss` [OBSERVED, MEDIUM] e 50 `has_pt_br_editorial_gloss` [EDITORIAL, MEDIUM, DRAFT]).
- **PT-BR**: 300/300 lemmas cobertos. Todas as traduções do lote são afirmações editoriais DRAFT com proveniência explícita, sem extrapolação da glosa espanhola.
- **Revisão semântica**: 250/250 novos lemmas marcados como `NEEDS_SEMANTIC_REVIEW`.
- **Fonologia e Morfologia**: Nenhuma inferência em massa de duração vocálica (`UNKNOWN`), saltillo (`UNKNOWN`) ou IPA. Morfologia mantida como `NOT_REVIEWED`.
- **Bloqueios de Direitos**: 0.
- **Bloqueios de Variante Moderna**: 0 (exclusivamente Classical Nahuatl).

## Integridade Textual e Ledger Generalizado
- **Varredura de mojibake**: `TEXT_MOJIBAKE_DETECTED` = 0 em todos os arquivos (`batch*.tsv`, canonical JSON, coverage, duplicates, preview JSON, reports).
- **Caracteres históricos válidos**: `ſ`, `ç`, `ñ`, acentos e til preservados sem distorção.
- **Ledger Batch 05**: `data/gate6/batches/batch05.tsv`.
- **Hash do Ledger**: `5820b50432f5e1109a7358d2ec75959c5086fd1c50675e2867bae41f7512be3e`.
- **Concordância Ledger ↔ Canonical**: 50/50 concordantes em `page`, `column`, `source_form`, `historical_gloss`, `pt_br`, `domain`.
- `BATCH_LEDGER_CANONICAL_DRIFT`: **0**.
- `REVIEWED_LEDGER_HASH_MISMATCH`: **0**.

## Métricas Automatizadas do Corpus (300 Lemmas)

```json
{
  "attestations_count": 348,
  "attestations_per_lemma": {
    "1": 252,
    "2": 48
  },
  "blocks_note": "No prohibited capture submitted for corpus admission; negative fixtures reported separately.",
  "claims_count": 629,
  "context_directly_inspected": 0,
  "context_references": 47,
  "duplicate_candidates": 32,
  "duplicate_identity_statuses": {
    "LEXICAL_IDENTITY_UNRESOLVED": 32
  },
  "duplicate_review_warning": null,
  "duplicate_trend_checkpoints": {
    "batch01": 3,
    "batch02": 8,
    "batch03": 18,
    "batch04": 32,
    "current": 32
  },
  "editorial_states": {
    "DRAFT": 250,
    "IN_REVIEW": 50
  },
  "evidence_count": 348,
  "historical_attestation_coverage": 300,
  "lexical_class": {
    "NOT_REVIEWED": 300
  },
  "modern_variety_blocks_admission": 0,
  "morphology_coverage": 12,
  "multi_source": 48,
  "new_lemmas": 250,
  "pt_br_coverage": 300,
  "rights_blocks_admission": 0,
  "saltillo_evidence": 10,
  "semantic_domain_editorial": {
    "NOT_CLASSIFIED": 50,
    "NOT_REVIEWED": 1,
    "alimentos": 6,
    "animais": 8,
    "ações": 6,
    "cognição": 18,
    "comunicação": 1,
    "comércio": 5,
    "corpo": 27,
    "emoções": 21,
    "espaço": 5,
    "expressões": 1,
    "fala": 3,
    "guerra": 3,
    "movimento": 11,
    "natureza": 7,
    "objetos": 30,
    "parentesco": 2,
    "percepção": 9,
    "pessoas": 8,
    "plantas": 6,
    "propriedades": 1,
    "qualidades": 4,
    "quantidade": 30,
    "relações": 17,
    "religião": 1,
    "saúde": 1,
    "sociedade": 4,
    "tempo": 8,
    "trabalho": 5,
    "ética": 1
  },
  "semantic_review_candidates": 250,
  "single_source": 252,
  "sources_distribution": {
    "A01": 299,
    "A02": 2,
    "A04": 47
  },
  "total_lemmas": 300,
  "vowel_length_evidence": 23
}
```

# Gate 6 — Audit report

Executor: `EXECUTION_AGENT`. Gate 6 foi autorizado pelo PRODUCT_OWNER e pelo
ORCHESTRATOR_REVIEWER, mas o executor não aprova nem encerra o Gate.

## Estado do trabalho

`GATE_6_STATUS: IN_PROGRESS / SOURCE_EVIDENCE_PATH_RESOLVED`

Os lotes 01 e 02 passaram pelo pipeline aprovado e elevaram o corpus de 50 para
150. O alvo de 500 continua aberto. A resolução operacional do bloqueio permite
usar OCR somente como locator assist; cada registro ainda exige captura visual
JCB e Evidence da imagem. O download dos arquivos OCR do IA continua bloqueado
por DNS neste ambiente, sem alterar a elegibilidade do caminho visual.

## Controles executados

- Preflight de escala: A01 JCB/Luna `jcb_1571_images`, CC BY 4.0, manifesto IIIF,
  589 canvases; BVPB surrogate continua RIGHTS_UNCLEAR.
- 50 novos registros: IDs L0051–L0100, Classical Nahuatl, SOURCE_FORM e
  Evidence de imagem visualmente inspecionados, locators e hashes.
- 50 novos registros: IDs L0101–L0150, com o mesmo Witness e controles; BATCH 02
  PASS, oito candidatos de duplicidade preservados.
- 50 novas traduções PT-BR: EDITORIAL, DRAFT, derivadas da Evidence, sem atribuí-las
  como tradução histórica.
- Pipeline Gate 5: source, rights, variety, normalization, builders, replay e
  idempotência PASS.
- Baseline Gate 3: hash semântico e blob hash preservam L0001–L0050.
- Duplicidade: 3 candidatos; nenhum merge automático.
- Suíte Gate 6: 20 testes (18 negativos + controles positivos) PASS.
- Locator OCR: manifest dos nomes remotos reais e invariantes `OCR_NOT_LINGUISTIC_EVIDENCE`
  implementados; nenhum OCR bruto foi versionado.

## Métricas

Os valores completos do checkpoint estão em
`docs/20_GATE_6_COVERAGE_REPORT.md`, `docs/gate6/BATCH_02_REPORT.md` e
`data/gate6/coverage.json`. Cobertura de attestation histórica e PT-BR é
150/150. Multi-source real é 48/150; single-source é 102/150. Context
references=47 e context directly inspected=0.
Novos registros não adicionam Evidence fonológica nem morfologia.

## Decisão operacional

O bloqueio `BLOCKED_BY_SOURCE_EVIDENCE` foi resolvido operacionalmente por
`SOURCE_EVIDENCE_PATH_RESOLVED`; OCR continua sem valor de Evidence. A expansão
além do BATCH 02 só prossegue com mais capturas visualmente verificáveis. O
estado permanece IN_PROGRESS; Gate 7 permanece NOT_STARTED. Não criar
`gate-6-approved`, não promover Claims e não alterar os 50 registros baseline.

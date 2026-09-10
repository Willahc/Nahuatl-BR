# Gate 6 — Audit report

Executor: `EXECUTION_AGENT`. Gate 6 foi autorizado pelo PRODUCT_OWNER e pelo
ORCHESTRATOR_REVIEWER, mas o executor não aprova nem encerra o Gate.

## Estado do trabalho

`GATE_6_STATUS: IN_PROGRESS / BLOCKED_BY_SOURCE_EVIDENCE`

O primeiro lote de 50 novos lemmas passou pelo pipeline aprovado e elevou o
corpus de 50 para 100. O alvo de 500 não foi preenchido porque a regra de
qualidade exige parar quando não há capturas históricas suficientes e não
permite inventar ou copiar em massa. Próximo lote requer nova captura visual
controlada e validação do checkpoint anterior.

## Controles executados

- Preflight de escala: A01 JCB/Luna `jcb_1571_images`, CC BY 4.0, manifesto IIIF,
  589 canvases; BVPB surrogate continua RIGHTS_UNCLEAR.
- 50 novos registros: IDs L0051–L0100, Classical Nahuatl, SOURCE_FORM e
  Evidence de imagem visualmente inspecionados, locators e hashes.
- 50 novas traduções PT-BR: EDITORIAL, DRAFT, derivadas da Evidence, sem atribuí-las
  como tradução histórica.
- Pipeline Gate 5: source, rights, variety, normalization, builders, replay e
  idempotência PASS.
- Baseline Gate 3: hash semântico e blob hash preservam L0001–L0050.
- Duplicidade: 3 candidatos; nenhum merge automático.
- Suíte Gate 6: 20 testes (18 negativos + controles positivos) PASS.

## Métricas

Os valores completos do checkpoint estão em
`docs/20_GATE_6_COVERAGE_REPORT.md` e `data/gate6/coverage.json`. Cobertura de
attestation histórica e PT-BR é 100/100. Multi-source real é 48/100; single-
source é 52/100. Context references=47 e context directly inspected=0.
Novos registros não adicionam Evidence fonológica nem morfologia.

## Decisão operacional

`BLOCKED_BY_SOURCE_EVIDENCE` para a expansão além de BATCH 01 nesta execução.
O estado permanece IN_PROGRESS; Gate 7 permanece NOT_STARTED. Não criar
`gate-6-approved`, não promover Claims e não alterar os 50 registros baseline.

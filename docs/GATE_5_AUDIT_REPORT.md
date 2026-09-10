# Gate 5 — Relatório de auditoria (entrega do pipeline de ingestão e prévia)

Executor: `EXECUTION_AGENT`. Esta auditoria documenta a entrega parcial do Gate 5
(pipeline, fixtures, validação, exporter e Research Preview 0). **Não aprova nem
encerra o Gate**: o `PRODUCT_OWNER` humano autoriza ou rejeita a progressão,
após recomendação do `ORCHESTRATOR_REVIEWER`.

`GATE_5_DELIVERY_STATUS: IN_PROGRESS — NÃO APROVADO`

## Escopo entregue

- Pipeline canônico em `src/pipeline/` (models, errors, loader, gates,
  normalize, builders, engine, cli).
- 32 fixtures em `data/fixtures/gate5_ingestion_cases/` (G5-001..G5-032):
  8 ACCEPT + 24 REJECT com códigos esperados.
- `scripts/validate_gate5.py --check` (validação read-only) e
  `scripts/build_preview_data.py` (exporter determinístico).
- `tests/test_gate5_pipeline.py` (11 testes de regressão em árvore temporária).
- Research Preview 0: `preview/` (Vite + React + TS) + `preview/public/data/nahuatl-br.json`.
- Docs 15/16/17 + atualização da cadeia de validação de CI.

## Verificações (validador automático)

| Controle | Resultado |
|---|---|
| 32 fixtures: outcome e códigos por fixture em subconjunto esperado | PASS |
| Comportamento estável do engine (digest idêntico em re-execução) | PASS |
| Negação obrigatória: `RIGHTS_PERMISSION`, `RIGHTS_DO_NOT_INGEST`, `RIGHTS_UNCLEAR`, `RIGHTS_REFERENCE_ONLY`, `MODERN_AS_CLASSICAL_EVIDENCE` exercitadas | PASS |
| Cobertura de fontes modernas C01/C02/C03 em fixtures REJECT | PASS |
| Fixtures ACCEPT geram artefatos (forms/claims/evidence) e REJECT sem artefato | PASS |
| Claims de pipeline nascem `DRAFT` + origem `PIPELINE` + Evidence vinculada | PASS |
| Export da prévia reproduzível de dados canônicos (`--check`) | PASS |
| Prévia com 50 lemas; sem C01/C02/C03 em `sources`; `generated_at: NOT_RECORDED` | PASS |
| `python -m unittest discover -s tests` (47 Gate 4 + 11 Gate 5) | PASS |
| `npm run build` (tsc -b + vite build) com `preview/` | PASS |

## Resultados de validação na entrega

```
GATE 5 VALIDATION: PASS
  fixtures_total: 32, engine_passes: ALL, exporter_reproducible: true
GATE 5 EXPORT: PASS (deterministic preview data)
Ran 58 tests ... OK
✓ built in 1.08s (vite v7.3.6)
```

## Invariantes respeitados

- `SOURCE_FORM` imutável (`SOURCE_FORM_MUTATION` como protetor).
- `SEARCH_KEY` marcado lossy; `declared_lossy` exigido (`LOSSY_UNDECLARED`).
- Sem inferência de comprimento vocálico, saltillo ou IPA sem evidência
  (`PHONOLOGY_AUTOGENERATION`, `SALTILLO_EVIDENCE_REQUIRED`, `AUTO_SHORT_INFERENCE`).
- Variedade moderna nunca alimenta evidência clássica
  (`MODERN_AS_CLASSICAL_EVIDENCE`), por metadados estruturados.
- Direitos resolvidos por `source_id + component_id`; `AGGREGATOR` exige
  mediator; testemunho direto exige inspeção declarada.
- Dados do Gate 4 inalterados (29 Claims `IN_REVIEW`, label histórico
  `classical_phonology_v1@1.0.0-draft.1` preservado).

## Remediação final autorizada pelo PRODUCT_OWNER

`GATE_5_DELIVERY_STATUS: IN_PROGRESS / AWAITING_EXTERNAL_REVIEW`
`RESEARCH_PREVIEW_PUBLIC_DEPLOYMENT: AUTHORIZED`
Gate 6: `NOT_STARTED`. A autorização atual substitui o escopo antigo do
AGENTS.md; o EXECUTION_AGENT não aprova nem encerra o Gate 5.

- `search-diacritic-001` usa exclusivamente a whitelist `ā ē ī ō Ā Ē Ī Ō`.
  NFC e lowercase continuam em suas regras próprias. Grave, agudo, circunflexo,
  trema, til, cedilha e marcas combinantes não listadas não são removidos.
- `xöchitl` recupera L0050 pela SOURCE_FORM histórica existente; `xochitl`
  recupera L0050 pela SEARCH_KEY exportada / NORMALIZED_FORM existente.
  Não há transformação `ö → o`. Igualdade de SEARCH_KEY não cria Claim de
  identidade linguística. Nenhum dado linguístico ou policy foi ampliado.
- O frontend prioriza SEARCH_KEYs exportadas, sem recalculá-las. A query usa
  apenas NFC, lowercase e a whitelist de macrons. As demais representações
  e textos editoriais usam correspondência literal sem folding de acentos.
- **C02 mantida**: `clin_metadata` cobre CAN_REFERENCE / modern Variety;
  RIGHTS_UNCLEAR tem cobertura estrutural independente. Não adicionar caso
  obrigatório `alin_archive`. ALIN/Audiorama ficam para trabalho explícito
  futuro com modern varieties/audio; nenhum áudio é criado nesta entrega.
- Publicação autorizada exclusivamente de `preview/dist`, com base
  `/Nahuatl-BR/`, HashRouter e aviso visível de Research Preview / IN_REVIEW.

## Critérios formais de saída

Gate 5 só pode receber PASS após todos os controles abaixo passarem e revisão
externa; o executor não converte resultados técnicos em fechamento do Gate.

- Pipeline determinístico e read-only por padrão; Source resolution, Rights
  Gate, Variety Gate e SOURCE_FORM immutable PASS.
- Normalização somente por rules aprovadas, sem hidden transformations;
  Claims geradas DRAFT, Evidence resolvida e idempotência PASS.
- 32 fixtures com outcomes esperados e mandatory negative classes cobertas.
- Preview derivado e reproduzível, exatamente 50 lemmas, sem ingestão de
  fontes modernas/restritas.
- Regressões Gate 3 e Gate 4, validator Gate 5, suíte completa, testes de
  busca frontend e npm build PASS.
- Publication security PASS e CI remoto PASS.

O deploy depende do sucesso do CI principal para o mesmo commit. O workflow
publica somente `preview/dist`, com permissões de Pages/OIDC limitadas ao job
de deploy e sem token customizado. Resultado remoto e verificação HTTP/rotas
serão apresentados no relatório de execução após o push.

### Validação local da remediação — 2026-09-10

Gate 3, Gate 4 e Gate 5: PASS. As 32 fixtures mantêm os outcomes esperados;
idempotência e export reproduzível: PASS. Suíte completa: **60 testes PASS**.
`npm ci`, `npm test`, `npm run build`, `audit_publication.py`,
`audit_preview_dist.py` e `git diff --check`: PASS.
Nenhum arquivo em `data/` nem o JSON canônico derivado precisou ser alterado.
O teste frontend executa a busca real nos 50 lemmas e isola SOURCE_FORM de
SEARCH_KEY para provar os caminhos distintos de recuperação de L0050.
Glosas históricas que já eram listas são percorridas como texto na busca;
seu conteúdo permanece inalterado.

Pages foi habilitado pela API oficial com `build_type: workflow`, no repositório
público `Willahc/Nahuatl-BR`; HTTPS habilitado. Não foi necessária intervenção
manual em Settings. O workflow segue as [instruções oficiais de Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Declaração

- Nenhuma tag `gate-5-approved` foi criada.
- Nenhuma licença, autoria, cobertura ou método de extração foi confirmado sem
  verificação documental.
- Nenhum arquivo-fonte original foi modificado; o exporter e o pipeline são
  read-only por construção.
- Claims fonológicas permanecem `IN_REVIEW` com origem EXECUTION_AGENT; a
  revisão humana individual não está documentada.

## EXTERNAL REVIEW DECISION

Decisão externa comunicada pelo PRODUCT_OWNER em 2026-09-10, após revisão do
ORCHESTRATOR_REVIEWER. As seções anteriores preservam a autoauditoria histórica
e os estados vigentes nas entregas; esta seção registra o fechamento formal.
O EXECUTION_AGENT registra a decisão externa, sem aprovar o próprio trabalho.

```text
ORCHESTRATOR_REVIEWER_DECISION: PASS
GATE_5_STATUS: CLOSED
PIPELINE_USE: APPROVED
RESEARCH_PREVIEW_STATUS: APPROVED
PUBLIC_DEPLOYMENT_STATUS: APPROVED
Gate 6: AUTHORIZED / NOT_STARTED
```

Todos os critérios formais de saída definidos neste relatório foram satisfeitos.
As reservas futuras não reabrem o Gate 5.

Referências da entrega aprovada:

- Initial delivery: `c310429`.
- Search-policy remediation: `1f7c913`.
- Preview-label finalization: `40f1623`.
- [CI principal aprovado](https://github.com/Willahc/Nahuatl-BR/actions/runs/34477470190).
- [Deploy aprovado](https://github.com/Willahc/Nahuatl-BR/actions/runs/34477517132).
- Public Research Preview: https://willahc.github.io/Nahuatl-BR/

A aprovação abrange pipeline read-only/dry-run, Source resolution, Rights Gate,
Variety Gate, transformações governadas por policy, geração de candidatos DRAFT,
idempotência, exporter determinístico, Research Preview 0 e deployment estático
controlado. O Research Preview é produto derivado, não fonte canônica; seu
deployment, design e conteúdo linguístico permanecem preservados. Somente os
metadados derivados de status dos Gates acompanham este fechamento.

Não há aprovação automática de ingestão irrestrita de fontes, fontes
RIGHTS_UNCLEAR, Hueyapan, modern varieties como Classical, Claims individuais,
IPA em massa, áudio, scraping em massa ou conteúdo dos futuros 500 lemmas.

**Gate approval != Claim publication.** Os estados atuais permanecem intactos;
nenhuma Claim passa de DRAFT ou IN_REVIEW para PUBLISHED. Nenhum dos 50 lemmas
é alterado. Nenhum validator é enfraquecido. Gate 6 não é iniciado nesta execução.

O commit `docs: close Gate 5 ingestion pipeline` registra este fechamento.
A tag anotada `gate-5-approved`, com mensagem
`Gate 5 approved: canonical ingestion pipeline and Research Preview 0`, deve
apontar exatamente para esse commit, sendo criada e enviada somente após
SUCCESS do CI principal e do deploy correspondentes.

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

## Decisões abertas (para o PRODUCT_OWNER / Orquestrador)

1. **Mapeamento de busca lossy**: SEARCH_KEY atualmente converte `ö→o` como
   convenção de recuperação com `declared_lossy: true`. Confirmar que a
   convenção deve ser oficializada na política de ortografia.
2. **Fixture C02**: a negação C02 usa `clin_metadata` (CAN_REFERENCE) como
   alvo de captura indevida; confirmar se um segundo caso envolvendo o dicionário
   INALI (componente `alin_archive`) deve ser mantido como referência.
3. **Evolução da policy `classical_orthography_v1`**: permanece
   `APPROVED`/1.0.0 no escopo atual; qualquer mudança de normalização deve ser
   versionada e revalidada.
4. **Prévia como GitHub Pages**: nenhum workflow de deploy foi criado; o build
   `npm run build` é validado em CI, e a publicação é decisão futura do
   PRODUCT_OWNER.
5. **Condições de saída do Gate 5**: entrada (`IN_PROGRESS`), saída e aprovação
   seguem pendentes de definição pelo PRODUCT_OWNER; o Gate 6 segue
   `NOT_STARTED`.

## Declaração

- Nenhuma tag `gate-5-approved` foi criada.
- Nenhuma licença, autoria, cobertura ou método de extração foi confirmado sem
  verificação documental.
- Nenhum arquivo-fonte original foi modificado; o exporter e o pipeline são
  read-only por construção.
- Claims fonológicas permanecem `IN_REVIEW` com origem EXECUTION_AGENT; a
  revisão humana individual não está documentada.
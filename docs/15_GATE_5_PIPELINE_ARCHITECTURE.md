# Arquitetura do pipeline de ingestão (Gate 5)

Executor: `EXECUTION_AGENT`. O Gate 5 permanece `IN_PROGRESS` (ver
`docs/GATE_STATUS.md`). Este documento descreve a arquitetura do pipeline
canônico de ingestão implementado nesta entrega; **não** constitui aprovação ou
encerramento do Gate.

## Princípios

1. **Canônico → Derivado.** Os dados canônicos vivem em `data/` e nunca são
   alterados pelo pipeline: o CNL processa um fixture em memória e, quando
   aprovado, produz artefatos derivados (`DRAFT`/`PIPELINE`). Não há escrita em
   `data/pilot/` ou `data/phonology/` nesta entrega.
2. **Determinismo.** Mesmo fixture + mesmas políticas agregadas + mesmo registry
   ⇒ mesmo digest SHA-256, mesmo conjunto de artefatos e de códigos de erro.
3. **Idempotência.** Executar o mesmo fixture duas vezes produz exatamente o
   mesmo resultado.
4. **Proveniência no nível da afirmação.** Cada Claim carrega modalidade
   epistêmica, origem (`PIPELINE`), estado editorial e Evidence vinculada.
5. **Busca ≠ evidência.** `SEARCH_KEY` é utilitário de recuperação e nunca é
   evidência linguística (AGENTS.md §14). Mapping de busca é rotulado `lossy`
   e exige declaração explícita no fixture.
6. **Permissão primeiro.** O Rights Gate resolve `source_id + component_id` no
   registro de fontes e decide o uso antes de qualquer análise linguística.

## Módulos

| Módulo | Responsabilidade |
|---|---|
| `src/pipeline/models.py` | Esquemas (Policy, Artifact, Claim, Evidence, SearchKey), `PIPELINE_VERSION`, `IngestionResult` (outcome/errors/artifacts/stages/digest) |
| `src/pipeline/errors.py` | Códigos de erro tipados e mensagens verificáveis |
| `src/pipeline/loader.py` | Leitura canônica (JSON e YAML-subset), registry, policies, baseline, status |
| `src/pipeline/gates.py` | Permissões (`RightsGate`/`EligibilityGate`) e classificação de modernidade |
| `src/pipeline/normalize.py` | Normalização editorial e mapping de busca com auditoria (lossy/declared) |
| `src/pipeline/builders.py` | Primitivas de construção de forms, claims e evidence |
| `src/pipeline/engine.py` | Encadeamento de estágios, digest e resultado final |
| `src/pipeline/cli.py` | `python -m src.pipeline.cli ingest <fixture>` / `ingest-all --root .` (read-only) |

## Estágios

`PRE_FLIGHT → RIGHTS → VARIETY → SOURCE_FORM_IMMUTABILITY → NORMALIZATION →
REQUIRED_FORMS → AGGREGATOR_MEDIATION → PROVENANCE → CLAIM_EVIDENCE →
PHONOLOGY → SEARCH_KEY → BUILD → CANONICAL_ARTIFACT`

- Fixtures de busca/referência pura (`SEARCH_ONLY`, `REFERENCE_ONLY`) não geram
  forms, claims, evidence ou atestações (`capture = false`).
- Claims nascem `DRAFT` com origem `PIPELINE` e carregam Evidence vinculada.
- Nenhuma duração vocálica, saltillo ou IPA é inferida sem evidência
  (`PHONOLOGY_AUTOGENERATION`, `SALTILLO_EVIDENCE_REQUIRED`,
  `AUTO_SHORT_INFERENCE`).
- Variedade moderna usada como evidência clássica é rejeitada
  (`MODERN_AS_CLASSICAL_EVIDENCE`) por metadados estruturados, sem depender do
  nome da variedade.

## Validação

- `scripts/validate_gate5.py --check` (read-only): executa os 32 fixtures,
  exige outcome e subconjunto de códigos esperados, verifica determinismo
  (digest idêntico em execução repetida), cobre negações obrigatórias
  (`RIGHTS_PERMISSION`, `RIGHTS_DO_NOT_INGEST`, `RIGHTS_UNCLEAR`,
  `RIGHTS_REFERENCE_ONLY`, `MODERN_AS_CLASSICAL_EVIDENCE`, e C01/C02/C03) e
  compara o export em memória com o arquivo commitado da prévia.
- `tests/test_gate5_pipeline.py`: 11 testes de regressão executados em árvore
  temporária (cópia de `data/`, `src/`, `scripts/` e da prévia); nunca toca o
  repositório canônico.

## Determinismo do export da prévia

`scripts/build_preview_data.py` produz `preview/public/data/nahuatl-br.json`
com `generated_at: NOT_RECORDED`, ordenação estável e sem fontes modernas
(C01/C02/C03). `--check` (padrão) compara em memória e falha em qualquer
deriva; `--write` regenera o arquivo commitado.
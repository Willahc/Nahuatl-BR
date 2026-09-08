# Gate 4 — Autoauditoria da fonologia (infraestrutura de validação)

Executor: `EXECUTION_AGENT`. Esta auditoria documenta a infraestrutura de
validação e o reexame dos artefatos do Gate 4. **Não aprova nem encerra o Gate**:
a revisão humana do conteúdo e a progressão são do `PRODUCT_OWNER`, após
recomendação do `ORCHESTRATOR_REVIEWER`.

`AUDIT_RESULT: PASS_WITH_RESERVATIONS`
(recomendação de infraestrutura; não é aprovação do Gate)

## Escopo auditado

- `data/phonology/claims/G4C001..G4C029` (29 Claims, todos `IN_REVIEW`);
- `data/phonology/evidence.yml` (28 registros: 8 contextuais + 20 por-token);
- `data/fixtures/gate4_phonology_cases.yml` (32 casos G4F001–G4F032);
- `data/phonology/integration_sample.yml` (15 itens, teto 15);
- `data/phonology/gate3_baseline.yml`, `data/phonology/audio_model.yml`;
- `data/policies/classical_phonology_v1.yml` (policy `DRAFT`, v1.0.0-draft.1);
- `data/source_registry/` (A01–A04, D01–D05 e demais);
- `scripts/validate_gate4.py` e `scripts/gate3_integrity.py`.

Data: 2026-09-08. Responsável: `EXECUTION_AGENT`.

## Verificações (validador automático)

| Controle | Resultado |
|---|---|
| 29 Claims, IDs únicos e campos consistentes | PASS |
| 29/29 `IN_REVIEW`, provenança EXECUTION_AGENT, `NOT_REVIEWED` | PASS |
| 29/29 com Evidence resolvida (Claims sem Evidence ≠ `PUBLISHED`/canônicas) | PASS |
| Topics/layers/certainty/confidence/modality em vocabulário fechado | PASS |
| 28 Evidence, IDs únicos, `direct_witness_inspected: false` | PASS |
| Nenhuma variante moderna como `DIRECT_CLASSICAL_EVIDENCE` | PASS |
| 32 fixtures, Sources e Evidence resolvidas | PASS |
| 15 itens de integração, lemmas distintos e no baseline do Gate 3 | PASS |
| `SOURCE_FORM` igual ao baseline (nenhuma forma de lemma alterada) | PASS |
| Policy permanece `DRAFT` com 9 inferências proibidas | PASS |
| Zero arquivos de áudio em `data/`/`docs/`; `audio_model` sem instâncias | PASS |
| Conversão automática cu/uc, IPA em massa ou aprovação por agente | NONE |

Execução: `python scripts/validate_gate4.py --check` → `GATE 4 VALIDATION: PASS`,
com métricas JSON (29 claims, 28 evidence, 32 fixtures, 15 integração).

## Ajustes feitos durante a auditoria

A primeira execução do validador apontou `AUTO_SHORT_INFERENCE` no caso
G4F022 (`chichi` SHORT, Rincón). O caso é Evidence reportada de contraste de
quantidade (G4E001), não uma inferência de curteza aplicada a lemma do piloto.
A regra foi calibrada para exigir Evidence por-token apenas em itens de
integração (`token_rule=True`), mantendo as fixtures como casos de referência
reportados (`token_rule=False`). Nenhum dado linguístico foi alterado; apenas a
lógica de validação foi ajustada.

## Controles manuais relevantes

- G4C006 usa G4E006 como Evidence **e** contra-evidência: Canger sustenta um
  resultado glotal central mas se opõe à generalização pan-colonial. Registrado
  como análise paralela, não como contradição resolvida.
- G4C018/G4C019: stress reportado (vocativo; domínio palavra) com `INFERRED`
  apenas para G4C019, claramente declarado.
- G4F021/G4F022 (par `chichi`, `RINCON_CHICHI`) preservam LONG/SHORT com
  grafia idêntica e sentidos distintos sem fusão (G4C026).
- G4F025/G4F026 (`nohuian`/`nohuiän`, `GDN_NOHUIAN`) preservam grafias
  paralelas; nenhuma é apresentada como transcrição estreita concorrente.
- `phonemic_ipa` presente apenas em G4C006 `/ʔ/`, G4C011 `/t͡ɬ/`, G4C012 `/kʷ/`;
  nenhum `phonetic_ipa` preenchido; o restante é `NOT_REVIEWED` (G4C029).
- 20 Evidence por-token reutilizam exactamente o capture do Gate 3
  (`PROJECT_CAPTURE_REUSED`, `gate4_online_entry_reinspection: false`) e não
  são apresentadas como nova inspeção de Witness.

## Reservas (não bloqueiam a infraestrutura)

1. Escopo e cronologia regionais da fonologia clássica seguem abertos
   (especialmente a origem glotal vs. fricativa — G4C006/G4C007).
2. Realização fonética estreita (release lateral de `/t͡ɬ/`, qualidades
   vocálicas, laríngea) sem evidência acústica ou inspeção de Witness.
3. Domínios prosódicos de palavra/clítico e regra exata do acento.
4. Curteza lexical onde a grafia não marca (`UNKNOWN` é a norma).
5. Distinção diacrítico tipográfico vs. editorial nas entradas GDN.
6. Páginas integrais de Karttunen, Lockhart e Andrews não inspecionadas
   (G4C007 as cita em segundo nível).
7. Ausência de re-inspeção online das 20 entradas GDN reutilizadas.
8. Aprovação linguística especializada pendente.

Nenhuma reserva implica correção automática de conteúdo nesta entrega: alterar
Claims/Evidence para "passar" no validador seria adulterar a base linguística e
é explicitamente proibido.

## Validação de regressão

Rodados sem mutar o repositório (cópias temporárias + snapshot byte-a-byte):

- `python scripts/validate_gate4.py --check` (estado canônico) → PASS;
- `python -m unittest discover -s tests -p "test_*.py"` → 44 testes OK
  (28 Gate 3 + 16 Gate 4, incluindo negativos T01–T15);
- Gate 3 permanece fechado; artefatos do Gate 3 não foram tocados.

## Conclusão

A infraestrutura de validação do Gate 4 está completa e reproduzível, e o
conteúdo linguístico candidato permanece inalterado e `IN_REVIEW`. A progressão
do Gate 4 e a revisão das reservas acima são de responsabilidade do
`PRODUCT_OWNER`. Gate 5 não foi iniciado.

## EXTERNAL REVIEW DECISION

- `ORCHESTRATOR_REVIEWER_DECISION: PASS`
- `GATE_4_STATUS: CLOSED`
- `MODEL_USE: APPROVED`
- `INDIVIDUAL_CLAIMS: IN_REVIEW`

`PASS_WITH_RESERVATIONS` do EXECUTION_AGENT foi posteriormente aceito pelo
ORCHESTRATOR_REVIEWER. As reservas registradas nesta autoauditoria são
não bloqueadoras e **não reabrem o Gate**.

A aprovação vale para o modelo fonológico (framework de reconstrução fonêmica e
modelo de evidência ortografia→fonologia, policy
`classical_phonology_v1`, `APPROVED`, `ORCHESTRATOR_REVIEWER_GATE_4_PASS`).
Não valem como promovidos: Claims individuais (`IN_REVIEW`), fonética estreita
(como fato observado), `/ʔ/` pan-nahua, nem Evidence mediada como
`DIRECT_WITNESS`. A policy aprovada declara `approved_scope` e
`not_approved_as` correspondentes.

Gate 5: AUTHORIZED / NOT_STARTED — a implementação não foi iniciada nesta
tarefa.
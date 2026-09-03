# Gate 3 — Autoauditoria do corpus piloto

## Escopo auditado

- 50 arquivos em `data/pilot/lemmas/`;
- `data/pilot/pilot_index.yml`;
- `data/pilot/pilot_metrics.json`;
- `scripts/validate_gate3.py`;
- Witness Lock, política ortográfica, relatório do piloto e registros A01–A04/B01/B03.

Data: 2026-09-03. Responsável: `EXECUTION_AGENT`.

## Verificações

| Controle | Resultado |
|---|---|
| Exatamente 50 Lemmas e IDs únicos | PASS |
| 50/50 `Classical Nahuatl` | PASS |
| 50/50 tradução PT-BR `EDITORIAL` | PASS |
| 50/50 Attestation, Source e Work | PASS |
| Locator ou justificativa explícita | PASS |
| Claims com modalidade, Confidence e estado | PASS |
| `SOURCE_FORM` vinculada a Attestation | PASS |
| Macron pedagógico sem Evidence | NONE |
| Saltillo preenchido sem Evidence | NONE |
| `SEARCH_KEY` usada como Evidence | NONE |
| Hueyapan como Evidence clássica | NONE |
| Source ID inexistente | NONE |
| Estado editorial inválido | NONE |
| Ingestão/OCR/scraping em massa | NONE |

O primeiro ciclo do validador detectou 25 EvidenceLinks prosódicos com ID
inválido `E0`. Os links foram corrigidos para a Evidence A04 já registrada e a
segunda execução retornou `PASS`. O erro e sua correção não foram ocultados.

## Métricas verificadas

Esta subseção preserva o retrato da autoauditoria anterior. Os nomes e valores
que foram corrigidos pela revisão externa estão revogados e substituídos pela
seção `EXTERNAL REVIEW REMEDIATION` abaixo e pelo arquivo de métricas gerado.

- `total_lemmas`: 50
- `with_pt_br`: 50
- `with_primary_attestation`: 50
- `with_two_historical_sources`: 48
- `with_context`: 47
- `with_vowel_length_evidence`: 23
- `with_saltillo_evidence`: 10
- `with_morphology`: 12
- `with_conflicting_claims`: 3
- `with_unknown_fields`: 50
- `claims_total`: 129
- `attestations_total`: 98

As metas não bloqueadoras foram atingidas sem preencher dados por memória.

## Proveniência e direitos

O GDN está registrado como agregador B01 e cada Attestation conserva A01, A02
ou A04 como Source histórica. A03 foi avaliada no Witness Lock, mas não foi
necessária nos registros finais selecionados. Referências contextuais mantêm
somente metadados/IDs. Não houve uso de C01 nem cópia de componentes restritos
do Digital Florentine Codex.

## UNKNOWN e reservas

Todos os Lemmas contêm ao menos um `UNKNOWN` ou `NOT_REVIEWED`, principalmente
em `PEDAGOGICAL_FORM`, Locator interno, morfologia e interpretação fonológica.
Isso é intencional e impede falsa precisão.

Reservas:

1. o ambiente não possuía Python; foi instalado Python 3.13.15 oficial em
   escopo de usuário para executar o validador exigido;
2. o Locator de Olmos é verificável no nível da Edition digital GDN, mas o folio
   interno permanece `NOT_REVIEWED`;
3. as camadas modernas do GDN continuam `CAN_REFERENCE`/direitos não resolvidos;
4. as traduções PT-BR, conflitos e frames morfológicos permanecem `IN_REVIEW`;
5. nenhuma decisão fonética definitiva foi tomada a partir dos diacríticos.

## Conclusão

**PASS_WITH_RESERVATIONS**

Os invariantes bloqueadores e as metas quantitativas foram satisfeitos, mas o
piloto ainda exige revisão linguística humana e jurídica/editorial das camadas
referenciadas. Esta autoavaliação não aprova o Gate 3, não substitui o
`ORCHESTRATOR_REVIEWER` nem autoriza o Gate 4.

## EXTERNAL REVIEW REMEDIATION

`ORCHESTRATOR_REVIEWER_DECISION: PASS_AFTER_REMEDIATION`

`GATE_3_STATUS: CLOSED`

| Reserva | Ação | Resultado |
|---|---|---|
| Diferença semântica contada como contradição | Introduzida classificação estrutural de divergência | `with_conflicting_claims: 0` |
| `pilli` | `LEXICAL_IDENTITY_UNRESOLVED` | Sem escolha inventada entre polissemia e homonímia |
| `tlacatl` | `SOURCE_GRANULARITY_DIFFERENCE` | Incompatibilidade não presumida |
| `mati` | `FRAME_VARIATION` | Frames distintos preservados |
| Referência confundida com contexto textual | Separadas referência e inspeção | 47 referências; 0 textos inspecionados |
| Work histórica confundida com Witness direto | Adicionado `mediation_level` | 98 `AGGREGATOR`; 0 `DIRECT_WITNESS` |

Métricas finais recalculadas:

- `with_historical_attestation`: 50;
- `with_direct_witness_attestation`: 0;
- `with_aggregator_mediated_attestation`: 50;
- `with_context_reference`: 47;
- `with_context_text_inspected`: 0;
- `with_conflicting_claims`: 0;
- `with_semantic_variation`: 1;
- `with_frame_variation`: 1;
- `with_lexical_identity_unresolved`: 1;
- `attestations_by_mediation.AGGREGATOR`: 98.

O validador exige mediação em cada Attestation e impede que uma ocorrência
com agregador ou sem inspeção declarada seja chamada `DIRECT_WITNESS`. Um
`EvidenceLink` `CONTRADICTS` somente passa com avaliação estrutural explícita de
comparabilidade e `TRUE_CONTRADICTION`.

Resultado final: `GATE 3 VALIDATION: PASS`.

O encerramento não inicia nem autoriza o Gate 4.

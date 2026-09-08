# Gates de uso (direitos) e de variedade (Gate 5)

Executor: `EXECUTION_AGENT`. O Gate 5 permanece `IN_PROGRESS`. Este documento
cobre a decisão normativa de **quem pode ser usado como evidência de Náhuatl
Clássico** e qual o papel recomendado de cada fonte no registro.

## Classificação de uso por componente

A classe vem do registro canônico em `data/source_registry/*.yml`. O Rights
Gate resolve `source_id + component_id` para uma classe de uso:

| Classe | Significado |
|---|---|
| `CAN_INGEST_WITH_ATTRIBUTION` | Pode alimentar evidência, com citação verificável |
| `CAN_REFERENCE` | Apenas referência/consulta; não captura evidência |
| `MANUAL_PERMISSION_REQUIRED` | Requer permissão humana explícita antes de qualquer uso |
| `DO_NOT_INGEST` | Proibido (direitos não passíveis de resolução automática) |
| `RIGHTS_UNCLEAR` (estimado) | Cálculo a partir de campos acarreta incerteza registrada |

Cada `RightsRecord` expõe `computed_uses`, `needs_attribution`,
`storage_permission`, `redistribution_permission`, `recommended_role` e
`rationale`. O código `RIGHTS_UNCLEAR` é emitido quando o registro não tem
classe resolvível de forma inequívoca e `RIGHTS_PERMISSION` quando a classe
exige permissão manual ainda não declarada no fixture.

## Modernidade (Variety Gate)

`is_modern_source(entry)` avalia por campos estruturados
(`linguistic_features.modern_variety`, `linguistic_scope.variety/period`) —
**não** por heurísticas de string no nome da variedade. Fontes modernas
(C01 Hueyapan/2016, C02 INALI, C03 UCLA Mecayapan) alimentam apenas referência
cruzada e são rejeitadas como evidência clássica
(`MODERN_AS_CLASSICAL_EVIDENCE`). A variedade moderna nunca é usada para
preencher lacunas do Náhuatl Clássico; ausência de notação não prova ausência
de contraste (AGENTS.md §15).

## Mediação

`DIRECT_WITNESS` exige `direct_witness_inspected: true`
(`DIRECT_WITNESS_INSPECTION`). `AGGREGATOR` exige mediator declarado
(`AGGREGATOR_MEDIATION`). O rótulo de mediação nunca é confundido com tipo da
fonte nem com confiança.

## Fixtures de negação obrigatória

`scripts/validate_gate5.py` falha se qualquer negação deixa de ser exercitada:

| Código obrigatório | Fixture de referência |
|---|---|
| `RIGHTS_PERMISSION` | G5-009 (C01), G5-032 (C03) |
| `RIGHTS_DO_NOT_INGEST` | G5-010 (C01 `local_pdf_witness`) |
| `RIGHTS_UNCLEAR` | G5-011 (A03 `digital_surrogate`), G5-014 (B01), G5-020 (A03 `digital_surrogate`) |
| `RIGHTS_REFERENCE_ONLY` | G5-012 (C02), G5-013 |
| `MODERN_AS_CLASSICAL_EVIDENCE` | G5-009/010 (C01), G5-012 (C02), G5-014 (B01), G5-032 (C03) |

A cobertura C01/C02/C03 é verificada por `source_id` nas fixtures de REJECT com
`MODERN_AS_CLASSICAL_EVIDENCE`. Remover qualquer um desses casos quebra a
validação.

## Registro de decisões aplicadas

- C01: componentes didáticos e dicionário `MANUAL_PERMISSION_REQUIRED`;
  `local_pdf_witness` `DO_NOT_INGEST`.
- B01 (GDN): registros lexicais e paleografia `CAN_REFERENCE`; traduções/exemplos
  `RIGHTS_UNCLEAR`; variedade moderna (`modern_variety: true`).

Ver decisões abertas no relatório de auditoria (`docs/GATE_5_AUDIT_REPORT.md`).
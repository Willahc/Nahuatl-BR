# Estado dos Gates

Gate 0: PASS / CLOSED

Gate 1: PASS / CLOSED

Gate 2: PASS / CLOSED

Gate 3: PASS / CLOSED

Gate 4: PASS / CLOSED

Gate 5: PASS / CLOSED

Gate 6: IN_PROGRESS / SOURCE_EVIDENCE_PATH_RESOLVED

Gate 7: NOT_STARTED

## Registro do fechamento do Gate 5

- Gate 5 initial delivery: `c310429`
- Gate 5 search-policy remediation: `1f7c913`
- Gate 5 preview-label finalization: `40f1623`
- Orchestrator Reviewer: `PASS`
- Decisão externa registrada em 2026-09-10: `GATE_5_STATUS: CLOSED`,
  `PIPELINE_USE: APPROVED`, `RESEARCH_PREVIEW_0: APPROVED`,
  `PUBLIC_DEPLOYMENT: APPROVED`.
- Public Research Preview: https://willahc.github.io/Nahuatl-BR/
- Commit de fechamento: `docs: close Gate 5 ingestion pipeline`; a tag anotada
  `gate-5-approved` identifica exatamente esse commit após os workflows SUCCESS.

A aprovação abrange pipeline read-only/dry-run, Source resolution, Rights Gate,
Variety Gate, transformações governadas por policy, geração de candidatos DRAFT,
idempotência, exporter determinístico, Research Preview 0 e deployment estático
controlado. O Preview é produto derivado, não fonte canônica.

Não aprova automaticamente ingestão irrestrita, fontes RIGHTS_UNCLEAR,
Hueyapan, modern varieties como Classical, Claims individuais, IPA em massa,
áudio, scraping em massa ou conteúdo dos futuros 500 lemmas.

Gate approval != Claim publication. Os estados atuais são preservados: nenhuma
promoção DRAFT -> PUBLISHED ou IN_REVIEW -> PUBLISHED decorre deste fechamento.
Todos os critérios formais de saída foram satisfeitos conforme a decisão externa
registrada em `GATE_5_AUDIT_REPORT.md`. Reservas futuras não reabrem o Gate 5.
Gate 6 está autorizado, mas não foi iniciado nesta execução.

## Registro do fechamento do Gate 4

- Gate 4 delivery commit: `6588dd9`
- Gate 4 validation/audit commit: `419beed`
- Fechamento formal: commit "docs: close Gate 4 phonology model", marcado pela
  tag `gate-4-approved`
- Orchestrator Reviewer decision: `PASS / APPROVED FOR MODEL USE`
- Aprovação: `ORCHESTRATOR_REVIEWER_GATE_4_PASS`, registrada na policy
  `data/policies/classical_phonology_v1.yml` (`APPROVED`, v1.0.0).

A aprovação do Gate 4 aprova o **modelo fonológico** (framework de reconstrução
fonêmica e modelo de evidência ortografia→fonologia) para uso nos próximos
Gates. Ela não promove automaticamente Claims, fonética estreita, `/ʔ/`
pan-nahua, traduções/Claims linguísticas individuais nem Evidence mediada a
Witness direto.

### Reservas aceitas (não bloqueadoras, não reabrem o Gate)

- direct Witness inspection pendente;
- narrow phonetic realization pendente;
- regional/chronological refinement pendente;
- prosodic domains pendentes;
- expert individual Claim review pendente.

## Linha temporal de referência

Gate 3 final commit: `3995c2a` (Gate 3 `PASS_AFTER_REMEDIATION`; o hardening
posterior não reabre o Gate).

Gate 4: modelo, Claims, Evidence e fixtures entregues em `6588dd9`; validação,
testes, docs e auditoria em `419beed` (`GATE_4_AUDIT_REPORT.md`);
`PASS_WITH_RESERVATIONS` do EXECUTION_AGENT foi aceito pelo ORCHESTRATOR_REVIEWER
e o Gate foi encerrado com `PASS`.

`gate-3-approved` identifica exclusivamente o corpus aprovado antes do hardening:
`3995c2a10b2b66136c4819064c79d37ba580bfa5`. Não identifica tooling mais recente.

## Estado do conteúdo editorial

As 129 Claims do Gate 3 e as 29 Claims do Gate 4 (G4C001–G4C029) permanecem
`IN_REVIEW`, com revisão individual não documentada. Gate completion não
equivale a aprovação editorial individual. A policy fonológica é aprovada como
modelo; nenhuma Claim individual foi promovida a `PUBLISHED`.

Os 29 Claims fonológicos nascem `IN_REVIEW` por instrução explícita do
PRODUCT_OWNER (exceção registrada no AGENTS.md), com origem EXECUTION_AGENT
registrada. Revisão humana individual não está documentada.

Gate 5 está PASS / CLOSED por decisão externa. Pipeline e Research Preview 0
aprovados no escopo acima, sem promoção de Claims individuais.
Gate 6 está IN_PROGRESS / SOURCE_EVIDENCE_PATH_RESOLVED.
Gate 7 permanece NOT_STARTED.

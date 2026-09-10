# Gate 6 — Coverage report (checkpoint 01)

Data: 2026-09-10. Corpus atual: **100 lemmas** (50 baseline + 50 novos).
Meta final: 500; novos admitidos: 50/450. Este é um relatório de checkpoint,
não aprovação ou fechamento do Gate 6.

| Métrica | Valor |
|---|---:|
| historical attestation coverage | 100/100 |
| PT-BR editorial coverage | 100/100 |
| multi-source | 48 |
| single-source | 52 |
| attestations | 148 |
| Evidence | 148 |
| Claims | 229 (50 novas DRAFT; 29 Gate 4 permanecem IN_REVIEW) |
| context references | 47 |
| context directly inspected | 0 |
| vowel-length evidence | 23 (baseline; nenhum novo valor inferido) |
| saltillo evidence | 10 (baseline; nenhum novo valor inferido) |
| morphology coverage | 12 (baseline; novos NOT_REVIEWED) |
| duplicate candidates | 3; CANDIDATE_ONLY; automatic_merge false |
| semantic review candidates | 50 novos |
| rights blocks / modern-variety blocks | 0 admitidos; negativos cobertos nos fixtures |

Distribuição histórica: A01=99, A02=2, A04=47. Os 50 novos são A01
`jcb_1571_images`, um único Witness visual com mediação DIRECT_WITNESS; por isso
todos são SINGLE_SOURCE. A meta de ≥300 multi-source não é atingida neste
checkpoint e não será compensada por cópia de camadas restritas.

Domínios editoriais dos novos: animais 2, natureza 1, emoções 5, sociedade 1,
ações 1, trabalho 1, expressões 1, relações 6, tempo 3, pessoas 2, objetos 8,
comércio 3, cognição 2, quantidade 8 e alimentos 3. Classe lexical permanece
NOT_REVIEWED. Ver `data/gate6/coverage.json` para o retrato determinístico.

`BLOCKED_BY_SOURCE_EVIDENCE`: a expansão para os próximos lotes está pausada
nesta execução. Apenas 50 capturas foram visualmente inspecionadas e possuem
hash/locator arquivados fora do Git; não há base auditada suficiente para
admitir mais 400 sem nova captura manual e revisão de cada página. Completar
500 agora exigiria inventar dados ou tratar OCR/camada moderna como Evidence,
ambos proibidos.

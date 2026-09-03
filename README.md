# Nahuatl-BR

Plataforma brasileira de estudo de náhuatl, com núcleo em Náhuatl Clássico e
tratamento explicitamente separado e documentado de variantes modernas, como
Hueyapan.

Os Gates 0, 1, 2 e 3 estão encerrados. O Gate 3 foi encerrado como
`PASS_AFTER_REMEDIATION`; o Gate 4 permanece `NOT_STARTED`. Ainda não há banco de dados, ingestão,
API ou frontend.

## Princípios

- nenhuma afirmação linguística sem proveniência;
- grafia da fonte preservada e normalização armazenada separadamente;
- variantes, períodos e tradições editoriais nunca combinados silenciosamente;
- tradução PT-BR tratada como camada editorial independente;
- conflito e incerteza preservados, não apagados;
- evidência primária, fonte acadêmica, inferência e reconstrução distinguidas.

## Documentação inicial

- [`docs/00_VISAO_DO_PROJETO.md`](docs/00_VISAO_DO_PROJETO.md)
- [`docs/01_POLITICA_LINGUISTICA.md`](docs/01_POLITICA_LINGUISTICA.md)
- [`docs/02_MAPA_DE_FONTES.md`](docs/02_MAPA_DE_FONTES.md)
- [`docs/03_MODELO_CANONICO.md`](docs/03_MODELO_CANONICO.md)
- [`docs/04_POLITICA_DE_PROVENIENCIA.md`](docs/04_POLITICA_DE_PROVENIENCIA.md)
- [`docs/05_ROADMAP.md`](docs/05_ROADMAP.md)
- [`docs/06_GLOSSARIO_CANONICO.md`](docs/06_GLOSSARIO_CANONICO.md)
- [`docs/GATE_0_AUDIT_REPORT.md`](docs/GATE_0_AUDIT_REPORT.md)
- [`docs/07_GATE_1_SOURCE_AUDIT.md`](docs/07_GATE_1_SOURCE_AUDIT.md)
- [`docs/08_GATE_2_EDITORIAL_ORTHOGRAPHY.md`](docs/08_GATE_2_EDITORIAL_ORTHOGRAPHY.md)

## Estrutura reservada

- `data/`: futuros dados derivados e validados;
- `docs/`: decisões e políticas do projeto;
- `scripts/`: futuras ferramentas reprodutíveis;
- `sources/`: materiais-fonte, segregados por tipo/variante;
- `src/`: futura implementação;
- `tests/`: futuros testes e validações.

O PDF já presente em `sources/hueyapan/` não foi inspecionado, copiado nem
ingerido neste gate. Sua situação jurídica, conteúdo e adequação técnica
continuam pendentes do Gate 1.

## Estado

Consulte o [roadmap](docs/05_ROADMAP.md). O avanço de gate exige satisfazer os
critérios de saída documentados e autorização humana do `PRODUCT_OWNER`; a
existência de código ou uma autoavaliação do Codex não substitui revisão
linguística, jurídica ou de proveniência e nunca autoriza progressão.

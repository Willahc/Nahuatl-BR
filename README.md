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

- `data/`: registry, política ortográfica, fixtures e piloto de 50 lemmas;
- `docs/`: decisões e políticas do projeto;
- `scripts/`: validador e controles de integridade do piloto;
- `sources/`: materiais-fonte, segregados por tipo/variante;
- `src/`: futura implementação;
- `tests/`: testes regressivos isolados do validador.

C01 foi inspecionado no Gate 1 e está registrado em
`data/source_registry/C01_hueyapan_2016.yml`. O PDF local não é versionado;
seus direitos permanecem restritos ou sujeitos a autorização. Hueyapan não
fornece Evidence ao piloto clássico.

## Validação local

Com Python 3.13 e biblioteca padrão:

```text
python scripts/validate_gate3.py --check
python -m unittest discover -s tests -p "test_*.py"
```

O modo padrão é somente leitura e detecta derivados desatualizados.
`--write-derived` regenera índice/métricas somente após validar as entradas.
Consulte o [contrato de validação](docs/GATE_3_VALIDATION_POLICY.md) e a
[política de proveniência editorial](docs/EDITORIAL_PROVENANCE.md).

O piloto tem 129 Claims e 50 Translations em `IN_REVIEW`. O encerramento do
Gate 3 aprova a estrutura do piloto; não equivale à revisão individual por
especialista nem promove conteúdo a `APPROVED`/`PUBLISHED`.

## Estado

`PROJECT_LICENSE_STATUS: OPEN_DECISION`

A visibilidade PUBLIC no GitHub não concede uma licença aberta ao conteúdo
original. Nenhuma LICENSE foi criada; a decisão será tomada separadamente.
Fontes externas mantêm seus direitos. Consulte
[direitos e licenciamento](docs/RIGHTS_AND_LICENSING.md),
[reprodutibilidade](docs/11_REPOSITORY_REPRODUCIBILITY.md),
[status dos Gates](docs/GATE_STATUS.md) e
[manifest C01](manifests/external_sources/C01_hueyapan_2016.yml).

Consulte o [roadmap](docs/05_ROADMAP.md). O avanço de gate exige satisfazer os
critérios de saída documentados e autorização humana do `PRODUCT_OWNER`; a
existência de código ou uma autoavaliação do Codex não substitui revisão
linguística, jurídica ou de proveniência e nunca autoriza progressão.

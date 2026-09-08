# Reprodutibilidade do repositório

O repositório canônico pretendido é `https://github.com/Willahc/Nahuatl-BR`.
A branch de trabalho/publicação é `main`; seu histórico completo deve ser
preservado, sem squash, reinicialização ou force-push.

## Execução a partir de clone limpo

Requisitos: Git e Python 3.13. O validador e a suíte usam somente a biblioteca
padrão; não é necessário instalar pacotes ou adquirir fontes externas.

```text
git clone https://github.com/Willahc/Nahuatl-BR.git
cd Nahuatl-BR
python -B scripts/validate_gate3.py --check
python -B -m unittest discover -s tests -p "test_*.py"
git diff --exit-code
git status --short
```

`-B` evita bytecode local. O CI usa `PYTHONDONTWRITEBYTECODE=1` e executa
validador, regressões e `git diff --exit-code`, além de verificar que não
surgiram arquivos não rastreados. Push e pull_request disparam a validação.
Não há etapa de ingestão ou regeneração de derivados no CI.

## Artefatos e derivações

Os 50 arquivos de lemma, registry, policy, fixtures, scripts e testes são
suficientes. O conteúdo calculado do índice e métricas deve corresponder aos
arquivos versionados. Se estiver desatualizado, o check falha com
`DERIVED_DATA_OUT_OF_DATE` e não grava correções.

Somente uma regeneração explícita e autorizada usa:

```text
python scripts/validate_gate3.py --write-derived
```

Esse modo valida as entradas antes de escrever. Alterar valores linguísticos
para silenciar teste é proibido. Proveniência editorial e relações novas do
hardening são descritas em [GATE_3_HARDENING_REPORT.md](GATE_3_HARDENING_REPORT.md).

## Fontes excluídas e segurança

O PDF local C01 não faz parte do clone. Seu caminho e hash estão no
[manifest](../manifests/external_sources/C01_hueyapan_2016.yml); não é uma
dependência de teste. Nenhum áudio, imagem externa ou dado raw/staging é exigido.

Antes de publicação pública, executar `python scripts/audit_publication.py`.
A auditoria examina caminhos e conteúdo atual e todos os blobs únicos alcançáveis
por refs Git, com padrões de alto risco. Não imprime os valores candidatos;
qualquer candidato exige parada e revisão humana. O resultado é uma verificação
por padrões, não uma garantia universal de ausência de segredo ou de direitos.

As Actions são fixadas por SHA dos repositórios oficiais de
[checkout](https://github.com/actions/checkout) e
[setup-python](https://github.com/actions/setup-python), com permissão de leitura.
Gate 4 permanece NOT_STARTED.

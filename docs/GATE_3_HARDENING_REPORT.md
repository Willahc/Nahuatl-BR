# Hardening pré-publicação do Gate 3

Origem: auditoria independente apresentada na conversa do projeto, reproduzida
por mutações isoladas do validador no HEAD `3995c2a10b2b66136c4819064c79d37ba580bfa5`.
Executor: `EXECUTION_AGENT`. Este relatório não é aprovação de novo Gate.

`PRE_PUBLICATION_HARDENING: PASS`

Gate 3 continua PASS / CLOSED; Gate 4 continua NOT_STARTED.

## Regressões e causas corrigidas

| Caso | Lacuna anterior | Controle atual |
|---|---|---|
| T01 | Estado válido bastava sem suporte | EvidenceLink apropriado obrigatório fora de DRAFT/QUARANTINED |
| T02 | ID válido e busca textual por Hueyapan | Compatibilidade com linguistic_scope do registry |
| T03 | Referências de Form não resolvidas | Resolução tipada de Evidence |
| T04 | Conversão direta em set apagava duplicações | Duplicidades detectadas antes de indexar |
| T05 | Relações fora do vocabulário aceitas | Vocabulário fechado com quatro relações |
| T06 | NOT_REVIEWED não tratado como ausência | Justificativa explícita para Locator ausente/não revisado |
| T07 | Igualdade com qualquer atestação era suficiente | Cadeia Form → Evidence → Attestation específica |
| T08 | Existência do objeto contava como tradução | Texto obrigatório, não vazio nem whitespace |
| T09 | Perfil não era conferido | Perfil aprovado, versionado e aplicável |

O controle de IDs cobre lemma no corpus e classes locais referenciáveis. As
referências de tradução, morfologia, fonologia, divergência, Source, agregador
e Work também são verificadas. O contrato e os limites do leitor de metadados
estão em [GATE_3_VALIDATION_POLICY.md](GATE_3_VALIDATION_POLICY.md).

## Proveniência e preservação

Os 129 objetos Claim e 50 Translations mantêm `IN_REVIEW`. O histórico Git
confirma sua existência nesse estado no primeiro commit do piloto `f21b642`.
O novo `editorial_provenance` registra esse fato e a ausência de trajetória
anterior, sem inventar transição DRAFT → IN_REVIEW, revisor, timestamp editorial
individual ou versão histórica da ferramenta. Consulte
[EDITORIAL_PROVENANCE.md](EDITORIAL_PROVENANCE.md).

Foram acrescentados 98 vínculos Evidence.attestation_id, recuperados unicamente
por igualdade dos metadados já existentes. Uma comparação estruturada com o
commit aprovado, removendo apenas os campos novos, demonstrou igualdade de
todos os valores anteriores nos 50 arquivos. Índice e métricas aprovados não
mudaram: 50 lemmas, 129 Claims, 98 Attestations, todas mediadas por agregador.

## Alinhamento documental

README descreve corpus, ferramentas e inspeção C01 existentes. Markdown do
Gate 2 distingue status inicial DRAFT de status atual APPROVED e aponta para
o fechamento administrativo. A comparação Git `58c58e4..f21b642` demonstra que
a promoção do perfil não mudou regras de normalização: os 25 casos originais
foram documentados sob draft.1, não executados por um normalizador. As referências
foram migradas para 1.0.0 com justificativa; a fixture continua DRAFT, sem
inventar aprovação individual dos casos. O caso Olmos permanece preservado.

Roadmap distingue conclusão estrutural do Gate e aprovação editorial individual.
Relatórios históricos não foram reescritos; receberam remissão à manutenção atual.

## Validação e derivados

O modo padrão e `--check` são somente leitura. Derivados são calculados em memória;
divergência ou ausência gera `DERIVED_DATA_OUT_OF_DATE`. `--write-derived` só grava
após validar integralmente as entradas. Dados inválidos não sobrescrevem derivados.

A suíte `tests/test_gate3_validator.py` cobre T01–T09, controle positivo,
referências adicionais, todos os namespaces existentes, estados permitidos e
proibidos sem Evidence, drift, proveniência e ausência de gravação nas falhas.
As cópias são temporárias; nenhum teste modifica o piloto real.

Comandos de aceitação:

```text
python scripts/validate_gate3.py --check
python -m unittest discover -s tests -p "test_*.py"
git diff --check
```

Resultados: GATE 3 VALIDATION: PASS; 28 testes PASS, incluindo nove regressões
obrigatórias e controle positivo; diff sem erros. A primeira execução dos testes
adicionais expôs que a contagem 51 ocultava a categoria DUPLICATE_ID; a ordem do
diagnóstico foi corrigida e a suíte repetida.

A reprodução de aceitação usa os arquivos do índice Git em diretório temporário,
sem PDF, credenciais ou material externo, executando validador e suíte. O conteúdo
da árvore temporária deve permanecer idêntico após os comandos.

Resultado da reprodução: PASS com 99 arquivos do índice, 28 testes e nenhuma
mudança de bytes ou de inventário após execução, com bytecode Python desabilitado.

O PASS de hardening se limita a essas verificações estruturais e operacionais;
não é revisão linguística individual, parecer jurídico ou autorização do Gate 4.

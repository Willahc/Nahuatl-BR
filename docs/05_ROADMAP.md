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
correção sem apagar o histórico. Este repositório está no **Gate 0**; este
documento não autoriza iniciar o Gate 1.

## GATE 0 — Governança e arquitetura

**Objetivo:** estabelecer missão, políticas, modelo conceitual, fontes
candidatas, responsabilidades e progressão.

**Entregáveis:** documentação inicial, instruções do repositório e inventário da
estrutura existente.

**Saída:** recomendação documentada do `ORCHESTRATOR_REVIEWER` e decisão
explícita do `PRODUCT_OWNER`; papéis de Gate formalizados; decisões críticas
abertas registradas; confirmação de que não houve ingestão, implementação de
banco ou frontend. Autoavaliação do `EXECUTION_AGENT` não satisfaz a decisão.

## GATE 1 — Auditoria jurídica/técnica das fontes

**Objetivo:** avaliar individualmente identidade, direitos, adequação
linguística, granularidade, qualidade e meios legítimos de acesso das fontes.

**Entregáveis:** ficha e evidências por fonte/edição; matriz de permissões e
restrições; política de armazenamento; decisão de uso; auditoria específica do
PDF local de Hueyapan, sem misturá-lo ao núcleo clássico.

**Saída:** conjunto mínimo de fontes clássicas aprovado para o piloto; métodos
de obtenção autorizados e reprodutíveis; riscos e fontes recusadas documentados.

## GATE 2 — Corpus piloto de 50 lemmas clássicos

**Objetivo:** testar o modelo com 50 lemmas de Náhuatl Clássico, selecionados por
critérios documentados, sem incorporar variantes modernas.

**Entregáveis:** amostra com formas originais, normalizações separadas, sentidos,
traduções PT-BR revisadas e proveniência granular; relatório de conflitos,
lacunas, tempo de curadoria e mudanças propostas ao modelo.

**Saída:** 50 lemmas auditados por revisão linguística e editorial; amostra de
citações reconferida; zero mistura silenciosa de variante; modelo conceitual
ajustado e aprovado.

## GATE 3 — Modelo fonológico

**Objetivo:** definir representação responsável de IPA, duração vocálica,
saltillo, sílabas, acento e tipos de pronúncia.

**Entregáveis:** convenções versionadas; representação de incerteza e
alternativas; critérios para atestação versus reconstrução; casos de teste
clássicos e, separadamente, por variante moderna quando autorizada.

**Saída:** revisão especializada; nenhuma derivação ortográfica não declarada;
componentes fonológicos rastreáveis e validados em amostra.

## GATE 4 — Pipeline de ingestão

**Objetivo:** implementar ingestão reprodutível sem destruir o original ou a
proveniência.

**Entregáveis:** formatos intermediários, validadores, logs, hashes, versionamento,
quarentena e revisão humana; testes contra duplicação, conflito e cruzamento de
variantes.

**Saída:** execução repetível sobre fontes autorizadas; auditoria entrada-saída;
falhas seguras; documentação operacional e testes aprovados.

## GATE 5 — Base canônica de 500 lemmas

**Objetivo:** ampliar o núcleo clássico curado mantendo os padrões do piloto.

**Entregáveis:** 500 lemmas, cobertura e lacunas mensuradas, traduções revisadas,
relatório de qualidade, conflitos e proveniência.

**Saída:** amostragem independente aprovada; integridade referencial e de
variante validada; metas mínimas de completude definidas por campo, sem fabricar
dados ausentes.

## GATE 6 — API

**Objetivo:** oferecer acesso estável e rastreável à base aprovada.

**Entregáveis:** contrato versionado, filtros obrigatórios de variante/período,
paginação, proveniência, licenças, estados de revisão, autenticação quando
necessária, observabilidade e documentação.

**Saída:** testes de contrato, segurança, desempenho e prevenção de mistura;
política de versões e depreciação aprovada.

## GATE 7 — Interface de dicionário

**Objetivo:** apresentar consulta lexical sem ocultar original, variante,
incerteza, conflito ou fonte.

**Entregáveis:** pesquisa, verbetes, filtros, citações, acessibilidade e desenho
responsivo; separação visual inequívoca entre clássico e variantes modernas.

**Saída:** testes de usabilidade e acessibilidade; auditoria de fidelidade entre
API e tela; revisão linguística da apresentação.

## GATE 8 — Sistema de estudo

**Objetivo:** criar atividades baseadas apenas em dados aprovados e adequadas ao
nível do estudante.

**Entregáveis:** modelo pedagógico, exercícios, revisão espaçada, feedback,
progresso e indicação permanente de variante/fonte.

**Saída:** revisão pedagógica; métricas de aprendizagem e privacidade definidas;
conteúdo gerado ou autoral claramente distinguido de atestação.

## GATE 9 — Áudio e treino de pronúncia

**Objetivo:** associar áudio e prática de pronúncia com classificação,
consentimento e limites epistêmicos claros.

**Entregáveis:** fluxo de gravação/curadoria, tipos obrigatórios, metadados de
falante e variante, gestão de consentimento/licença e experiência de treino.

**Saída:** revisão fonética e comunitária aplicável; rastreabilidade integral;
nenhum áudio sintético ou reconstruído apresentado como fala nativa.

## GATE 10 — Corpus histórico e leitura assistida

**Objetivo:** permitir leitura contextualizada de textos históricos preservando
estrutura documental e camadas editoriais.

**Entregáveis:** passagens, fac-símiles quando permitidos, transcrição,
normalização, análise, tradução e ligação lexical em camadas alternáveis.

**Saída:** citação em granularidade adequada; direitos por item verificados;
amostra comparada ao original; interfaces não confundem texto e intervenção.

## GATE 11 — Escrita glífica

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
- convenção ou convenções de normalização e política de lematização;
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

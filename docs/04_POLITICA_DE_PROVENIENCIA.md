# Política de proveniência

## Finalidade

Toda afirmação linguística deve permitir responder: quem afirmou, o quê, sobre
qual forma/variante/período, com base em qual evidência, onde ela pode ser
verificada, quando foi registrada ou revisada, sob quais direitos e com qual
grau de certeza.

## Unidade de proveniência

A proveniência é registrada no nível da afirmação. Uma referência anexada ao
verbete inteiro é insuficiente quando tradução, classe, morfologia, IPA ou
etimologia vêm de bases diferentes. Campos compostos, como uma transcrição IPA,
devem permitir apoio por componente quando as evidências divergirem.

## Cadeia mínima

Uma afirmação publicável deve conter:

- identificador estável e versão;
- sujeito e conteúdo exato da afirmação;
- variante e período aplicáveis;
- modalidade epistêmica da Claim: `OBSERVED`, `REPORTED`, `INFERRED`,
  `RECONSTRUCTED` ou `EDITORIAL`;
- fonte/afirmação de origem e localização verificável;
- agente responsável pela captura ou análise;
- data e método de produção;
- avaliação de confiança segundo rubrica versionada;
- estado de revisão;
- situação de licença/uso do material subjacente.

Quando algum elemento não existir, registra-se o motivo e restringe-se a
publicação. “Sem página” não autoriza fabricar página; usa-se o localizador mais
preciso que a fonte realmente oferece.

## Dimensões epistêmicas separadas

A modalidade epistêmica pertence à Claim. `OBSERVED`, `REPORTED`, `INFERRED`,
`RECONSTRUCTED` e `EDITORIAL` descrevem como seu conteúdo foi produzido.
Evidence Link registra somente `SUPPORTS`, `CONTRADICTS`, `QUALIFIES` ou
`DERIVED_FROM`. Modalidade epistêmica, tipo da Source, Confidence e estado
editorial são dimensões diferentes e nenhuma delas converte automaticamente o
conteúdo em verdade.

Evidence primária registra o que está diretamente no documento, inscrição ou
Recording; Source acadêmica registra análise atribuída; Inference e
Reconstruction explicitam premissas e método. IA não é Source linguística
primária.

## Citação e localização

Referências bibliográficas devem identificar obra e edição/versão. Localizadores
podem incluir página, fólio e lado, livro/capítulo, coluna, entrada, linha,
timestamp, identificador persistente ou região de imagem. A citação exibida e o
seletor estruturado devem coexistir. Citações indiretas devem manter a cadeia
“consultado em” e não fingir consulta ao original.

## Preservação e derivação

Materiais-fonte admitidos futuramente serão preservados sem modificação quando
legalmente permitido. Para cada arquivo ou resposta capturada deverão constar:

- origem e data de aquisição;
- identificador/URL e versão;
- hash criptográfico e tamanho;
- licença/termos vigentes ou estado desconhecido;
- ferramenta e versão usadas em cada transformação;
- parâmetros, data, entradas e saídas da transformação;
- revisão humana aplicada.

OCR, transcrição, correção, expansão, normalização, tradução e análise são
etapas distintas. Um derivado nunca será apresentado como fac-símile.

## Correções e conflitos

Correções criam nova versão e evento de revisão, mantendo o valor anterior,
autor, justificativa e evidência. Afirmações conflitantes recebem relações de
contradição ou alternativa; não são deduplicadas apenas porque compartilham o
mesmo sujeito. Uma escolha editorial preferencial é outra afirmação auditável.

## Traduções PT-BR

Cada tradução informa texto-base, tradutor, revisores, versão, data, decisões
terminológicas, licença e estado. Tradução intermediada por outro idioma deve
declarar essa cadeia. Tradução automática, se algum dia permitida, deverá ser
rotulada com sistema/versão e não poderá ser publicada como revisão humana.

## Áudio, falantes e direitos

Para cada Recording devem ser avaliados separadamente: Provenance; identidade e
Variety do Speaker quando legal e apropriado; consentimento de coleta; License;
copyright e direitos conexos; direitos de armazenamento, reprodução e
redistribuição; restrições comunitárias/culturais; e direito de retirada, quando
aplicável. Consentimento não é automaticamente necessário nem suficiente para
todo áudio externo. Metadados sensíveis não devem ser expostos só por ajudarem
tecnicamente a busca.

O tipo é `HUMAN_NATIVE`, `MODERN_READING`, `HISTORICAL_RECONSTRUCTION` ou
`SYNTHETIC`. Uma leitura moderna nunca é rotulada como gravação histórica de
Náhuatl Clássico.

## Confiança e revisão

Confidence usa provisoriamente `UNASSESSED`, `LOW`, `MEDIUM` e `HIGH`. Não é
verdade/falsidade, modalidade epistêmica, qualidade da Source ou estado
editorial, e não compensa Provenance ausente. A rubrica matemática definitiva é
`OPEN_DECISION` até validação após o corpus piloto.

Estados editoriais iniciais: `DRAFT`, `IN_REVIEW`, `APPROVED`, `PUBLISHED`,
`QUARANTINED`, `REJECTED` e `DEPRECATED`. `APPROVED`/`PUBLISHED` não equivalem a
`HIGH` Confidence; incerteza explícita pode ser publicada.

Uma Claim sem Evidence só pode estar `DRAFT` ou `QUARANTINED`. Se sua classe
exigir Evidence, ela não pode ser `PUBLISHED` nem canônica sem satisfazer essa
exigência. Claims geradas ou sugeridas por IA nascem como `DRAFT`, com origem
registrada, e nunca como fato linguístico.

Ausência de valor usa `UNKNOWN`, `NOT_APPLICABLE`, `NOT_REVIEWED` ou
`NOT_ATTESTED`. String vazia, `-`, `N/A` e `NULL` técnico isolado não podem
determinar indiscriminadamente esses significados.

## Auditoria

Auditorias devem conseguir reconstruir a cadeia completa sem depender da
interface. Exportações futuras incluirão identificadores, versões e
proveniência compatível com os direitos aplicáveis. Amostras serão verificadas
contra a fonte e revisões registrarão taxa e tipo de erro; métricas não
substituem inspeção linguística.

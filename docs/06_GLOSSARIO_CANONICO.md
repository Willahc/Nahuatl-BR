# Glossário canônico

## Status e uso

Este glossário fixa o vocabulário conceitual do Gate 0. Termos em inglês são os
nomes canônicos das entidades e valores; a explicação em português orienta o
uso editorial. `PROVISIONAL` indica uma definição suficiente para governança,
mas dependente de validação posterior. Não implica decisão de esquema físico.

## Objetos linguísticos

### Lemma — PROVISIONAL

Unidade editorial usada para organizar consulta e relacionar Forms, Senses e
Claims dentro de uma Variety e escopo temporal declarados. Não é sinônimo de
uma ocorrência textual nem apaga homônimos ou variação. O algoritmo de
lematização é `OPEN_DECISION`.

### Form — PROVISIONAL

Representação linguística identificável tratada pelo projeto. É um termo geral;
seu subtipo e relação com uma Attestation devem ser explícitos. Não autoriza
atribuição automática de pronúncia, morfologia, sentido ou variante.

### Historical Form — PROVISIONAL

Form registrada ou atribuída a contexto histórico definido, preservando a
grafia/transcrição pertinente e ligada a Evidence. “Historical” descreve o
contexto temporal, não certifica autenticidade nem reconstrução.

### Normalized Form — PROVISIONAL

Representação derivada de outra Form segundo convenção identificada e
versionada. Coexiste com o original e nunca o substitui. A convenção definitiva
é `OPEN_DECISION`.

### Sense — PROVISIONAL

Aceção editorial proposta para um Lemma em escopo declarado. Polissemia e
análises concorrentes permanecem separadas e sustentadas por Claims.

### Attestation

Registro de que determinada Form ou conteúdo ocorre em um Witness, com Locator
e transcrição verificável. Attestation é ocorrência documentada; não é, por si
só, análise linguística nem garantia de interpretação correta.

### Variety — PROVISIONAL

Identidade controlada de uma variedade linguística à qual dados e Claims são
atribuídos. Pode incluir nomes, localidade, comunidade e período documentados.
Sua taxonomia definitiva depende de fontes ainda não auditadas.

### Classical Nahuatl — PROVISIONAL

Variety ou conjunto histórico de variedades que constitui o núcleo inicial do
projeto, sempre com período, proveniência e convenção explicitados. Sua
delimitação linguística definitiva é `OPEN_DECISION`; o rótulo não permite
absorver dados de Modern Varieties.

### Modern Variety — PROVISIONAL

Variety contemporânea ou de período moderno identificada separadamente, como
Hueyapan. Não herda nem fornece automaticamente Forms, análises ou pronúncias
ao Classical Nahuatl.

### Morphological Analysis — PROVISIONAL

Claim estruturada sobre segmentação, morfemas, funções e relações morfológicas
de uma Form segundo abordagem declarada. A ontologia morfológica completa é
`OPEN_DECISION`.

### Phonological Analysis — PROVISIONAL

Conjunto ou estrutura de Claims sobre propriedades fonológicas ou fonéticas de
uma Form, como IPA, duração vocálica, saltillo, sílabas e acento. Cada componente
mantém Provenance adequada; o IPA completo do Classical Nahuatl é
`OPEN_DECISION`.

### Reconstruction

Resultado de método explícito que propõe uma forma, propriedade ou pronúncia
não diretamente observada. Deve ser representado por Claim com modalidade
`RECONSTRUCTED`, método, premissas e Evidence.

### Inference

Conclusão analítica derivada de premissas e Evidence declaradas, representada
por Claim com modalidade `INFERRED`. Não é Attestation nem Reconstruction.

## Afirmações e conhecimento

### Claim

Proposição versionável e auditável sobre um sujeito. Contém conteúdo, escopo de
Variety/período quando aplicável, modalidade epistêmica, Confidence, estado
editorial, responsável e Provenance. Modalidade, tipo de Source, Confidence e
estado editorial são dimensões independentes.

### Evidence

Objeto verificável usado para apoiar, contradizer, qualificar ou servir de base
a uma Claim. Pode remeter a Attestation, Source/Locator ou outra Claim. Seu tipo
não determina automaticamente modalidade ou Confidence.

### Evidence Link

Vínculo dirigido entre Claim e Evidence. Registra exclusivamente a relação de
suporte inicial `SUPPORTS`, `CONTRADICTS`, `QUALIFIES` ou `DERIVED_FROM`, além de
responsável, data e notas necessárias. Não duplica a modalidade epistêmica.

### Modalidade epistêmica da Claim

Caracteriza como o conteúdo da Claim foi epistemicamente produzido:

- `OBSERVED`: transcrição ou observação direta declarada de Evidence;
- `REPORTED`: conteúdo atribuído a uma Source ou Agent identificado;
- `INFERRED`: conclusão analítica derivada de premissas declaradas;
- `RECONSTRUCTED`: resultado de reconstrução por método explícito;
- `EDITORIAL`: decisão ou conteúdo editorial do projeto, incluindo organização
  e Editorial Translation quando aplicável.

### Confidence — PROVISIONAL

Avaliação editorial da sustentação de uma Claim: `UNASSESSED`, `LOW`, `MEDIUM`
ou `HIGH`. Não representa verdade/falsidade, modalidade epistêmica, qualidade
da Source ou estado editorial. A rubrica matemática definitiva será validada
após o corpus piloto e permanece `OPEN_DECISION`.

### Estados editoriais

Estado de fluxo de uma Claim ou objeto editorial:

- `DRAFT`: em elaboração, ainda não aprovado;
- `IN_REVIEW`: submetido à revisão competente;
- `APPROVED`: aprovado no fluxo interno, ainda não necessariamente publicado;
- `PUBLISHED`: disponibilizado no produto ou release aplicável;
- `QUARANTINED`: isolado por insuficiência, risco ou anomalia que impede uso
  normal;
- `REJECTED`: avaliado e recusado, preservando histórico;
- `DEPRECATED`: anteriormente aceito ou publicado, mas substituído ou
  desaconselhado, preservando histórico.

`APPROVED` e `PUBLISHED` não significam `HIGH` Confidence. Uma Claim pode ser
publicada como incerta se a incerteza estiver explícita e as demais regras
forem satisfeitas.

### Ausência de valor

Estados semânticos controlados:

- `UNKNOWN`: existe uma pergunta aplicável, mas o valor é desconhecido;
- `NOT_APPLICABLE`: o campo/conceito não se aplica ao objeto;
- `NOT_REVIEWED`: ainda não houve revisão para determinar o valor;
- `NOT_ATTESTED`: não foi encontrada Attestation dentro do corpus e método de
  busca declarados; não significa inexistência absoluta.

String vazia, `-`, `N/A` ou equivalentes não podem representar
indiscriminadamente esses estados. `NULL` técnico, isoladamente, não determina
qual significado se aplica.

### Política de Claim sem Evidence

Uma Claim pode existir sem Evidence apenas como `DRAFT` ou `QUARANTINED`. Se a
política de sua classe exigir Evidence, ela não pode tornar-se `PUBLISHED` nem
canônica enquanto a exigência não for satisfeita. Claims geradas ou sugeridas
por IA nascem como `DRAFT`, registram sistema, versão e contexto de origem e
nunca são tratadas como fato linguístico. IA não é Source linguística primária.

### Provenance

Histórico verificável da origem, autoria, método, Evidence, transformações,
versões, datas, direitos e revisão de um objeto ou Claim. Deve permitir
reconstruir como o conteúdo chegou ao estado atual.

## Fontes e localização

### Source

Termo geral para recurso consultado ou referenciado. Deve ser especializado ou
descrito quanto ao tipo; o tipo da Source não é modalidade epistêmica.

### Work

Conteúdo intelectual ou criação abstrata atribuída a autorias e contexto, em
distinção de Edition e Witness. Exemplo de uso conceitual: uma obra gramatical,
sem decidir neste Gate qual edição utilizar.

### Edition — PROVISIONAL

Realização editorial identificada de uma Work, incluindo edição impressa,
crítica ou digital conforme o caso. Suas intervenções, responsáveis, data e
direitos podem diferir dos da Work.

### Witness — PROVISIONAL

Manifestação ou exemplar específico pelo qual conteúdo é atestado ou
consultado, como manuscrito, exemplar físico, imagem ou arquivo identificado.
Sua aplicação exata por classe de Source será validada posteriormente.

### Locator

Endereço verificável dentro de Source, Edition ou Witness: página, fólio/lado,
coluna, linha, entrada, timestamp, região de imagem, identificador persistente
ou combinação apropriada. Deve registrar precisão e incerteza quando necessário.

### Corpus — PROVISIONAL

Coleção delimitada de materiais ou passagens com critérios, versões, direitos e
política documentados. Uma ausência em Corpus não prova ausência na língua.

## Tradução

### Translation

Relação ou produto textual que representa conteúdo em outro idioma, preservando
idiomas de origem/destino, texto-base, autoria, versão e Provenance.

### Editorial Translation

Translation produzida ou adotada pela equipe editorial, inclusive PT-BR. É uma
Claim `EDITORIAL`, independente de glosas históricas e versionada com tradutor,
revisor, data e Evidence usada.

## Áudio e agentes

### Speaker

Agent humano cuja fala aparece em Recording. Identidade e Variety são
registradas apenas quando legal, apropriado e compatível com direitos,
privacidade e restrições comunitárias; anonimização ou pseudonimização pode ser
necessária.

### Recording

Objeto de áudio identificado com Provenance própria. Seu tipo de pronúncia é
obrigatoriamente `HUMAN_NATIVE`, `MODERN_READING`,
`HISTORICAL_RECONSTRUCTION` ou `SYNTHETIC`. Uma leitura moderna de texto
clássico é `MODERN_READING`, nunca gravação histórica de Classical Nahuatl.

Para Recording devem ser avaliadas separadamente: Provenance; identidade e
Variety do Speaker quando legal e apropriado; consentimento de coleta; License;
copyright e direitos conexos; direito de armazenamento; direito de reprodução;
direito de redistribuição; restrições comunitárias/culturais; e direito de
retirada, quando aplicável. Consentimento não é automaticamente necessário nem
suficiente para todo áudio externo; a base jurídica e os direitos de cada item
precisam ser auditados.

## Direitos

### License

Instrumento ou declaração identificada que concede permissões sob condições.
Deve ser ligada ao objeto e versão corretos; não se presume que cubra Work,
Edition, Witness, dados e Recording da mesma maneira.

### Rights Status — PROVISIONAL

Avaliação documentada do que se sabe sobre titularidade, License, permissões,
restrições e usos pretendidos de um objeto. `UNKNOWN` não significa domínio
público nem autorização. Vocabulário operacional definitivo depende da
auditoria jurídica do Gate 1.

## OPEN_DECISION

Permanecem explicitamente abertas e não devem ser resolvidas no Gate 0:

- tecnologia de banco;
- cardinalidades físicas definitivas;
- formato definitivo de intercâmbio;
- ontologia morfológica completa;
- IPA completo do Classical Nahuatl;
- edição definitiva de Molina, Olmos, Rincón ou Carochi;
- License das Sources ainda não auditadas;
- rubrica matemática de Confidence;
- algoritmo de lematização;
- corpus definitivo de 50 Lemmas.

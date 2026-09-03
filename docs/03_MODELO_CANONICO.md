# Modelo canônico conceitual

## Objetivo e limites

Este documento propõe entidades e relacionamentos lógicos. Não define banco,
DDL, formato de arquivo, API nem tecnologia. O princípio central é separar o
objeto linguístico da afirmação sobre ele e ligar cada afirmação à proveniência.

## Visão relacional

```text
LanguageVariety ──< FormAttestation >── SourceLocator ── SourceWork
       │                  │                    │              │
       │                  ├── CorpusPassage ───┘              └── Agent
       │                  │
       └──< Lemma ──< Sense ──< Translation
               │        │
               ├──< FormLink
               └──< LinguisticAssertion >── EvidenceLink ── SourceLocator
                          │
                          ├── MorphologicalAnalysis ──< MorphemeOccurrence >── Morpheme
                          ├── PhonologicalAnalysis
                          ├── GrammaticalClassification
                          └── RelationAssertion

FormAttestation/CorpusPassage ──< Example
FormAttestation/Lemma ──< AudioRecording >── Speaker
Qualquer entidade versionável ──< RevisionEvent >── Agent
```

As cardinalidades e agregados serão refinados no corpus piloto.

## Entidades nucleares

### `LanguageVariety`

Identidade controlada da variedade: nome preferido, nomes alternativos, código
externo quando verificável, localidade, comunidade, período de validade e notas.
Náhuatl Clássico e Hueyapan serão registros distintos. Relações genealógicas ou
comparativas são explícitas, não herança automática de dados.

### `HistoricalPeriod`

Recorte temporal versionado, com início/fim exatos ou aproximados, critério e
fonte. Pode qualificar variedade, obra, passagem, forma ou afirmação.

### `Lemma`

Unidade editorial de acesso associada a uma única variedade principal e ao
escopo temporal pertinente. Contém identificador estável e rótulo editorial,
mas não incorpora silenciosamente todas as formas parecidas. Homônimos podem
ser lemmas separados; a política definitiva de lematização segue aberta.

### `FormAttestation`

Ocorrência ou forma registrada por uma fonte. Campos conceituais: transcrição
original, variedade atribuída, período, localização na fonte, método e
responsável pela transcrição. Repetições podem permanecer ocorrências distintas.

### `NormalizedForm`

Representação derivada de uma forma atestada: valor, convenção/versionamento,
operações aplicadas, responsável, data e confiança. Uma atestação admite várias
normalizações concorrentes.

### `FormLink`

Liga lemma e forma atestada, indicando papel (forma de citação, flexionada,
variante gráfica etc.), autor da ligação, confiança e evidência. Não presume
identidade apenas por comparação de texto.

### `Sense`

Aceção editorial ligada a um lemma e variedade, com definição controlada,
escopo, relações semânticas e estado de revisão. Divergências podem gerar
sentidos paralelos ou afirmações concorrentes.

### `Translation`

Camada editorial ligada a um sentido, exemplo ou passagem: idioma de destino
(`pt-BR` inicialmente), texto, tradutor, revisor, versão, data, fonte-base,
notas, confiança e estado. Não substitui a glosa original da fonte.

### `LinguisticAssertion`

Superentidade para uma proposição auditável. Contém sujeito, predicado/tipo,
valor ou objeto, variedade, período, modalidade epistêmica, confiança, estado,
responsável e datas. Exemplos: “forma X tem classe Y”, “segmento é raiz”, “IPA é
Z”. Cada afirmação possui ao menos uma justificativa ou é explicitamente
marcada como ainda sem suporte e impedida de publicação.

### `GrammaticalClassification`

Afirmação de classe e subclasse gramatical segundo um vocabulário/sistema
identificado e versionado.

### `MorphologicalAnalysis`

Análise de uma forma específica segundo uma teoria ou referência. Mantém
segmentação, fronteiras, glossas funcionais e confiança. Duas análises não são
mescladas.

### `Morpheme` e `MorphemeOccurrence`

`Morpheme` representa uma unidade analítica proposta (prefixo, raiz, sufixo ou
outro tipo controlado). `MorphemeOccurrence` representa seu segmento, ordem e
função numa análise particular. A categoria e a identidade são afirmações com
proveniência, não deduções da posição gráfica.

### `PhonologicalAnalysis`

Agrupa, sem tornar obrigatórios, IPA, duração vocálica por segmento, saltillo,
divisão silábica e acentuação. Declara variedade, nível (fonêmico/fonético, a
refinar), método, sistema de símbolos, fonte ou base reconstrutiva e confiança.
Cada componente deve poder ter proveniência própria.

### `Corpus` e `CorpusPassage`

`Corpus` identifica uma coleção e sua política. `CorpusPassage` preserva trecho
original, estrutura e localização (página, fólio, coluna, linha ou identificador
equivalente). Normalização, tradução e anotação são camadas relacionadas.

### `Example`

Associação de um lemma/sentido a uma passagem ou exemplo pedagógico. Registra o
tipo e a justificativa. Uma passagem histórica não é alterada para servir ao
lemma.

## Fontes, agentes e direitos

### `SourceWork`, `SourceExpression` e `SourceItem`

Separam, conceitualmente, obra (conteúdo intelectual), edição/transcrição ou
versão, e exemplar/arquivo concreto. Campos incluem título, autoria, datas,
identificadores, idioma, variante alegada e notas bibliográficas. Essa separação
evita citar “Molina”, por exemplo, sem determinar edição e página.

### `SourceLocator`

Endereço interno a uma fonte: entrada, página, fólio, lado, coluna, linha,
timestamp, região de imagem ou outro seletor. Mantém a citação humana e o
seletor estruturado; pode registrar nível de precisão e incerteza.

### `Agent`

Pessoa, comunidade, organização ou software, com papéis contextuais: autor,
editor, transcritor, tradutor, revisor, falante, depositante ou importador.
Dados pessoais devem ser mínimos e governados pela base jurídica e pelos
direitos aplicáveis; consentimento é uma possibilidade, não pressuposto único.

### `LicenseAssessment`

Registra texto/identificador da licença ou termos, jurisdição quando relevante,
URL/evidência, titular, data de verificação, avaliador e permissões/restrições
separadas. “Desconhecida” é um estado válido; não equivale a domínio público.

### `EvidenceLink`

Relaciona uma Claim a Evidence com relação `SUPPORTS`, `CONTRADICTS`,
`QUALIFIES` ou `DERIVED_FROM`, trecho mínimo de apoio quando aplicável,
responsável e data. A cadeia deve chegar a Evidence auditável. O vínculo não
duplica a modalidade epistêmica da Claim.

## Modalidade, confiança e revisão

### Modalidade epistêmica da `Claim`

A modalidade pertence à Claim e usa `OBSERVED`, `REPORTED`, `INFERRED`,
`RECONSTRUCTED` ou `EDITORIAL`. Ela descreve como o conteúdo foi produzido e
não o tipo da Source. Evidence Link registra apenas a relação de suporte. A
modalidade epistêmica, o tipo da Source, Confidence e o estado editorial são
dimensões independentes.

### `ConfidenceAssessment`

Avaliação separada da Claim: `UNASSESSED`, `LOW`, `MEDIUM` ou `HIGH`, além de
rubrica/versionamento, avaliador, data e justificativa. Confidence não significa
verdade/falsidade, modalidade epistêmica, qualidade da Source ou estado
editorial. A rubrica matemática definitiva é `OPEN_DECISION` e será validada
após o corpus piloto.

### Estado editorial e ausência de Evidence

Vocabulário inicial: `DRAFT`, `IN_REVIEW`, `APPROVED`, `PUBLISHED`,
`QUARANTINED`, `REJECTED` e `DEPRECATED`. `APPROVED`/`PUBLISHED` não equivalem a
`HIGH` Confidence; uma Claim pode ser publicada como incerta quando a incerteza
estiver explícita.

Uma Claim sem Evidence só pode existir como `DRAFT` ou `QUARANTINED`. Quando a
política de sua classe exigir Evidence, não pode tornar-se `PUBLISHED` nem
canônica até satisfazer a exigência. Claims geradas ou sugeridas por IA nascem
como `DRAFT`, registram a origem e nunca constituem fato ou Source linguística
primária.

### Ausência de valor

Usam-se `UNKNOWN`, `NOT_APPLICABLE`, `NOT_REVIEWED` e `NOT_ATTESTED`. String
vazia, `-`, `N/A` ou equivalentes são proibidos como marcadores semânticos
indiscriminados; `NULL` técnico isolado não determina qual estado se aplica.

### `RevisionEvent`

Histórico imutável de criação, alteração, revisão, aprovação, rejeição ou
descontinuação, com agente, data, justificativa e referências às versões.
Registros não são apagados para ocultar conflito; podem ser despublicados sem
perder a trilha.

## Áudio

### `Speaker`

Agent humano com metadados estritamente necessários, incluindo relação
declarada com uma `LanguageVariety` quando legal e apropriado. Identidade
pública, anonimização e pseudonimização dependem da base jurídica, direitos e
restrições aplicáveis, não apenas de consentimento.

### `AudioRecording`

Arquivo/objeto, conteúdo pronunciado, Speaker (quando humano), Variety do
Speaker, Variety do item, contexto, data, equipamento/metodologia quando
relevante e tipo obrigatório:

`HUMAN_NATIVE`, `MODERN_READING`, `HISTORICAL_RECONSTRUCTION` ou `SYNTHETIC`.

Para sintético, registram-se sistema/modelo e versão; para reconstrução,
registram-se método e Evidence. Uma leitura moderna de texto clássico é
`MODERN_READING`, nunca gravação histórica de Classical Nahuatl. Arquivo,
recorte e associação ao Lemma/Forms são objetos distintos.

Devem ser avaliados separadamente: Provenance da Recording; identidade e
Variety do Speaker quando legal e apropriado; consentimento de coleta; License;
copyright e direitos conexos; direitos de armazenamento, reprodução e
redistribuição; restrições comunitárias/culturais; e direito de retirada, quando
aplicável. Consentimento não é automaticamente necessário nem suficiente para
todo áudio externo.

## Restrições de integridade conceituais

1. Uma atestação tem exatamente uma variedade atribuída ou estado explícito de
   indeterminação; jamais herda a variedade do lemma sem revisão.
2. Uma forma normalizada nunca substitui nem altera a forma original.
3. Claims publicáveis têm autor/responsável, modalidade e Provenance; classes
   que exigem Evidence não podem ser publicadas sem ela.
4. Tradução PT-BR tem autoria e versão próprias.
5. IPA e demais componentes fonológicos exigem suporte individual identificável.
6. Toda ligação entre registros de variedades diferentes é comparativa e
   explícita; não compartilha automaticamente análises.
7. Recording tem tipo e Variety, e cada dimensão jurídica/comunitária aplicável
   é avaliada separadamente.
8. Licença desconhecida impede redistribuição até decisão, sem presumir proibição
   de mera referência bibliográfica.
9. Conflitos não são resolvidos por sobrescrita.

## OPEN_DECISION — questões a validar posteriormente

Granularidade entre lemma e lexema, tratamento de homonímia, ontologia de
classes, representação de alomorfia, formato de segmentação, níveis fonológicos,
modelo de citações manuscritas, escala de confiança, estados de publicação e
cardinalidades definitivas permanecem deliberadamente abertos.

# Política linguística

## 1. Unidade de diversidade

O projeto não trata “náhuatl” como uma variedade homogênea. Cada dado deve ser
vinculado a uma entidade de variante linguística. Náhuatl Clássico e variantes
modernas — especialmente Hueyapan neste repositório — não podem compartilhar
uma análise por mera semelhança gráfica.

Uma relação histórica, cognata ou de correspondência entre formas será uma
afirmação própria, com fonte ou classificação como inferência/reconstrução. Ela
não transforma duas formas em um único registro.

## 2. Período e localidade

Variante e período são dimensões independentes. Sempre que a fonte permitir,
registram-se intervalo temporal, localidade e comunidade. Valores amplos como
“clássico” ou “moderno” não substituem datação mais precisa. Datas incertas e
atribuições contestadas devem permanecer explicitamente incertas.

## 3. Forma original e normalização

- `forma_original` reproduz a grafia/transcrição da fonte, inclusive variações,
  diacríticos e segmentação, acompanhada por sua localização.
- `forma_normalizada` é uma afirmação derivada e reversível, ligada a uma
  convenção de normalização identificada e versionada.
- o lemma é uma unidade de organização editorial; não substitui as formas
  atestadas nem apaga suas diferenças.
- nenhuma busca, importação ou exibição deve sobrescrever o original com o
  normalizado.

Transcrição diplomática, expansão editorial, correção de erro aparente e
modernização ortográfica são operações distintas e devem ser rotuladas.

## 4. Tradução e significado

Significados descrevem sentidos atribuídos a uma forma/lemma em contexto e têm
proveniência. Traduções PT-BR são objetos editoriais separados, associados ao
sentido ou exemplo pertinente, com tradutor/revisor, versão, data e base usada.
Uma glosa em espanhol ou inglês não deve ser apresentada automaticamente como
tradução portuguesa.

Polissemia e divergência entre fontes geram sentidos ou afirmações paralelas.
Não se fabrica equivalência moderna para preencher lacunas.

## 5. Gramática e morfologia

Classe gramatical, decomposição em prefixos, raízes e sufixos, flexão e demais
análises são afirmações analisáveis e não propriedades indiscutíveis da cadeia.
Cada análise deve declarar:

- o sistema analítico ou referência adotada;
- a forma e variante às quais se aplica;
- os segmentos e suas funções, sem forçar fronteiras não atestadas;
- o responsável e nível de confiança;
- análises concorrentes, quando existirem.

Não se transfere uma análise do Náhuatl Clássico para Hueyapan, ou vice-versa,
sem evidência explícita e identificação do caráter comparativo da afirmação.

## 6. Fonologia e pronúncia

IPA, duração vocálica, saltillo, silabificação e acentuação são campos separados
e dotados de proveniência. Ortografia não autoriza inferência automática desses
valores. Ausência de marca na fonte deve ser registrada como “não informado”,
não como vogal breve ou ausência de saltillo.

Uma representação fonológica reconstruída não é gravação nem pronúncia nativa.
Uma Recording deve declarar Provenance e um tipo de pronúncia. Também devem ser
avaliados separadamente: identidade e Variety do Speaker quando legal e
apropriado; consentimento de coleta; License; copyright e direitos conexos;
direitos de armazenamento, reprodução e redistribuição; restrições
comunitárias/culturais; e direito de retirada, quando aplicável. Consentimento
não é automaticamente necessário nem suficiente para todo áudio externo.

Os tipos são:

- `HUMAN_NATIVE`: fala humana de falante nativo da variante declarada;
- `MODERN_READING`: leitura humana moderna de material, inclusive clássico;
- `HISTORICAL_RECONSTRUCTION`: realização humana baseada em reconstrução;
- `SYNTHETIC`: áudio gerado por síntese.

A categoria deve refletir a origem efetiva do áudio; prestígio ou qualidade não
mudam sua classificação. Uma leitura humana moderna de texto clássico é sempre
`MODERN_READING`, nunca gravação histórica de Náhuatl Clássico.

## 7. Exemplos e corpus

Exemplos devem apontar para uma passagem de corpus ou para material pedagógico
explicitamente identificado como tal. Texto histórico preserva a forma original
e sua localização. Segmentação, normalização, tradução e anotação são camadas
distintas. Exemplos inventados só poderão existir futuramente como conteúdo
pedagógico autoral claramente rotulado, nunca como atestação histórica.

## 8. Conflito, ausência e confiança

Afirmações conflitantes coexistem, cada qual com sua proveniência. Eventual
preferência editorial deve ser registrada como nova decisão justificável, sem
excluir as alternativas. Valores ausentes usam `UNKNOWN`, `NOT_APPLICABLE`,
`NOT_REVIEWED` ou `NOT_ATTESTED`, conforme o glossário. String vazia, `-`, `N/A`
e `NULL` técnico isolado não expressam adequadamente essas diferenças.

Confidence usa provisoriamente `UNASSESSED`, `LOW`, `MEDIUM` ou `HIGH`. Mede uma
avaliação editorial da sustentação da Claim; não é verdade/falsidade, modalidade
epistêmica, qualidade da Source ou estado editorial, não mede autoridade social
da Variety ou do Speaker e não substitui Evidence. A rubrica matemática é
`OPEN_DECISION` até validação posterior ao corpus piloto.

## 9. Revisão

Dados linguísticos exigirão revisão por pessoa competente na variedade e no
tipo de fonte. Conteúdo de variante moderna deve prever consulta e participação
comunitária. Toda correção conserva histórico, autor, data e justificativa.

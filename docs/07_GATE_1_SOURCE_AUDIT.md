# Gate 1 — Auditoria técnica, jurídica e linguística das fontes

## Status, método e limites

Este levantamento técnico-documental foi executado em 2026-09-03. Não é
parecer jurídico e não aprova o Gate 1. Foram usados requests exploratórios
mínimos a páginas institucionais, catálogos oficiais, páginas de permissões e
registros de recursos. Não houve scraping, OCR em massa, download de corpus ou
ingestão lexical.

Quando uma permissão não foi localizada explicitamente, o componente recebeu
`UNKNOWN_RIGHTS`, ainda que a Work histórica seja de domínio público ou o
arquivo esteja disponível para download. `CAN_INGEST` e
`CAN_INGEST_WITH_ATTRIBUTION` são recomendações documentais preliminares, não
conclusões jurídicas. Os registros YAML em `data/source_registry/` são a fonte
estruturada detalhada deste relatório.

O PDF local de Hueyapan foi identificado por nome, tamanho e SHA-256. Inspeção
independente confirmou 136 páginas, dados editoriais, prólogo e estrutura. O
dicionário integral não foi extraído.

## Vocabulário de direitos

- `PUBLIC_DOMAIN_WORK`: Work histórica sem proteção autoral patrimonial
  aparente pelo decurso temporal; não se estende automaticamente à Edition ou
  ao Witness digital.
- `PUBLIC_DOMAIN_DIGITAL_SURROGATE`: reprodução digital declarada como domínio
  público pela instituição. Nenhum componente recebeu este valor sem declaração.
- `OPEN_LICENSE`: licença aberta explicitamente declarada para o componente.
- `RESTRICTED_COPYRIGHT`: direitos reservados ou permissão limitada declarada.
- `UNKNOWN_RIGHTS`: licença/permissões não localizadas ou alocação incerta.
- `CONTRACTUAL_RESTRICTION`: condições contratuais ou termos de plataforma.
- `COMMUNITY_RESTRICTION`: restrição cultural/comunitária documentada; a
  necessidade de investigá-la não equivale a afirmar que já existe.

## Bloco A — núcleo clássico

### A01 — Alonso de Molina, 1571

O catálogo oficial identifica o *Vocabulario en lengua castellana y mexicana*,
impresso no México por Antonio de Spinosa em 1571, em duas partes/direções e com
reprodução digital. É fonte P0 lexical para o náhuatl colonial central. A Work
histórica é tratada como `PUBLIC_DOMAIN_WORK`, mas a reprodução digital e os
metadados permanecem `UNKNOWN_RIGHTS` na ausência de licença explícita. Acesso:
HTML, reprodução por páginas e ligação persistente; API/IIIF não confirmados.

Papel: Evidence lexical histórica, sempre preservando direção, grafia e fólio.
Não oferece IPA; comprimento e saltillo não podem ser inferidos da ausência de
marcação. Evidências: registro da [BVPB](https://bvpb.mcu.es/es/consulta/registro.do?id=469079)
e descrição institucional do [INALI](https://site.inali.gob.mx/publicaciones/libro_lectura_nahuatl/pdf/lectura_del_nahuatl.pdf).

### A02 — Andrés de Olmos

O GDN informa que o *Arte* foi concluído em Hueytlalpan em 1547 e sobrevive em
seis cópias. A lista verbal dita “Vocabulario de Olmos” ocorre no Codex Toledo;
o próprio recurso afirma que sua autoria não está comprovada. Portanto, essa
atribuição deve ser Claim disputada, nunca fato herdado. O GDN também documenta
normalização separada da paleografia.

Papel P0: gramática histórica; lista verbal com atribuição qualificada. Work
histórica: ingestão possível com atribuição a partir de Witness autorizado;
transcrição/normalização moderna do GDN: `CAN_REFERENCE`, direitos não
explicitados. Evidências: [história dos Witnesses](https://gdn.iib.unam.mx/textos/olmos-v)
e [processo de normalização](https://gdn.iib.unam.mx/textos/olmos).

### A03 — Antonio del Rincón, 1595

O registro oficial da University of Utah identifica a primeira edição de
*Arte mexicana* (México, Pedro Balli, 1595), gramática, PDF, ARK e digitalização
de 600 ppi com derivados. O campo Rights do item está vazio: a Work histórica
é `PUBLIC_DOMAIN_WORK`, mas PDF, TIFFs e imagens são `UNKNOWN_RIGHTS`.

Papel P0: Evidence gramatical e exemplos históricos; não é corpus amplo nem
fonte automática de IPA. A estrutura por página/ARK favorece citação. Evidência:
[registro da Marriott Library](https://collections.lib.utah.edu/details?id=296198).

### A04 — Horacio Carochi, 1645

A Biblioteca Virtual Miguel de Cervantes identifica a Edition HTML de 2014,
derivada do impresso mexicano de 1645, com 132 folhas, espanhol e náhuatl, ARK,
BibTeX/RIS e catálogo RDF. Carochi é P0 para gramática e para estudo histórico
de duração vocálica e saltillo, mas sua notação não deve ser convertida
diretamente em IPA.

A Work histórica é `PUBLIC_DOMAIN_WORK`; a transcrição HTML moderna permanece
`CAN_REFERENCE` por falta de licença explícita localizada. Metadados ligados são
referenciáveis, mas a expressão “dados abertos” sem URI de licença não bastou
para autorização de incorporação. Evidências: [registro Cervantes](https://www.cervantesvirtual.com/nd/ark:/59851/bmcvt3g7)
e [apresentação do derivado GDN](https://gdn.iib.unam.mx/textos/carochi).

## Bloco B — plataformas e corpora

### B01 — Gran Diccionario Náhuatl / UNAM

Integra dicionários históricos e modernos, incluindo Molina, Olmos, Rincón,
Carochi, Mecayapan e Tzinacapan. Oferece busca por náhuatl, grafia normalizada e
tradução; em componentes documentais expõe paleografia, tradução, exemplos,
comentários e localizadores. O próprio material descreve normalização e
intervenções editoriais. É, portanto, mistura deliberada de períodos e
Varieties, não um corpus homogêneo.

Não foi localizada licença aberta nem API/exportação documentada. Registros e
camadas editoriais são `CAN_REFERENCE`/`RIGHTS_UNCLEAR`. Prioridade P1 como
descoberta e comparação; toda Claim futura deve manter o dicionário-fonte.
Evidência: [documentação GDN](https://gdn.iib.unam.mx/textos/diccionario-de-documentos).

### B02 — Temoa / UNAM

Interface de corpus histórico com reprodução, Nahuatl, notas e tradução quando
disponíveis, URLs por fonte/fólio e segmentos numerados. A página avisa que nem
todos os textos têm todas as camadas e que o sítio segue em desenvolvimento.
Não foi localizada licença ou API documentada.

Prioridade P1 para localizar ocorrências. Imagens são `RIGHTS_UNCLEAR`;
transcrições, traduções e metadados são `CAN_REFERENCE`. Evidência:
[fólio exploratório oficial](https://temoa.iib.unam.mx/cf_01_i/29r).

### B03 — Digital Florentine Codex / Getty

Edition digital de um manuscrito bilíngue de 12 livros, 2.446 páginas e quase
2.500 imagens, com busca, URLs livro/fólio e viewer IIIF. A página oficial
distingue manuscrito, transcrições de Nahuatl e espanhol, traduções, metadados,
identificações de mãos, ensaios e outros conteúdos.

Direitos foram avaliados por componente. A Work histórica é
`PUBLIC_DOMAIN_WORK`. Imagens do manuscrito são referenciadas sob a licença
específica declarada na página de permissões, que restringe uso comercial e
derivados; por isso ficam `CAN_REFERENCE`. Textos Anderson/Dibble e López
Austin/García Quintana são usados com permissão e “all rights reserved”:
`CAN_REFERENCE`. Metadados/identificações e ensaios Getty explicitamente CC BY
4.0 são `CAN_INGEST_WITH_ATTRIBUTION`; áudio só entra nessa classe quando o item
específico estiver coberto pela declaração Getty.

É P0 para ocorrência clássica. A coluna espanhola é interpretação paralela, não
tradução literal automática do Nahuatl. Evidências: [About](https://florentinecodex.getty.edu/about/1_About_the_Project),
[Citations and Permissions](https://florentinecodex.getty.edu/about/3_Citations_and_Permissions)
e [fólio demonstrativo](https://florentinecodex.getty.edu/en/book/10/folio/1r).

### B04 — Early Nahuatl Library

O Wired Humanities descreve a ENL como biblioteca de manuscritos alfabéticos em
texto integral com transcrições e traduções. URLs observadas chegam ao nível de
documento/fólio/elemento. Não foi localizada licença aberta ou API oficial.

Prioridade P1 como corpus de ocorrências e rastreamento documental;
transcrições, traduções e metadados ficam `CAN_REFERENCE` até autorização.
Evidências: [Wired Humanities](https://wired-humanities.org/) e uma
[citação ENL preservada no OND](https://nahuatl.wired-humanities.org/content/tecpillalli).

### B05 — Online Nahuatl Dictionary

Dicionário agregado editado por Stephanie Wood, ©2000–presente, com fontes
históricas e contribuições modernas, pesquisa, listas alfabéticas, temas,
citações e traduções. A página oficial registrava problemas em buscas complexas
em 2026-08-06. Não foi localizada licença aberta ou exportação oficial.

Prioridade P1, `CAN_REFERENCE`: usar para descoberta e retornar à fonte citada.
Risco crítico de mistura de Variety/período e de copiar camada agregada.
Evidência: [página oficial](https://nahuatl.wired-humanities.org/content/welcome-online-nahuatl-dictionary).

### B06 — Visual Lexicon of Aztec Hieroglyphs

Base pesquisável de glifos, principalmente Codex Mendoza, Matrícula de
Huexotzinco e comparações do Florentino. Direitos de imagem são item/repositório
específicos. A plataforma permite uso acadêmico com citação, enquanto descrições
e comentários individualmente atribuídos declaram CC BY-NC-SA 3.0.

Descrições/comentários: `CAN_INGEST_WITH_ATTRIBUTION`, sujeitos à restrição NC;
imagens e dados cuja licença não esteja clara: `CAN_REFERENCE`. Prioridade P3,
reservada principalmente ao Gate 11. Evidência: [página oficial e declaração de direitos](https://aztecglyphs.wired-humanities.org/).

### B07 — Cantares Mexicanos

A Edition eletrônica UNAM de 2016 oferece PDFs por seção; o volume de estudos é
descrito como 30 MB e identifica editores, ISBNs e instituições. A Work
manuscrita histórica é `PUBLIC_DOMAIN_WORK`, mas estudos, transcrição,
tradução e PDFs modernos são `RESTRICTED_COPYRIGHT`/`CAN_REFERENCE` porque não
foi localizada licença aberta.

Prioridade P1 como corpus poético/histórico. O registro alto/poético não deve
ser generalizado para todo Náhuatl Clássico. Evidência: [Edition UNAM](https://historicas.unam.mx/publicaciones/publicadigital/libros/cantares/cm01.html).

## Bloco C — moderno e fonética

### C01 — Dicionário de Hueyapan 2016

*EJERCICIOS PARA EL APRENDIZAJE DE LA LENGUA NÁHUATL DE HUEYAPAN Y
DICCIONARIO ESPAÑOL-NÁHUATL*, de Marcelino Montero Baeza, é uma *Edición
Electrónica 2016, México*, com ISBN indicado como “en trámite” e 136 páginas. O
trabalho foi financiado em 2012 com recursos do programa “Apoyo a Proyectos de
Comunicación Indígena” da CDI. O prólogo afirma que a obra resulta de pesquisa
comunitária entre habitantes de Hueyapan e representa a Variety da comunidade,
em Hueyapan, Tetela del Volcán, Morelos, México. É exclusivamente Modern Variety
no Nahuatl-BR.

A estrutura confirmada contém introdução/características, alfabeto,
substantivos, plural, verbos, orações, pronomes, adjetivos, numerais, conjugação,
conversação, dicionário espanhol–náhuatl, bibliografia e seção do autor.

A página editorial contém declaração que restringe o uso às finalidades
estabelecidas pelo programa. Isso é registro documental, não parecer jurídico.
O Rights Status é `RESTRICTED_OR_PERMISSION_REQUIRED`, e todo conteúdo
autoral/editorial é `MANUAL_PERMISSION_REQUIRED`. O PDF local permanece
`DO_NOT_INGEST` e não será redistribuído. Papel recomendado: referência
linguística de Hueyapan, comparação explicitamente separada com Classical
Nahuatl e futura fonte de dados somente após autorização adequada. Prioridade
P2. Evidências: [arquivo governamental identificado](https://www.gob.mx/cms/uploads/attachment/file/64177/diccionario_nahuatl_hueyapan_comunicadores_indigenas_v2016.pdf)
e [bibliografia acadêmica independente](https://elpezylaflecha.uv.mx/index.php/elpezylaflecha/article/view/122).

### C02 — INALI

O CLIN oferece nomes, autodenominações e referências geoestatísticas para
Varieties modernas. O ALIN é descrito como acervo físico/digital com
vocabulários, frases, narrativas, áudio e vídeo; “aberto” descreve o acervo, mas
nenhuma licença de reutilização foi localizada. O Audiorama lista 19 áudios de
náhuatl sem direitos/falante/Variety suficientes na página auditada.

Prioridade P1 para metadados de Variety (`CAN_REFERENCE`). ALIN é
`RIGHTS_UNCLEAR`; áudio requer permissão e auditoria por Recording. Evidências:
[CLIN Nahuatl](https://www.inali.gob.mx/sitios/clin-inali/html/v_nahuatl.html),
[ALIN](https://www.inali.gob.mx/detalle/acervo-de-lenguas-indigenas-nacionales)
e [Audiorama](https://site.inali.gob.mx/Micrositios/audiorama/n8.html).

### C03 — UCLA Phonetics Lab Archive: Isthmus-Mecayapan

Página por Variety com lista de palavras, Speaker identificado na amostra,
arquivos WAV/MP3, fichas JPG/TIF e detalhes da Recording. A amostra visível é
de 1966 e nomeia E. Bautista; a própria página alerta que células podem estar
vazias. Download técnico não equivale a licença.

Prioridade P1 para fonética moderna comparativa, nunca pronúncia histórica do
Náhuatl Clássico. Áudio requer permissão manual; fichas/metadados são
`CAN_REFERENCE`. Evidência: [arquivo UCLA](https://archive.phonetics.ucla.edu/Language/NHX/nhx.html).

### C04 — Outros corpora sonoros

Nenhum candidato adicional foi promovido nesta rodada. A busca limitada não
encontrou recurso cuja relevância, documentação de Variety, Provenance de
Recording e direitos justificassem ampliar o escopo. Isso é `NOT_ATTESTED` no
método desta auditoria, não afirmação de inexistência.

## Matriz final

| ID | Fonte | Período/Variante | Valor lexical | Valor gramatical | Valor corpus | Valor fonético | Acesso técnico | Direitos | Ingestion class dominante | Prioridade |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | Molina 1571 | colonial central, PROVISIONAL | alto | médio | médio | baixo | imagens/HTML, folio | Work PD; surrogate desconhecido | CAN_INGEST_WITH_ATTRIBUTION / RIGHTS_UNCLEAR | P0 |
| A02 | Olmos | 1547+, Witness-dependent | alto | alto | baixo | médio | GDN HTML | Work PD; edição moderna desconhecida | CAN_INGEST_WITH_ATTRIBUTION / CAN_REFERENCE | P0 |
| A03 | Rincón 1595 | colonial central, PROVISIONAL | médio | alto | baixo | médio | PDF/imagens/ARK | Work PD; surrogate desconhecido | CAN_INGEST_WITH_ATTRIBUTION / RIGHTS_UNCLEAR | P0 |
| A04 | Carochi 1645 | clássico colonial | médio | alto | baixo | alto histórico | HTML/ARK/RDF | Work PD; HTML moderno desconhecido | CAN_INGEST_WITH_ATTRIBUTION / CAN_REFERENCE | P0 |
| B01 | GDN | histórico + moderno misto | alto | médio | médio | médio | busca HTML | sem licença de dados localizada | CAN_REFERENCE / RIGHTS_UNCLEAR | P1 |
| B02 | Temoa | corpora coloniais mistos | médio | baixo | alto | baixo | folio/segmento HTML | por componente desconhecido | CAN_REFERENCE / RIGHTS_UNCLEAR | P1 |
| B03 | Digital Florentine Codex | 1575–77 + camadas modernas | alto | médio | alto | médio | busca, folio, IIIF | licenças por componente | CAN_INGEST_WITH_ATTRIBUTION / CAN_REFERENCE | P0 |
| B04 | Early Nahuatl Library | documentos coloniais mistos | alto | baixo | alto | baixo | elemento HTML | sem licença aberta localizada | CAN_REFERENCE | P1 |
| B05 | Online Nahuatl Dictionary | histórico + moderno misto | alto | médio | médio | médio | busca/listas HTML | ©2000–presente | CAN_REFERENCE | P1 |
| B06 | Visual Lexicon | glifos séc. XVI | médio | baixo | médio visual | baixo | busca/página | imagem por item; texto CC BY-NC-SA | CAN_INGEST_WITH_ATTRIBUTION / CAN_REFERENCE | P3 |
| B07 | Cantares Mexicanos | séc. XVI, poético | médio | médio | alto | médio histórico | PDFs/HTML | Work PD; Edition restrita | CAN_INGEST_WITH_ATTRIBUTION / CAN_REFERENCE | P1 |
| C01 | Hueyapan 2016 | moderno, Hueyapan | alto | médio | médio | médio | PDF | licença não localizada | MANUAL_PERMISSION_REQUIRED | P2 |
| C02 | INALI | moderno, múltiplas Varieties | médio | baixo | médio | médio | HTML/PDF/áudio | desconhecido por item | CAN_REFERENCE / RIGHTS_UNCLEAR | P1 |
| C03 | UCLA Mecayapan | moderno, Isthmus-Mecayapan | médio | baixo | baixo | alto | WAV/MP3/JPG/TIF | licença não localizada | MANUAL_PERMISSION_REQUIRED / CAN_REFERENCE | P1 |

## Componentes por classe

### CAN_INGEST

Nenhum componente recebeu `CAN_INGEST` sem condição. Até Works históricas e
componentes abertos exigem Provenance/atribuição no Nahuatl-BR.

### CAN_INGEST_WITH_ATTRIBUTION

- texto subjacente das Works históricas A01–A04, a partir de Witness
  tecnicamente e juridicamente adequado;
- Work histórica do Florentino e Cantares, nas mesmas condições;
- metadados/identificações e ensaios Getty explicitamente CC BY 4.0;
- áudio Getty somente após confirmação da licença no item;
- descrições/comentários do Visual Lexicon sob CC BY-NC-SA 3.0, sujeito à
  compatibilidade da restrição não comercial.

### CAN_REFERENCE

Inclui metadados e/ou camadas editoriais de A01, A02, A03, A04, B01–B07, C02 e
C03 conforme detalhado nos YAML. Em particular, transcrições/traduções modernas
do Florentino, ENL, OND e Cantares não devem ser copiadas.

### RIGHTS_UNCLEAR

Inclui surrogates de Molina e Rincón; registros/camadas do GDN; imagens do
Temoa; metadados e imagens não licenciados uniformemente do Visual Lexicon;
ALIN e componentes institucionais sem licença explícita.

### MANUAL_PERMISSION_REQUIRED

- lições, dicionário e exemplos de Hueyapan;
- áudio WAV/MP3 da UCLA;
- áudio INALI/Audiorama e materiais cuja autorização dependa de item,
  Speaker, comunidade ou depositante.

## Riscos críticos e controles recomendados

1. **Contaminação de Variety:** GDN, OND e INALI agregam materiais heterogêneos.
   Controle: Variety/período obrigatórios por Claim e por Attestation.
2. **Transbordamento de direitos:** domínio público da Work não cobre Edition,
   Witness, transcrição ou tradução moderna. Controle: Rights Status por
   componente e bloqueio padrão `UNKNOWN_RIGHTS`.
3. **Camada editorial como original:** normalizações e traduções podem parecer
   atestação. Controle: manter Form original, Normalized Form e Translation
   separadas.
4. **Notação como IPA:** Carochi e ortografias históricas não autorizam conversão
   automática. Controle: Claims fonológicas separadas e revisão especializada.
5. **Áudio moderno como clássico:** UCLA/INALI são evidência de Varieties
   modernas. Controle: tipo `HUMAN_NATIVE` com Variety moderna; nunca Historical
   Recording de Classical Nahuatl.
6. **Direitos comunitários e pessoais:** disponibilidade não resolve Speaker,
   consentimento, copyright conexo ou restrição cultural. Controle: permissão
   item a item antes de armazenamento.

## Prontidão para revisão

As fontes A01–A04, B01–B07 e C01–C03 possuem registro estruturado, Evidence URL,
escopo linguístico, acesso técnico, direitos por componente, riscos, papel e
Ingestion Class. Nenhuma licença ausente foi presumida e não houve ingestão em
massa.

A auditoria está pronta para revisão, com reservas explícitas: direitos de
vários componentes permanecem desconhecidos, C01 requer autorização adequada,
e classificações jurídicas são triagem documental sujeita a revisão competente.
O `EXECUTION_AGENT` recomenda **PASS_WITH_RESERVATIONS**, mas não aprova este
Gate e não autoriza o Gate 2.

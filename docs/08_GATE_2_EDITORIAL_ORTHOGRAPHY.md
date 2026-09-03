# Gate 2 — Padrão editorial e ortográfico do Náhuatl Clássico

## Status e escopo

Esta política é `DRAFT`, versão 1.0.0, restrita ao tratamento editorial de
Náhuatl Clássico. Não aprova o Gate, não cria corpus de Lemmas, não define IPA e
não transfere dados de Modern Varieties. O YAML normativo correspondente é
`data/policies/classical_orthography_v1.yml`.

## Invariantes

1. `SOURCE_FORM` é imutável.
2. `NORMALIZED_FORM` nunca substitui `SOURCE_FORM`.
3. `PEDAGOGICAL_FORM` nunca é apresentada como transcrição diplomática.
4. `SEARCH_KEY` nunca é publicada como Evidence linguística.
5. Ausência de Diacritic não prova ausência de contraste fonológico.
6. Comprimento vocálico e saltillo não são inferidos sem Evidence.
7. IPA não é reconstruído neste Gate.
8. Modern Varieties não são convertidas automaticamente em Classical Nahuatl.
9. Hueyapan não preenche lacunas clássicas.
10. `UNKNOWN`, `NOT_APPLICABLE`, `NOT_REVIEWED` e `NOT_ATTESTED` permanecem
    semanticamente distintos.

## Seis camadas obrigatórias

### SOURCE_FORM

Valor exato fornecido pela Source consultada. Preserva maiúsculas, espaços,
pontuação, abreviaturas, grafemas e Diacritics inclusive quando a Source é uma
Edition moderna. Deve apontar para Source, Witness/Edition e Locator. Uma
correção cria Claim/camada editorial; nunca altera este valor.

### DIPLOMATIC_FORM

Transcrição fiel ao Witness quando o projeto a produzir. Toda expansão,
restituição, leitura de ligadura, quebra de linha ou caractere incerto é
Editorial Intervention registrada. Colchetes não são silenciosamente removidos.

### NORMALIZED_FORM

Forma derivada por `NormalizationProfile` explícito e versionado. Serve à
comparação editorial; não se declara “a grafia correta”. A versão 1 só permite
regras conservadoras e condicionais. Se uma equivalência exigir análise não
disponível, o valor fica `UNKNOWN` ou a Source Form é repetida com anotação de
“nenhuma regra aplicada”.

### PEDAGOGICAL_FORM

Forma de ensino. A convenção candidata usa minúsculas, macrons `ā ē ī ō` para
comprimento comprovado e `h` para saltillo comprovado. Esses sinais não afirmam
que a Source os continha. Sem Evidence, o traço desconhecido não é preenchido;
alternativas podem coexistir.

### SEARCH_KEY

Chave técnica exclusivamente para busca. Pode ser lowercase, NFC e sem
Diacritics segundo perfil declarado. Assim, `xochitl` e `xōchitl` podem produzir
a mesma chave candidata e recuperar o mesmo conjunto, sem Claim de identidade.
Aliases históricos são chaves adicionais ligadas à Form, não substituições.

### PHONOLOGICAL_REPRESENTATION

Camada de Claims distinta de todas as grafias. Pode futuramente conter
comprimento, saltillo, segmentação fonológica e IPA, cada qual com Evidence.
Neste Gate só são definidos estados e separação; não se gera IPA.

## Unicode

- arquivos controlados usam UTF-8;
- formas editoriais controladas (`DIPLOMATIC_FORM`, `NORMALIZED_FORM`,
  `PEDAGOGICAL_FORM`) usam NFC;
- `SOURCE_FORM` guarda os code points recebidos e também registra, futuramente,
  o estado Unicode detectado; nenhuma normalização destrutiva é silenciosa;
- `ā ē ī ō` e `Ā Ē Ī Ō` preferem caracteres NFC precompostos nas camadas
  controladas; combinantes são aceitos na captura e convertidos apenas fora de
  `SOURCE_FORM` com operação registrada;
- apóstrofos ASCII, `’`, `ʼ`, saltillo Unicode e caracteres parecidos não são
  equivalentes automaticamente;
- hífen-minus, non-breaking hyphen e outros hífens são preservados em
  `SOURCE_FORM`; mapeamento em Search Key é lossy e versionado;
- caracteres históricos ou não reconhecidos são preservados e sinalizados para
  revisão, nunca descartados.

## Comprimento vocálico

Estados por vogal/segmento:

- `SHORT`: breve sustentada por Evidence;
- `LONG`: longa sustentada por Evidence;
- `UNKNOWN`: aplicável, mas não determinada;
- `NOT_APPLICABLE`: comprimento não se aplica à unidade;
- `NOT_REVIEWED`: ainda não avaliado.

Na Pedagogical Form, `LONG` pode ser grafado `ā ē ī ō` (e maiúsculas
correspondentes). `SHORT` permanece sem macron, mas apenas quando seu estado é
explicitamente sustentado. `UNKNOWN` também aparece sem macron na string, porém
deve acompanhar metadado `UNKNOWN`; portanto a aparência nunca basta para
distingui-lo de `SHORT`. Nunca se transforma `a` em `ā` sem Evidence vinculada.

## Saltillo

As Sources registram ou omitem saltillo de modos distintos. Carochi emprega
Diacritics dentro de seu sistema; convenções acadêmicas modernas podem empregar
`h` ou outros sinais. A política separa:

- Source Form: conserva exatamente o sinal/ausência da Source;
- Normalized Form: v1 não acrescenta nem remove saltillo; preserva a cadeia ou
  deixa a questão anotada;
- Pedagogical Form: usa `h` somente para uma Claim de saltillo sustentada;
- Phonological Representation: guarda a análise separada, sem defini-la como
  simples letra;
- Search Key: pode gerar, além da chave estrita, chave lossy sem `h` apenas para
  recuperação, registrada como `search-fold-saltillo`; isso não altera Forms.

O uso pedagógico de `h` é uma convenção candidata deste perfil, escolhida por
legibilidade e compatibilidade com convenções acadêmicas documentadas no GDN;
alternativas permanecem válidas e registráveis. Realização fonética e posição
de saltillo desconhecidas continuam `UNKNOWN`.

## Capitalização, pontuação, espaços e hífen

- Source Form conserva tudo.
- Diplomatic Form conserva por padrão, registrando expansão ou regularização.
- Normalized Form v1 pode aplicar lowercase somente a uma forma isolada quando
  capitalização não for linguisticamente contrastiva e a condição estiver
  revisada; início de frase e nomes próprios não são normalizados cegamente.
- Pontuação não pertence automaticamente ao Lemma; sua remoção só é permitida
  em Search Key e é lossy.
- Espaços e fronteiras de palavra são Evidence editorial/histórica; junção ou
  separação exige regra e revisão.
- Hífen morfológico não é inferido. Hífens da Source são preservados; Search Key
  pode produzir alias sem hífen marcado como lossy.

## Matriz de variação ortográfica

`historical_examples` são strings efetivamente exibidas nas fontes auditadas;
não afirmam equivalência fonológica além da interpretação citada.

| Fenômeno | historical_examples | Source | Interpretação | Decisão v1 | Confidence | Open questions |
|---|---|---|---|---|---|---|
| u/v/hu/uh | `quauhcomitl`, `huia`; GDN registra regra `<u>` semiconsoante → `hu` em Rincón | Molina/GDN; Rincón/GDN | múltiplas funções e posições | nenhuma troca global; aliases condicionais | MEDIUM | ordem e contexto de cada regra |
| c/qu | `Nequametl` → `necuametl`; `quauhcomitl` → `cuauhcomitl` | Molina 1571 via GDN | distribuição condicionada, não troca cega | `qu`→`cu` somente nos contextos documentados e com revisão | HIGH | exceções e fronteiras |
| z/ç/c | `mauiaçoti`; GDN registra `<ç>`→`z` em Rincón | Rincón/GDN | grafias históricas para série sibilante | normalização condicionada `ç`→`z`; `c` exige contexto | MEDIUM | valores históricos por período |
| x | `xochitl`, `ixquich` | GDN/Carochi | Grapheme histórico estável em exemplos | preservar `x`; nenhuma conversão fonética | HIGH | variação por Witness |
| ch | `chichi`, `chocctia` | Rincón/GDN | dígrafo documentado | preservar `ch` | HIGH | duplicação adjacente |
| tz | `notza`, `piltzintli` | Carochi/GDN | sequência documentada | preservar `tz` | HIGH | nenhuma regra fonológica neste Gate |
| tl | `copalli`, `tlateotoquiliztli` | Molina/Carochi/GDN | Grapheme/sequência documentada | preservar `tl` | HIGH | posição final e segmentação |
| cu/uc | `Nequametl`/`necuametl`, `quauhcomitl`/`cuauhcomitl` | Molina/GDN | ordem gráfica depende de contexto | não transpor automaticamente; regra contextual | MEDIUM | formalização dos ambientes |
| y/i | `ycuelia`→`icnelia`; GDN: `y` inicial→`i`, `i` semiconsoante→`y` | Rincón/GDN | função depende do contexto | regras separadas e condicionais | MEDIUM | nomes próprios e hiatos |
| duplicação consonantal | `chocctia`→`choctia`, `nicnönötza` | Rincón; Carochi/GDN | pode ser erro tipográfico ou morfologia | nunca colapsar genericamente | HIGH | revisão caso a caso |
| h | `quauhcomitl`, proposta acadêmica de `h` para fechamento glotal | Molina; GDN sobre Karttunen/Carochi | `h` tem usos ortográficos diferentes | preservar Source; pedagógico só com Evidence | HIGH | escolha final após Gate 4 |
| saltillo histórico | `nicnònotza`, `monònötztihuî` descritos com saltillo | Carochi/GDN | Diacritics de Carochi codificam análise própria | Source preservada; Pedagogical `h` apenas com Claim | HIGH | mapeamento completo do sistema de Carochi |
| comprimento vocálico | `chichi` longo/breve; `nötza`, `icnöilama` | Rincón/Carochi via GDN | marcação/descrição explícita em fontes selecionadas | macron pedagógico apenas com Evidence | HIGH | escopo e conflitos entre fontes |
| ligaduras/abreviações | restituição `[n]` descrita pelo GDN | GDN Docs México | expansão editorial explícita | Diplomatic preserva e registra intervenção | HIGH | convenção por Witness |
| hífen | prefixos pospostos e segmentações editoriais no GDN | GDN | pode ser editorial/morfológico | não introduzir em v1 fora de citação | MEDIUM | modelo morfológico futuro |
| espaços/fronteiras | exemplos corridos de Carochi; entradas isoladas GDN | Carochi/GDN | Edition pode impor segmentação | preservar; alteração exige Claim | MEDIUM | critérios diplomáticos por Edition |
| maiúsculas/minúsculas | `Nequametl`, `Nimitz nötza`, `copalli` | Molina/Carochi via GDN | posição/editorialização variável | Source preservada; lowercase apenas em Search Key | HIGH | nomes próprios |
| pontuação | `pal,`, `analco.`, exemplos com vírgula | Rincón/Molina via GDN | pontuação pode pertencer à Edition | preservar Source; remover apenas em chave lossy | HIGH | limites de entrada |
| marcas modernas | macron `ā`, colchetes `[n]`, campos “normalizada/paleografía” | GDN | intervenções modernas distinguíveis | registrar perfil/editor/agente | HIGH | importação futura por componente |

## Search Key v1

O perfil produz múltiplas chaves, sempre ligadas à Form de origem:

1. `strict_nfc`: NFC + lowercase para correspondência técnica;
2. `fold_diacritics`: remove Diacritics de comprimento/acento da chave estrita
   (`xōchitl` → `xochitl`), `lossy: true`;
3. `fold_punctuation`: remove pontuação periférica, `lossy: true`;
4. aliases históricos: somente regras autorizadas e registradas, nunca uma
   cadeia universal;
5. `fold_saltillo`: opcional e separado, remove `h` pedagógico para ampliar
   recall, `lossy: true`.

Resultados devem retornar todas as Forms candidatas e suas camadas, não fundi-las.
Search Key nunca alimenta Reconstruction, Normalized Form ou Claim fonológica.

## Normalization Profile

`classical_orthography_v1` contém `profile_id`, nome, versão semântica, escopo,
data, status `DRAFT`, Evidence e notas. Cada regra possui `rule_id`, descrição,
padrões, condição, `lossy`, Evidence e Confidence. Regras não implementam
algoritmo neste Gate; descrevem transformações candidatas reproduzíveis.

## Evidência principal

- GDN, [apresentação e filosofia de normalização](https://gdn.iib.unam.mx/presentacion),
  acesso em 2026-09-03;
- GDN, [Rincón: regras e correções](https://gdn.iib.unam.mx/textos/rincon),
  acesso em 2026-09-03;
- GDN, [Carochi e convenções acadêmicas](https://gdn.iib.unam.mx/textos/carochi),
  acesso em 2026-09-03;
- GDN, [Olmos e separação entre paleografia/normalização](https://gdn.iib.unam.mx/textos/olmos),
  acesso em 2026-09-03;
- GDN, [Documentos de México: camadas e restituições](https://gdn.iib.unam.mx/textos/diccionario-de-documentos),
  acesso em 2026-09-03.

## OPEN_DECISION

- inventário completo das regras por Source/Witness;
- normalização definitiva de `u/v/hu/uh`, `cu/uc`, `y/i` e sibilantes;
- escolha final e mapeamento integral do saltillo após o modelo fonológico;
- tratamento diplomático de ligaduras/abreviações por Witness;
- política de fronteira de palavra e hífen morfológico;
- uso de maiúsculas em nomes próprios;
- rubrica operacional de Confidence;
- aprovação externa e eventual versão 1.0.0 `APPROVED`.

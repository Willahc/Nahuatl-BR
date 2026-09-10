# Gate 6 — Scale source preflight

Executor: EXECUTION_AGENT. Data: 2026-09-10. Gate 6 IN_PROGRESS; Gate 7 NOT_STARTED.

## Resultado

`GATE_6_SCALE_SOURCE_PREFLIGHT: PASS_FOR_CONTROLLED_MANUAL_BATCHES`

A01 dispõe de um acesso adicional verificado, distinto do surrogate BVPB de
direitos incertos. Nenhuma autorização deste relatório se estende a qualquer
PDF, site, OCR ou edição moderna de Molina.

| Campo | Acesso selecionado |
|---|---|
| Work | Alonso de Molina, Vocabulario en lengua castellana y mexicana / mexicana y castellana |
| Edition | México, Antonio de Spinosa, 1571; duas partes, direções distintas |
| Witness | John Carter Brown Library, 1-SIZE B571 .M722v; catálogo b3200678 |
| Institution | John Carter Brown Library, Brown University |
| Item | https://americana.jcblibrary.org/search/object/jcbcap-991031815189706966-vocabularioenlen00moli/ |
| Catalog cross-reference | https://archive.org/details/vocabularioenlen00moli ; ark:/13960/t70v9j99r |
| Access layer | Americana IIIF manifest + imagens JCB Luna, componente específico A01/jcb_1571_images |
| Rights basis | https://jcblibrary.org/permissions/ declara CC BY 4.0 para as coleções digitais JCB, incluindo Luna e Internet Archive |
| Attribution | Courtesy of the John Carter Brown Library; autor, edição, exemplar e URL por captura; indicar transcrição seletiva e tradução editorial |
| Machine readability | Imagens legíveis; manifesto JSON. OCR IA anunciado, não verificado como transcrição fiel e não usado como Evidence |
| Locator scheme | ID do canvas + índice de página do manifesto (1-based) + coluna + headword; foliação impressa somente quando conferida |
| Mediation | DIRECT_WITNESS somente após inspeção visual da imagem; imagem digital de exemplar histórico, não exemplar físico |
| Checksum | SHA-256 das imagens efetivamente obtidas e inspecionadas, por captura; arquivos fora do repositório |

Manifesto consultado:
https://americana.jcblibrary.org/iiif/presentation/jcbcap-991031815189706966-vocabularioenlen00moli/manifest/manifest.json

O manifesto retornou 589 canvases. O catálogo IA registra erros de foliação e
troca de folhas entre partes; não inferir folio por aritmética do índice digital.
A portada (canvas 5) e páginas 265/270 foram inspecionadas no preflight. A
portada confirma título, impressão e ano. As páginas lexicais permitem leitura
manual, incluindo glosas e marcas históricas; casos ilegíveis serão excluídos.
Acesso local a archive.org falhou por DNS, mas Americana/Luna funcionou.
Não foi necessário usar GDN nem OCR para superar essa limitação.

## Camadas não habilitadas para captura em escala

- A01/BVPB digital_surrogate: continua RIGHTS_UNCLEAR. O novo componente JCB
  não modifica essa decisão.
- A02/Olmos: Work histórico permitido; paleografia/normalização GDN continua
  CAN_REFERENCE. Autoria do vocabulário permanece controversa. Sem captura nova.
- A03/Rincón: Work histórico permitido; surrogate Utah com direitos não
  resolvidos no registry. Sem captura nova dessa camada.
- A04/Carochi: Work histórico permitido; HTML Cervantes e edição/paleografia
  moderna continuam CAN_REFERENCE. Sem captura nova dessa camada.
- B01/GDN: somente discovery, cross-check e locator; sem crawler, harvesting
  ou dataset bulk. Attestation mediada deve permanecer AGGREGATOR.
- B03/Florentine Codex: ocorrência/referência por componente. Transcrição
  moderna, traduções, imagens e áudio não se confundem com Work. Nenhuma
  extração de Anderson/Dibble, Getty transcription ou áudio é autorizada aqui.
- Primeros Libros/Palafoxiana foi consultado como alternativa: o registro
  `401916addd18c602011ff0ea7e427cfe` combina Public Domain Mark com restrições
  de republicação de imagem; não usado para ingestão nesta entrega.

## Condições para os lotes

Somente transcrição seletiva de entradas visualmente verificadas, preservando
SOURCE_FORM. Glosa histórica curta permanece visível; PT-BR é proposta EDITORIAL
DRAFT independente, com confiança e derivação. Não inferir fonologia ou
morfologia. Não copiar arquivos de imagem para Git/Pages. Cada lote de 50 passa
pelo pipeline Gate 5 e checkpoint antes do seguinte. A disponibilidade deste
exemplar não garante a meta de 300 lemmas com fontes independentes: a métrica
real será publicada, sem inventar uma segunda fonte.

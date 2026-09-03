# Mapa de fontes candidatas

## Status deste documento

Este é um inventário para auditoria, não uma autorização de uso. Inclusão não
confirma licença, titularidade, autenticidade, cobertura, acesso programático,
qualidade, variante exata ou método de extração. Esses pontos serão verificados
individualmente no Gate 1 antes de qualquer cópia, download ou ingestão.

## Matriz preliminar

| Candidato | Natureza preliminar | Contribuição a investigar | Separação/cautela necessária | Estado |
|---|---|---|---|---|
| Andrés de Olmos | obra histórica | gramática e descrição do período colonial | identificar edição, testemunho, datação e paginação | não auditado |
| Alonso de Molina | obra histórica | léxico e formas coloniais | distinguir edições/direções do dicionário e grafia original | não auditado |
| Antonio del Rincón | obra histórica | descrição gramatical | verificar edição, convenções e localização citável | não auditado |
| Horacio Carochi | obra histórica | gramática, quantidade vocálica e saltillo | não generalizar a marcação para formas sem atestação | não auditado |
| Códice Florentino | manuscrito/corpus histórico | ocorrências contextualizadas e material multilíngue | distinguir livros, mãos, colunas, edições, imagens e transcrições | não auditado |
| Gran Diccionario Náhuatl / UNAM | recurso lexical digital | consulta cruzada de entradas e fontes | verificar termos, API/exportação, cobertura e atribuição por registro | não auditado |
| Temoa / UNAM | ferramenta/recurso digital | busca e descoberta de materiais | verificar escopo, persistência de resultados e termos de uso | não auditado |
| Cantares Mexicanos | manuscrito/corpus histórico | formas e passagens contextualizadas | identificar edição/transcrição, fólio e camadas editoriais | não auditado |
| Early Nahuatl Library | biblioteca/corpus digital | documentos e metadados históricos | verificar direitos por item, transcrição e localização | não auditado |
| Online Nahuatl Dictionary / Wired Humanities | dicionário digital | descoberta lexical e remissão a fontes | verificar termos, proveniência interna e possibilidade de reutilização | não auditado |
| Visual Lexicon of Aztec Hieroglyphs | léxico visual/digital | formas glíficas, leituras e imagens | direitos de imagem, critérios de leitura e granularidade de citação | não auditado |
| INALI | instituição e recursos linguísticos | identificação/classificação de variantes e materiais modernos | verificar recurso específico, variante, autoria comunitária e licença | não auditado |
| UCLA Phonetics Archive | arquivo de áudio/fonética | gravações e documentação fonética | confirmar coleção, consentimento, variante, falante e reutilização | não auditado |
| Dicionário de Hueyapan em `sources/hueyapan` | PDF local; conteúdo ainda não inspecionado | possível léxico da variante de Hueyapan | manter fora do corpus clássico; auditar metadados, licença, escopo e consentimento | presente, não auditado |

## Registro local observado

No início do Gate 0 foi observado, sem análise de conteúdo, o arquivo:

`sources/hueyapan/diccionario_nahuatl_hueyapan_comunicadores_indigenas_v2016.pdf`

Sua localização não prova permissão de redistribuição ou extração. O arquivo
deve permanecer imutável até a auditoria; futuramente será necessário registrar
hash, origem de aquisição, data de obtenção, versão, responsáveis, termos e
eventuais restrições. Ele jamais deve alimentar registros marcados como Náhuatl
Clássico.

## Ficha de auditoria prevista para o Gate 1

Cada candidato deverá receber uma ficha contendo, no mínimo:

- identidade bibliográfica ou institucional inequívoca;
- versão, edição, testemunho ou coleção;
- URL/catálogo e data de acesso, quando aplicável;
- detentor(es) de direitos e texto verificável da licença/termos;
- permissões para acesso, extração, transformação, armazenamento e
  redistribuição, avaliadas separadamente;
- restrições de atribuição, uso comercial, derivados e dados pessoais;
- variantes, períodos, localidades, gêneros e campos cobertos;
- granularidade disponível de página, fólio, entrada, linha, imagem ou áudio;
- formatos, estabilidade, acesso técnico e limites operacionais;
- qualidade, vieses, lacunas, convenções de transcrição e riscos de mistura;
- decisão: `APPROVED`, `APPROVED_WITH_RESTRICTIONS`, `REJECTED` ou `PENDING`;
- responsável, data, evidências e próxima revisão.

## Classes de uso a manter separadas

Uma mesma fonte pode cumprir mais de uma função, mas elas não são equivalentes:

- **evidência primária:** manuscrito, impresso histórico, gravação ou ocorrência;
- **fonte acadêmica:** edição crítica, gramática, artigo ou análise;
- **índice/ferramenta de descoberta:** conduz a outra fonte, mas não herda
  automaticamente sua autoridade ou licença;
- **conteúdo editorial do projeto:** normalização, tradução PT-BR e curadoria;
- **material comunitário moderno:** requer identificação da variante, autoria,
  consentimento e condições de uso apropriadas.

## Questões abertas por candidato

Para todos permanecem abertas: qual objeto/edição exata usar, que direitos se
aplicam aos dados e às imagens, como citar no nível da afirmação, qual qualidade
de transcrição existe, e se o acesso permite o uso planejado. Nenhum método de
extração foi escolhido.

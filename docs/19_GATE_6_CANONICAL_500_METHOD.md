# Gate 6 — Método do corpus canônico

Alvo: 500 registros únicos, incluindo L0001–L0050 imutáveis e 450 novos IDs
L0051–L0500, atribuídos por admissão em nove lotes. IDs não codificam ordem
alfabética. O executor não aprova nem encerra o Gate.

`data/canonical/catalog.json` declara a fonte canônica composta: referências aos
50 arquivos piloto, sem cópia física, e os novos arquivos em
`data/canonical/lemmas/`. `data/gate6/baseline.json` fixa o commit anterior e
hashes semânticos e dos blobs Git dos 50. A comparação semântica evita falsos
positivos por CRLF de checkout e detecta qualquer mudança de campo.

Cada lote TSV contém captura manual de imagens JCB inspecionadas: página digital,
coluna, headword preservado, glosa histórica curta, proposta PT-BR e domínio
editorial. Não se completa uma entrada de memória. Trechos incompletos ou
ilegíveis são excluídos. Não se infere gênero, classe lexical, morfologia,
comprimento vocálico, saltillo ou IPA.

`scripts/admit_gate6_batch.py` é dry-run por padrão e reutiliza
`IngestionEngine`. Source resolution, Rights Gate, Variety Gate, Normalizer,
Claim/Evidence builders executam antes do adaptador canônico. `--write` é
explícito, admite somente 50 após a validação de todos, exige o checkpoint
anterior e nunca sobrescreve um ID. O request e digest ficam em cada registro;
o validador refaz o pipeline e compara seus artefatos integralmente.

PT-BR tem translation_id, modalidade EDITORIAL, estado DRAFT, derived_from,
confidence e editorial_provenance. Glosa histórica tem Claim OBSERVED apenas
quanto à leitura visual da página, não quanto à verdade universal de uma
equivalência lexical. Traduções são propostas do EXECUTION_AGENT, não de Molina.
Confidence MEDIUM registra legibilidade da captura e limitações da interpretação
monofonte; não equivale a revisão humana. Todas as novas Claims ficam DRAFT.

Uma entrada histórica pode conter prefixos de citação, acepções alternativas e
remissões; a captura seletiva não afirma que uma glosa esgota o lemma. Casos
semânticos permanecem NEEDS_SEMANTIC_REVIEW. SINGLE_SOURCE/MULTI_SOURCE medem
cobertura; não substituem modalidade, Confidence ou estado editorial.

O detector compara SOURCE_FORM, NORMALIZED_FORM, SEARCH_KEY e textos de sentidos.
O relatório `duplicate_candidates.json` preserva pares, motivos e CANDIDATE_ONLY.
Colisão não prova identidade; não há fusão. Quantidade de IDs não prova que todos
os problemas de identidade lexical estejam resolvidos.

`validate_gate6.py --check` exige 500/450. `--checkpoint N` exige exatamente
50 + 50*N e não é aprovação final. Cada checkpoint deve PASS antes do lote
seguinte; falha de direitos/evidência impede continuação. `--check` não aceita
499/501. Testes sintéticos nunca entram no corpus ou na Evidence publicada.

A auditoria de 10% ordena IDs por SHA-256(UTF-8(lemma_id + `gate6-audit-v1`)) e
seleciona os primeiros 50, sem substituições manuais. A revisão inclui direitos,
locator, imagem/attestation, tradução, Evidence, Variety, forms, risco de colisão
e estado. A seleção sozinha não significa auditoria concluída.

O Preview é derivado. O exporter agrega os mesmos registros canônicos e preserva
os 50; o Gate 5 verifica essa inclusão e a reprodução exata, enquanto o Gate 6
impõe a cardinalidade final. Research Preview 1 somente após 500 validados.
Nenhum arquivo de fonte, imagem ou PDF é publicado. Gate 7 não é iniciado.

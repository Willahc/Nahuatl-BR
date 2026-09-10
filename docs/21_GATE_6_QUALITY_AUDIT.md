# Gate 6 — Quality audit (checkpoint 01)

Os 50 registros novos foram admitidos com replay do pipeline Gate 5 e
`pipeline_digest` persistido. Cada um tem SOURCE_FORM visualmente transcrito,
attestation A01, locator de página/coluna/headword, Evidence resolvida, glosa
histórica curta, tradução PT-BR EDITORIAL DRAFT, provenance e confidence
MEDIUM. Não há IPA, comprimento vocálico, saltillo ou morfologia automática.

O detector encontrou três candidatos de duplicidade. Nenhum foi fundido, e
SEARCH_KEY não é tratado como identidade linguística. Todos os novos registros
estão SINGLE_SOURCE e NEEDS_SEMANTIC_REVIEW. A seleção de auditoria de 10% é
determinística por SHA-256(lemma_id + `gate6-audit-v1`); a amostra final de 50
será materializada apenas com 500 registros.

Controles negativos Gate 6 (18) e o controle positivo passaram em testes
sintéticos; sintéticos não entram no corpus. Gate 3, Gate 4, Gate 5 e o
exporter permanecem sem enfraquecimento. O Preview continua Research Preview 0
e é derivado; não é fonte canônica.

Resultado: **PASS no checkpoint 01; Gate 6 IN_PROGRESS / BLOCKED_BY_SOURCE_EVIDENCE
para expansão adicional nesta execução**. Esta condição não encerra o Gate e
não inicia Gate 7.

## Checkpoint 02 — source path resolved

O caminho OCR-assisted foi resolvido para o mesmo exemplar JCB de Molina 1571. OCR permanece somente um auxiliar técnico de localização; a admissão canônica usa transcrição visual da imagem, com página/canvas, coluna e hash da imagem.

O lote 02 adicionou L0101–L0150, elevando o corpus para 150 lemmas. Os 50 registros foram visualmente verificados, passaram pelo pipeline Gate 5 e pelo validador Gate 6. Foram preservados 8 candidatos de duplicidade sem fusão automática. O Preview continua Research Preview 0.

Resultado: **PASS no checkpoint 02; Gate 6 IN_PROGRESS / SOURCE_EVIDENCE_PATH_RESOLVED**. A aprovação do checkpoint não fecha o Gate 6 e não inicia o Gate 7.

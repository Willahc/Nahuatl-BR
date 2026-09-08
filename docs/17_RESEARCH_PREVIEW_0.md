# Research Preview 0 (Gate 5)

Executor: `EXECUTION_AGENT`. O Gate 5 permanece `IN_PROGRESS`. Esta prévia é um
produto de **pesquisa**, não de publicação: apresenta candidatas fonológicas,
dados de referência e fontes dentro do círculo do projeto, sem áudio e sem
afirmações promovidas a fatos.

## O que é

Aplicativo estático (Vite + React + TypeScript) em `preview/` que lê o arquivo
derivado `preview/public/data/nahuatl-br.json` — gerado deterministicamente
por `scripts/build_preview_data.py` a partir de dados canônicos de `data/`
(`gate_status`, sources, lemmas piloto, candidatas de integração fonológica).

## Schema do arquivo de dados

- `schema`: `nahuatl-br-preview-v1`.
- `generated_at`: sempre `NOT_RECORDED` (build determinístico, sem timestamp).
- `gate_status`: estados dos gates de GATE_STATUS.md.
- `counts`: lemmas (50), sources, claims_total, evidence_total, integration_items.
- `sources`: apenas fontes de uso permitido; fontes modernas (C01/C02/C03)
  **não** aparecem.
- `lemmas`: formas (source/normalized/pedagogical/search), interpretações,
  traduções editoriais PT-BR, glosas históricas, fonologia do lema e
  `analysis_candidate` (proposta de integração, com `editorial_state`,
  `modality`, `confidence`).

## Rotas (HashRouter)

`/#/` · `/#/dicionario` · `/#/lemma/:id` · `/#/fontes` · `/#/fonologia`

- **HashRouter** é usado de propósito: a prévia é servida como estática no
  GitHub Pages do repositório, que não faz fallback para `index.html` em rotas
  profundas com reescrita de servidor.
- `dicionario`: busca sem diferenciar diacríticos (NFD + remoção de acentos,
  alinhada ao conceito de SEARCH_KEY); `xochitl` e `xöchitl` convergem.
- `fonologia`: chamada de "Reconstrução fonêmica (candidata)" para
  `analysis_candidate`; estados `DRAFT`/`IN_REVIEW` visíveis via badges.
- `fontes`: fontes de referência com papel recomendado; modernas estão fora.
- Tema claro/escuro salvo em `localStorage` (padrão do sistema).

## Reprodução

```powershell
python scripts/build_preview_data.py --write   # gera preview/public/data/nahuatl-br.json
cd preview
npm install                                    # gera package-lock.json
npm run build                                  # tsc -b && vite build (saída em dist/)
npm run dev                                    # servidor local de desenvolvimento
```

`preview/dist/` e `preview/node_modules/` são ignorados pelo `.gitignore`; o
`package-lock.json` é versionado para builds reprodutíveis em CI.

## Limites desta prévia

- Nenhum áudio, nem IPA sintetizado, nem afirmação promovida a fato.
- Claims `IN_REVIEW` aparecem apenas como IDs; detalhes não são publicados.
- O rótulo `classical_phonology_v1@1.0.0-draft.1` (histórico da entrega do Gate
  4) permanece como está nos dados canônicos.
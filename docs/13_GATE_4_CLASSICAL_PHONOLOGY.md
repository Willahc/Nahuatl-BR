# Gate 4 — Fonologia do Clássico: modelo e limites

## Estado do modelo

`status: APPROVED` (policy `data/policies/classical_phonology_v1.yml`, v1.0.0,
`approval_reference: ORCHESTRATOR_REVIEWER_GATE_4_PASS`). Aprovado como **modelo
fonológico** para os próximos Gates: framework de reconstrução fonêmica e modelo
de evidência ortografia→fonologia (ver `approved_scope`/`not_approved_as` na
policy). O escopo é a documentação colonial central (principalmente séculos
XVI–XVII), **não pan-nahua**; Hueyapan e Mecayapan ficam excluídos do escopo.

`policy status = APPROVED` não significa que toda reconstrução individual seja
certeza histórica: as 29 Claims seguem `IN_REVIEW`, sem revisão humana individual
documentada, e os níveis `candidate`/`reconstructed`/`reported` de cada proposição
são preservados abaixo.

## Camadas de análise

O policy define camadas para impedir que notação histórica seja apresentada como
fonética moderna:

- `ORTHOGRAPHIC_EVIDENCE`: grafias e diacríticos reportados (ex.: Olmos `u`/`o`,
  `l/ll`, G4C027).
- `PHONOLOGICAL_ANALYSIS`: afirmações estruturais (contrastes, distribuição,
  processos). Ex.: quantidade elegendo o par `chichi` (G4C026), coda sonorante.
- `PHONEMIC_RECONSTRUCTION`: reconstrução de unidades, ex.: `/ʔ/` (G4C006,
  MEDIUM), `/t͡ɬ/` (G4C011), `/kʷ/` (G4C012).
- `PEDAGOGICAL_PRONUNCIATION`: convenções didáticas (ex.: `h` pedagógico,
  G4C008/G4C009), que nunca são Evidence sobre realização histórica exata.

`phonemic_ipa` só existe nos Claims onde o fonema em si é o objeto da afirmação
(G4C006 `/ʔ/`, G4C011 `/t͡ɬ/`, G4C012 `/kʷ/`); `phonetic_ipa` não está preenchido
em nenhum Claim ou item de integração — todo o restante é `NOT_REVIEWED`.

## Dimensões de certeza

Cada Claim usa um eixo de incerteza distinto do tipo de fonte e do estado
editorial: `CONTRAST_EXISTENCE`, `DISTRIBUTION`, `HISTORICAL_RECONSTRUCTION`,
`PHONETIC_REALIZATION`, `PEDAGOGICAL_CONVENTION`, `MORPHOPHONOLOGICAL_PROCESS`,
`PHONOTACTIC_STRUCTURE`. Isso evita tratar "saber que algo existe" como "saber
como soava" e evita tratar convenção didática como medição.

## Proposições centrais (todas candidatas)

- Inventário vocálico e correspondências: G4C001, G4C002.
- Quantidade: contrastiva; marcação diacrítica reportada (G4C003, G4C004,
  G4C026). Ausência de marca → `UNKNOWN`.
- Consonantismo: G4C010; dígrafos `tl`, `cu/uc`, `hu/uh` (G4C011–G4C014,
  G4C021), `c/z`, `tz/ch/x`, `p/t/c/qu/m/n/l/y` (G4C014–G4C016), Olmos
  `u/o`, `l/ll` (G4C027).
- Acento: regra penúltima e vocativo reportados por Launey (G4C017–G4C019).
- Sílaba e processos: estrutura (G4C020), coda sonorante (G4C022), assimilação
  nasal (G4C023), absolutivo (G4C024), reduplicação plural (G4C025), `h` em
  coda como `/w/` (G4C013/G4F029).
- Fronteiras metodológicas: dado moderno apenas como comparação (G4C028);
  `/.../` = análise, `[...]` = realização justificada (G4C029).

## Inferências proibidas (sentinelas do policy, 9)

O policy lista como proibido: tratar marca ausente como SHORT; tratar marca
ausente como ausência de saltillo; igualar ortografia à IPA estreita; usar
pronúncia moderna como prova clássica direta; tratar entrada do GDN como Witness
impresso inspecionado; reescrever `cu/uc` globalmente; gerar IPA em massa;
gerar áudio; aprovação pelo EXECUTION_AGENT. O validador `validate_gate4.py`
rejeita qualquer uma dessas situações.

## Registros produzidos

- 29 Claims (`data/phonology/claims/G4C001..G4C029`), todos `IN_REVIEW`, origem
  EXECUTION_AGENT registrada em `editorial_provenance`, `review_status:
  NOT_REVIEWED`.
- 28 Evidence (8 contextuais G4E001–G4E008 + 20 por-token G4E101–G4E150).
- 32 fixtures (G4F001–G4F032): 20 casos de lemma do piloto (capture do Gate 3
  reutilizado) e 12 casos de referência curta.
- 15 itens de integração (`integration_sample.yml`), teto de 15 lemmas; IPA
  `NOT_REVIEWED`.

## Decisões abertas

- Escopo e cronologia regionais da fonologia clássica (inclusive a crítica de
  Canger ao fechamento glotal pan-colonial, G4C006/G4C007).
- Realização fonética estreita (release lateral, qualidades vocálicas, laríngea).
- Domínios prosódicos de palavra/clítico e regra exata do acento.
- Curteza lexical onde a grafia não marca.
- Distinção diacrítico tipográfico vs. editorial nas entradas GDN.
- Inspeção independente dos testemunhos e páginas integrais de Karttunen,
  Lockhart e Andrews.
- Aprovação linguística especializada.

Nenhuma destas decisões promove inferência a fato atestado; permanecem em
`IN_REVIEW` até revisão externa do PRODUCT_OWNER/ORCHESTRATOR_REVIEWER.
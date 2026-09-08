# Gate 4 — Evidence Lock (Fonologia)

## Estado e finalidade

`status: CANDIDATE`

Este lock fixa as fontes e a mediação admitidas como Evidence fonológica no Gate 4.
Ele impede tratar agregador como Witness, dado moderno como prova clássica direta,
ausência de marca como prova de ausência, e notação modernizada como transcrição
estreita. O lock vale para os 29 Claims (`G4C001..G4C029`), os 32 casos
(`G4F001..G4F032`) e os 15 itens de integração. Não cria direitos nem substitui
a Política de Proveniência do Gate 2.

Toda Evidence declara `mediation_level`, `evidence_role`,
`direct_witness_inspected: false`, `rights_status` e `permitted_use: CAN_REFERENCE`.
Nenhuma presente evidence foi inspecionada em Witness impresso original neste Gate.

## Fontes admitidas

### A01 — Molina (1571), via GDN

- `source_id`: A01; `work`: *Vocabulario* (1571); acesso `UNAM / GDN`
  (`https://gdn.iib.unam.mx/`).
- Uso: forma e glosa histórica curta (`Metl`, `uentli`), registro da entrada.
- Regra: tradução PT-BR nunca é atribuída a Molina.

### A02 — Olmos (1547), via GDN

- `source_id`: A02; acesso `UNAM / GDN` (`Olmos`/`Olmos_G`).
- Uso: correspondências `u/o`, `l/ll`, exemplo vocativo (`nutza`, `calle`,
  `tlanellee`). A mediação Siméon/GDN é declarada (G4E008), nunca escondida.
- Regra: `u` não é automaticamente `/u/`; `l/ll` não recebe equivalência
  fonética automática.

### A03 — Rincón (1595), via GDN

- `source_id`: A03; acesso `UNAM / GDN` (Introdução; Libro V, cap. IV).
- Uso: contraste de quantidade `chichi` (G4E001). A nota prosódica é reportada
  como Evidence; não é convertida diretamente em IPA estreito.

### A04 — Carochi (1645), via GDN

- `source_id`: A04; acesso `UNAM / GDN` (entradas individuais e seções do texto).
- Uso: notação prosódica (macron, diacrítico) e glosa curta. Os diacríticos são
  preservados como Evidence reportada; vantagem de interpretação fonética
  definitiva fica fora do Gate 4.
- Os registros `G4E101..G4E150` reutilizam exatamente o capture do Gate 3
  (`access_basis: PROJECT_CAPTURE_REUSED`,
  `gate4_online_entry_reinspection: false`); não são uma nova inspeção online.

### D01 — Launey, *Introduction to Classical Nahuatl* (2011)

- `source_id`: D01; acesso: preview de distribuidor (Cambridge/PagePlace),
  pp. 4–8 e 13–20 (G4E003–G4E005). `mediation_level: MODERN_EDITION`,
  `evidence_role: SECONDARY_EVIDENCE`.
- Uso: inventário, acento/vocativo, saltillo, `tl`, coda `/w/` (`iuh`/`/iw/`),
  estruturas silábicas. É afirmação secundária; não é Witness clássico.

### D02 — Canger, *Estudios de Cultura Náhuatl* (2011)

- `source_id`: D02; acesso `UNAM` digital (pp. 244–251; G4E006–G4E007).
- Uso: hipótese regional do fechamento glotal, plural com reduplicação e
  saltillo (`ko:-koyo-’`). Contém crítica à generalização a todas as regiões
  coloniais; isso é preservado como contra-evidência em G4C006 (G4E006
  aparece em `evidence` e em `counterevidence`).

## Regras do lock

1. `direct_witness_inspected: false` em todas as Evidence; nenhuma entrada
   apresenta Witness impresso diretamente inspecionado.
2. `DIRECT_CLASSICAL_EVIDENCE` exige `direct_witness_inspected: true`; por isso
   nenhuma Evidence atual usa esse papel (todas são `REPORTED_CLASSICAL_EVIDENCE`
   ou `SECONDARY_EVIDENCE`).
3. Fonte moderna (variedades C01–C03 e comentário/síntese D01–D05) nunca é
   prova clássica direta; entra apenas como comparação ou reflexo (G4C028).
4. Ausência de diacrítico não prova ausência de contraste: `UNKNOWN` é estado
   válido; SHORT nunca é inferido por omissão (G4C003/G4C004, sentinelas do
   policy `classical_phonology_v1`).
5. `SEARCH_KEY`, ID do agregador e forma normalizada não são Evidence
   linguística.
6. Locator digital do GDN é preservado; folio interno não confirmado fica
   declarado, nunca inventado.
7. `h` pedagógico é convenção (G4C008), não medição fonética; não autoriza
   preencher saltillo lexical.
8. `comparison_group` (RINCON_CHICHI, GDN_NOHUIAN, COCHI_PLURAL) agrupa casos
   paralelos sem fundir sentidos nem grafias.

Data de acesso dos recursos: 2026-09-08 (contextuais) e 2026-09-03 (capture
do Gate 3 reutilizado).
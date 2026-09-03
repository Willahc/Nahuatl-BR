# Gate 3 — Relatório do corpus piloto

## Escopo e método

O piloto contém exatamente 50 Lemmas de `Classical Nahuatl`. A lista candidata
foi composta antes do preenchimento e escolhida para testar nomes concretos e
abstratos, verbos, termos culturalmente relevantes, polissemia, divergência de
glosas, variação gráfica e notação prosódica. Não constitui currículo nem
amostra estatística do léxico.

Foram feitas consultas pontuais no GDN, limitado aos candidatos. Para cada
Attestation, o registro preserva a Source histórica, Work, Edition/Witness
conforme o Witness Lock, forma paleográfica curta, glosa histórica curta e ID da
entrada. O GDN permanece `aggregator: B01`; não foi promovido silenciosamente a
Source primária. O material do Florentine Codex é apenas uma referência de
ocorrência/identificador `CAN_REFERENCE`, sem cópia de transcrição ou tradução.

## Os 50 Lemmas

`amoxtli`, `atl`, `calli`, `centli`, `chilli`, `cihuatl`, `citlalin`,
`cochi`, `cocotona`, `conetl`, `cua`, `cuahuitl`, `cuicatl`, `etl`, `eztli`,
`icxitl`, `ilhuicatl`, `io`, `itta`, `itoa`, `ixtli`, `iztatl`, `maitl`,
`mati`, `metl`, `metztli`, `milli`, `miqui`, `nacatl`, `nacaztli`, `nantli`,
`nemi`, `nonotza`, `omitl`, `oquichtli`, `pepena`, `pilli`, `tatli`, `tentli`,
`teotl`, `tequitl`, `tetl`, `tlacatl`, `tlacuilolli`, `tlalli`, `tlatoa`,
`tlatolli`, `tlazotla`, `tlaolli`, `xochitl`.

## Cobertura calculada

- 50/50 com tradução editorial PT-BR;
- 50/50 com Attestation histórica e Source/Work;
- 48/50 com duas Sources históricas;
- 47/50 com referência contextual em `CF_INDEX` ou `Sahagún Escolio`;
- 0/50 com texto do contexto histórico diretamente inspecionado neste piloto;
- 23/50 com Evidence de notação relevante ao comprimento vocálico;
- 10/50 com Evidence de notação relevante ao saltillo;
- 12/50 com informação morfológica limitada ao frame de citação reportado;
- 0/50 com `TRUE_CONTRADICTION`; três divergências foram classificadas separadamente.

As contagens são produzidas por `scripts/validate_gate3.py`; não são mantidas
manualmente nos arquivos de métrica e índice.

## Decisões editoriais

1. A forma de exibição é editorial; cada `SOURCE_FORM` permanece associada à
   Attestation da qual veio.
2. `PEDAGOGICAL_FORM` permanece `UNKNOWN` em todo o piloto: não se converteu a
   notação de Carochi em macrons ou `h`.
3. Diacríticos de Carochi foram preservados como Evidence reportada. Os campos
   fonológicos continuam `NOT_REVIEWED`.
4. Traduções PT-BR são Claims `EDITORIAL`, derivadas da glosa histórica e em
   `IN_REVIEW`.
5. O Locator digital do GDN é preservado; Locator interno ausente recebe motivo
   explícito, sem folio inventado.

## Ambiguidades e divergências

- `pilli`: Molina registra pessoa nobre, enquanto a entrada de Carochi
  selecionada, `pil[li]`, reporta filho/filha; a identidade lemática precisa de
  revisão.
- `tlacatl`: a glosa ampla de Molina e a glosa específica da entrada de Carochi
  não foram fundidas.
- `mati`: frames de citação e polaridade das glosas selecionadas divergem; o
  piloto preserva ambas e mantém revisão pendente.
- `io` possui apenas Carochi entre as Sources históricas fixadas.
- `metl` possui apenas Molina entre as Sources históricas fixadas.

## Caso Olmos

Foi localizado `centli` no registro `Olmos_G` 20313 do GDN. O caso foi incluído
na fixture do Gate 2 como `G2-026-olmos-centli`. O Locator digital é verificável;
o folio interno da Edition Siméon/Codex Colbert permanece `NOT_REVIEWED`.

## Limites do modelo observados

- O esquema precisa distinguir com mais precisão Locator do agregador e Locator
  interno do Witness.
- A distinção entre contradição, polissemia e frames de citação ainda depende de
  revisão humana.
- `PhonologicalAnalysis` precisa representar notação histórica antes de sua
  interpretação fonológica.
- A classe gramatical e a ontologia morfológica continuam insuficientemente
  definidas para preenchimento sistemático seguro.

Propõe-se que o revisor considere futuramente uma entidade de `AccessPath` ou
campos equivalentes para a cadeia agregador→Source→Witness→Locator. O Modelo
Canônico não foi alterado automaticamente para acomodar essa proposta.

## Direitos e limites operacionais

Foram copiados apenas fragmentos lexicográficos curtos necessários ao piloto e
identificadores. Nenhuma base, corpus ou transcrição moderna foi ingerida. C01
Hueyapan não foi usado como Evidence. O piloto é material de revisão, não uma
conclusão jurídica nem uma publicação canônica.

## EXTERNAL REVIEW REMEDIATION

`ORCHESTRATOR_REVIEWER_DECISION: PASS_AFTER_REMEDIATION`

`GATE_3_STATUS: CLOSED`

A revisão externa determinou que diferenças de glosa, sentido ou frame não
constituem automaticamente contradição. A modelagem foi corrigida assim:

- `pilli`: `LEXICAL_IDENTITY_UNRESOLVED`, com
  `POLYSEMY_CANDIDATE`/`HOMONYMY_CANDIDATE` como alternativas não decididas;
- `tlacatl`: `SOURCE_GRANULARITY_DIFFERENCE`, com
  `SEMANTIC_VARIATION` apenas como candidato;
- `mati`: `FRAME_VARIATION`;
- nenhum caso foi classificado como `TRUE_CONTRADICTION`.

As métricas recalculadas são `with_conflicting_claims: 0`,
`with_semantic_variation: 1`, `with_frame_variation: 1` e
`with_lexical_identity_unresolved: 1`.

O antigo `with_context` foi dividido em `with_context_reference: 47` e
`with_context_text_inspected: 0`. Um ID de `CF_INDEX` ou `Sahagún Escolio` não
é apresentado como texto contextual lido.

O antigo `with_primary_attestation` foi substituído por
`with_historical_attestation: 50`, `with_direct_witness_attestation: 0` e
`with_aggregator_mediated_attestation: 50`. As 98 Attestations possuem
`mediation_level: AGGREGATOR`; a Work histórica permanece identificada, sem
afirmação de inspeção direta do Witness.

Fontes institucionais consultadas: [GDN](https://gdn.iib.unam.mx/),
[Olmos](https://gdn.iib.unam.mx/textos/olmos),
[Rincón](https://gdn.iib.unam.mx/textos/rincon) e
[Carochi](https://gdn.iib.unam.mx/textos/carochi). Data de acesso: 2026-09-03.

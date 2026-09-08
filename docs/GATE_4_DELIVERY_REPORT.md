# Relatório de entrega do Gate 4

Executor: `EXECUTION_AGENT`. Este relatório documenta a entrega parcial do Gate 4
(modelo candidato, Claims, Evidence, fixtures e validação estrutural) e **não**
constitui aprovação ou encerramento do Gate. A aprovação cabe ao `PRODUCT_OWNER`
humano, após recomendação do `ORCHESTRATOR_REVIEWER`. Gate 5 não foi iniciado.

`DELIVERY_STATUS: IN_REVIEW`

## Escopo autorizado

Produzir, sem gerar áudio nem preencher IPA dos 50 lemmas em massa:

1. Modelo candidato de fonologia clássica (camadas, dimensões de certeza, política
   de representação, inferências proibidas).
2. Claims fonológicas com modalidade epistêmica e proveniência editorial.
3. Evidence records com mediação declarada (GDN, edições modernas).
4. Fixtures de casos para validação futura.
5. Integração amostral lemma → fixture → Evidence → Claims.

## Entregáveis

| Entregável | Arquivo | Conteúdo |
|---|---|---|
| Política candidata | `data/policies/classical_phonology_v1.yml` | Camadas, dimensões, inventários candidatos, correspondências, inferências proibidas; `DRAFT`, v1.0.0-draft.1 |
| Claims fonológicas | `data/phonology/claims/G4C001..G4C029` | 29 Claims (`IN_REVIEW`), origem EXECUTION_AGENT registrada |
| Evidence | `data/phonology/evidence.yml` | 28 registros: 8 contextuais (G4E001–G4E008) + 20 por-token (G4E101–G4E150) |
| Fixture | `data/fixtures/gate4_phonology_cases.yml` | 32 casos (G4F001–G4F032), status `IN_REVIEW` |
| Integração amostral | `data/phonology/integration_sample.yml` | 15 itens (12 lemma-cases + 3 adicionados nesta entrega) |
| Modelo de áudio (conceitual) | `data/phonology/audio_model.yml` | Tipos de áudio e campos; zero instâncias/arquivos |
| Baseline | `data/phonology/gate3_baseline.yml` | Registro do corpus aprovado no Gate 3 |
| Registro de fontes modernas | `data/source_registry/D01..D05` | Launey, Canger, Karttunen, Lockhart/Andrews (verificação bibliográfica) |

## Claims fonológicas (29)

Temas cobertos:

- **Inventário vocálico**: G4C001, G4C002.
- **Quantidade / marcas**: G4C003, G4C004, G4C026.
- **Saltillo (existência, realização, convenção pedagógica)**: G4C005–G4C009.
- **Inventário consonantal**: G4C010.
- **Correspondências grafema→fonema**: G4C011 (tl), G4C012 (cu/uc), G4C013 (hu/uh),
  G4C014 (c/z), G4C015 (tz/ch/x), G4C016 (p/t/c/qu/m/n/l/y), G4C027 (Olmos u, l/ll), G4C008.
- **Acento**: G4C017–G4C019.
- **Sílaba e processos**: G4C020 (estrutura), G4C021 (dígrafos), G4C022 (coda
  sonorante), G4C023 (assimilação nasal), G4C024 (absolutivo), G4C025 (reduplicação).
- **Fronteiras metodológicas**: G4C028 (dado moderno), G4C029 (IPA // vs []).

Todas as Claims nascem `IN_REVIEW` por instrução explícita do PRODUCT_OWNER
(exceção registrada no AGENTS.md), com origem EXECUTION_AGENT. Revisão humana
individual não está documentada.

## Evidence records (28)

- Contextuais: G4E001 (Rincón via GDN), G4E002 (Carochi via GDN), G4E003 (Launey),
  G4E004 (Launey sílaba), G4E005 (Launey absolutivo), G4E006 (Canger), G4E007
  (Canger plural), G4E008 (Olmos via GDN).
- Por-token (reaproveitamento do capture do Gate 3, `PROJECT_CAPTURE_REUSED`, sem
  re-inspeção online): G4E101–G4E150 para 20 lemmas com notação diacrítica.
- Toda Evidence declara `mediation_level`, `direct_witness_inspected: false`,
  `rights_status` e `permitted_use: CAN_REFERENCE`.

## Fixture (32 casos)

- G4F001–G4F020: casos dos lemmas do piloto (nota `Gate 3 capture reused exactly;
  not a new historical Witness inspection`).
- G4F021–G4F032: casos de referência curta (Rincón chichi LONG/SHORT, Olmos
  u/o e l/ll, Carochi nohuian/nohuiän, Launey acento/tl/uh/saltillo, Canger plural).
- `phonemic_candidate` e `phonetic_candidate` permanecem `NOT_REVIEWED`, exceto
  G4F029 (`/iw/` reportado por Launey para iuh) e G4F021/G4F022
  (`vowel_length` LONG/SHORT reportados por Rincón).
- O caso chichi (G4F021/G4F022) ilustra contraste de quantidade com grafia idêntica,
  sem fundir sentidos (comparison_group `RINCON_CHICHI`).

## Integração amostral (15 itens)

Itens vinculados:

- L0001 (ämoxtli), L0002 (ätl): LONG em vogal marcada.
- L0003 (calli), L0008 (cochi), L0011 (qua), L0012 (quahuitl): UNKNOWN onde não há marca.
- L0005 (chïlli), L0027 (mïlli): LONG em ï, com discussão de ll.
- L0018 (iô), L0033 (nònotza), L0038 (tà[tli]), L0044 (tlàcuilölli): saltillo
  PRESENT na notação grave.
- L0026 (métztli): SHORT em é (candidato, revisão tipográfica pendente).
- L0050 (xöchitl), L0044 (tlàcuilölli): LONG em ö.
- Nenhum `phonemic_ipa`/`phonetic_ipa` preenchido nos itens; `NOT_REVIEWED` é o
  padrão. `max_lemmas` 15 é o teto da amostra.

## Regras respeitadas

- `SOURCE_FORM` imutável; código-fonte não modificado.
- Sem tradução, IPA, duração ou saltillo inventados.
- Ausência de marca → `UNKNOWN`, nunca SHORT por omissão.
- Sem mistura de variante moderna com Clássico.
- Claims sugeridas por IA com origem registrada.
- Sem áudio, sem média fonética, sem silabificador, sem banco, sem API, sem Gate 5.

## Validação estrutural

Script de validação de referências internas executado:

- Todas as 28 Evidence IDs referenciadas por Claims existem.
- Todas as referenceiras de Evidence das fixtures resolvem.
- Integração: todos os `claim_ids` existem; todos os `evidence` resolvem.
- Política: todos os `claim_id` referenciados existem (29/29).
- `source_id` (A01–A04, D01–D02) presentes no `source_registry`.

Verificação JSON/YAML: todos os arquivos novos são JSON válido; registros de fonte
seguem o formato YAML plano já usado no repositório.

## Decisões abertas (para revisão humana)

- Escopo e cronologia regionais da fonologia clássica.
- Realização fonética estreita (release lateral, qualidades vocálicas, laríngea).
- Domínios prosódicos de palavra/clítico.
- Curteza lexical onde a grafia não marca.
- Distinção entre diacrítico tipográfico e editorial nas entradas GDN.
- Inspeção independente dos testemunhos históricos.
- Páginas integrais de Karttunen, Lockhart e Andrews.
- Aprovação linguística especializada.
- Gate 5 permanece não autorizado.

## Comandos de aceitação do Gate 4

```text
python scripts/validate_gate3.py --check
python scripts/validate_gate4.py --check
python -m unittest discover -s tests -p "test_*.py"
git diff --check
```

A infraestrutura de validação dos artefatos de fonologia foi entregue
posteriormente nesta fase (`scripts/validate_gate4.py`, testes T01–T15 e o
relatório de auditoria em `docs/GATE_4_AUDIT_REPORT.md`). Os três validam o
corpus do Gate 3 e os novos artefatos; a aprovação do conteúdo permanece do
PRODUCT_OWNER.
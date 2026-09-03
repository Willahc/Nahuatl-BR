# Gate 3 — Witness Lock

## Estado e finalidade

`status: LOCKED_FOR_PILOT`

Este documento fixa as Editions e Witnesses permitidos no piloto de 50 Lemmas.
O lock evita misturar exemplares, transcrições modernas e Works históricas. O
GDN é apenas agregador de descoberta e consulta: cada Attestation conserva a
Work subjacente e o Locator digital da entrada. Quando o folio interno não foi
confirmado, usa-se `NOT_REVIEWED`, nunca um Locator inventado.

## A01 — Molina

- `source_id`: A01
- `work`: *Vocabulario en lengua castellana y mexicana / mexicana y castellana* (1571)
- `edition`: impressão de 1571; representação consultada no GDN como `Molina_2`
- `witness`: entrada individual do GDN derivada de Molina; Witness impresso exato `NOT_REVIEWED`
- `institution`: UNAM/IIB (agregador); Work de Alonso de Molina
- `URL`: https://gdn.iib.unam.mx/
- `rights_status`: `PUBLIC_DOMAIN_WORK`; camadas modernas do GDN `UNKNOWN_RIGHTS`
- `allowed_use`: citação pontual, forma/glosa histórica curta e referência; sem ingestão da camada moderna
- `locator_scheme`: folio quando exposto; senão `GDN entry <id>` com motivo do Locator interno ausente
- `notes`: fonte lexical primária do piloto; nunca atribuir tradução PT-BR a Molina.

## A02 — Olmos

- `source_id`: A02
- `work`: *Arte para aprender la lengua mexicana* (1547)
- `edition`: Rémi Siméon, 1875, baseada no Codex Colbert e anotada pelo Codex Maisonneuve
- `witness`: registro `Olmos_G` do GDN; Witness manuscrito exato por entrada `NOT_REVIEWED`
- `institution`: UNAM/IIB (agregador); testemunhos descritos pela BnF/Library of Congress
- `URL`: https://gdn.iib.unam.mx/textos/olmos
- `rights_status`: `PUBLIC_DOMAIN_WORK`; transcrição/normalização GDN `UNKNOWN_RIGHTS`
- `allowed_use`: `CAN_REFERENCE` para a camada GDN; citação pontual do registro e metadados
- `locator_scheme`: `GDN Olmos_G entry <id>`; Locator interno de Siméon/manuscrito `NOT_REVIEWED`
- `notes`: o caso `centli`, entrada 20313, satisfaz a tentativa de Locator digital verificável sem fabricar folio.

## A03 — Rincón

- `source_id`: A03
- `work`: *Arte mexicana* (1595)
- `edition`: reedição Antonio Peñafiel, 1885, usada pelo GDN
- `witness`: registros individuais `Rincón` do GDN; imagens de Utah não copiadas
- `institution`: UNAM/IIB (agregador); J. Willard Marriott Library (Witness digital auditado no Gate 1)
- `URL`: https://gdn.iib.unam.mx/textos/rincon
- `rights_status`: `PUBLIC_DOMAIN_WORK`; surrogate Utah e camada GDN `UNKNOWN_RIGHTS`
- `allowed_use`: referência e metadados pontuais; sem cópia de surrogate
- `locator_scheme`: `GDN entry <id>`; página histórica `NOT_REVIEWED` salvo confirmação explícita
- `notes`: usado como comparação; não se converte sua nota prosódica diretamente em IPA.

## A04 — Carochi

- `source_id`: A04
- `work`: *Arte de la lengua mexicana con la declaración de los adverbios della* (1645)
- `edition`: Work de 1645; vocabulário GDN elaborado com fac-símile de 1983 e consulta a Lockhart quando necessário
- `witness`: entrada individual `Carochi` do GDN; HTML Cervantes apenas `CAN_REFERENCE`
- `institution`: UNAM/IIB (agregador); Biblioteca Virtual Miguel de Cervantes (Edition auditada)
- `URL`: https://gdn.iib.unam.mx/textos/carochi
- `rights_status`: `PUBLIC_DOMAIN_WORK`; Editions/transcrições modernas `UNKNOWN_RIGHTS`
- `allowed_use`: marcação prosódica e glosa curta por referência pontual; sem cópia extensiva
- `locator_scheme`: `GDN entry <id>`; seção da Arte apenas quando explicitamente exposta
- `notes`: diacríticos são preservados como Evidence reportada; sua interpretação fonética definitiva fica fora do Gate 3.

## Regras do lock

1. O agregador nunca substitui `Source`, `Work`, `Edition`, `Witness` e `Locator`.
2. Nenhuma transcrição ou tradução moderna protegida é copiada em massa.
3. `CAN_REFERENCE` permite registrar URL, identificador e existência de ocorrência, não ingerir o componente.
4. O Digital Florentine Codex é usado apenas por metadado/identificador de ocorrência; a transcrição moderna não é copiada.
5. Qualquer troca de Edition/Witness exige revisão documentada deste lock.

Data de acesso dos recursos: 2026-09-03.

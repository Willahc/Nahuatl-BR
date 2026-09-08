# Proveniência editorial mínima do piloto

Esta política complementa Provenance, sem criar uma entidade concorrente.
Aplica-se a Claims e Translations do piloto e à captura futura de sua trajetória.
Não reabre Gate 3 nem autoriza Gate 4.

## Registro atual

Cada Claim e Translation possui `editorial_provenance` com:

- `actor_role`, `actor_id`: papel e identidade registrados;
- `tool`, `tool_version`: ferramenta e versão histórica comprovada;
- `timestamp`: instante editorial do objeto, quando conhecido;
- `action`, `from_state`, `to_state`: natureza do registro e estados;
- `created_in_commit`: primeiro commit Git em que o objeto é verificável;
- `history_status`: disponibilidade da trajetória anterior;
- `review_status`: situação da revisão individual documentada;
- `notes`: limites e contexto de interpretação.

O histórico foi conferido em `f21b642`: todos os 129 IDs de Claims e os 50 IDs
de Translation já existiam com estado `IN_REVIEW`. O commit completo é guardado
nos objetos. A origem `EXECUTION_AGENT` é sustentada pela proveniência original;
Codex é a ferramenta identificada pela documentação do projeto.

`action: FIRST_VERSIONED_STATE` descreve uma observação do histórico, não uma
transição editorial. `from_state: NOT_RECORDED` e
`history_status: NOT_RECORDED_PRIOR_TO_FIRST_COMMIT` não afirmam passagem por
`DRAFT`. A regra para novas sugestões de IA continua sendo nascimento em DRAFT.
Não foi reconstruída retroativamente uma trajetória para satisfazer essa regra.

`actor_id`, `tool_version` e `timestamp` são `UNKNOWN`: a data do commit ou a data
geral de captura não é promovida a timestamp editorial individual. Não se usa a
versão instalada atualmente como prova da versão histórica.

`review_status: NOT_REVIEWED` significa ausência de revisão humana individual
documentada neste registro; não é declaração sobre eventos externos desconhecidos.
Não há atribuição de tradutor ou revisor humano. As Claims e Translations mantêm
`IN_REVIEW`; aprovação estrutural do Gate não as promove a APPROVED/PUBLISHED.

## Eventos futuros

Uma mudança editorial futura deve registrar seu próprio evento de Provenance:
`actor_role`, `actor_id`, `tool`, `tool_version`, `timestamp`, `action`,
`from_state`, `to_state`, `commit` e `notes`. O commit pode ser registrado depois
da criação do evento, sem tentar incluir o hash do próprio commit em si mesmo.
Eventos anteriores são preservados; `created_in_commit` não muda a cada edição.

`UNKNOWN` indica valor desconhecido; `NOT_REVIEWED`, avaliação ainda não
documentada; `NOT_RECORDED`, evento/campo histórico não registrado. Esses valores
não são intercambiáveis. Nenhum deles constitui Evidence linguística.

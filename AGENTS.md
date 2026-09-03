# Instruções para agentes e colaboradores

Estas regras valem para todo o repositório.

## Escopo atual

Os Gates 0, 1, 2 e 3 estão encerrados. O Gate 4 está `NOT_STARTED`. Não iniciar
modelo fonológico, banco de dados, pipeline, API,
frontend, sistema de estudo, áudio ou escrita glífica até aprovação explícita
do Gate correspondente. Não baixar, copiar, raspar ou ingerir fontes externas
sem autorização.

## Regras linguísticas obrigatórias

1. Nunca misturar Náhuatl Clássico com Hueyapan ou outra variante moderna.
2. Nunca inventar tradução, IPA, duração vocálica, saltillo, etimologia,
   segmentação, análise morfológica ou exemplo.
3. Preservar exatamente a forma encontrada na fonte; toda normalização deve
   ocupar campo separado e declarar a convenção usada.
4. Tratar tradução PT-BR como afirmação editorial versionada, não como parte
   intrínseca do lemma.
5. Exigir proveniência no nível da afirmação, incluindo localização verificável
   quando disponível.
6. Registrar em cada Claim uma modalidade epistêmica entre `OBSERVED`,
   `REPORTED`, `INFERRED`, `RECONSTRUCTED` e `EDITORIAL`, sem confundi-la com
   tipo da fonte, confiança ou estado editorial.
7. Preservar análises conflitantes como registros paralelos; não escolher ou
   fundir silenciosamente.
8. Marcar desconhecido como desconhecido. Ausência de dado não é evidência de
   ausência linguística.
9. Áudio deve identificar falante, variante e um tipo entre `HUMAN_NATIVE`,
   `MODERN_READING`, `HISTORICAL_RECONSTRUCTION` e `SYNTHETIC`.
10. Claims sem Evidence só podem existir como `DRAFT` ou `QUARANTINED` quando a
    classe exigir evidência; nunca podem ser `PUBLISHED` ou canônicas nessa
    condição.
11. Claims sugeridas por IA nascem como `DRAFT`, registram sua origem e nunca
    constituem evidência linguística primária.
12. `SOURCE_FORM` é imutável; `NORMALIZED_FORM` nunca a substitui.
13. `PEDAGOGICAL_FORM` nunca é apresentada como `DIPLOMATIC_FORM`.
14. `SEARCH_KEY` serve apenas à recuperação e nunca é Evidence linguística.
15. Ausência de Diacritic não prova ausência de contraste fonológico; não
    inferir comprimento vocálico, saltillo ou IPA sem Evidence.
16. Não converter Modern Variety em Classical Nahuatl nem usar Hueyapan para
    preencher lacunas clássicas.

## Disciplina de mudança

- Manter decisões normativas em `docs/` e registrar decisões ainda abertas.
- Fazer alterações pequenas, auditáveis e acompanhadas por validação adequada.
- Não modificar arquivos-fonte originais; derivados futuros devem ter hash e
  cadeia de transformação.
- Não confirmar licença, autoria, cobertura ou método de extração sem
  verificação documental.
- Não promover inferência ou reconstrução à condição de fato atestado.
- Não avançar de gate sem registrar critérios de entrada, saída e aprovação.
- O Codex atua como `EXECUTION_AGENT` e não aprova o próprio Gate. Somente o
  `PRODUCT_OWNER` humano autoriza ou rejeita progressão, após recomendação do
  `ORCHESTRATOR_REVIEWER`.

## Convenções futuras

- Identificadores internos devem ser estáveis e não carregar significado
  linguístico mutável.
- Vocabulários controlados devem ser versionados.
- Datas devem usar ISO 8601 quando conhecidas; intervalos e datas aproximadas
  devem manter sua incerteza explicitamente.
- Novos campos e entidades devem preservar a possibilidade de múltiplas
  variantes, fontes, análises e traduções por forma.

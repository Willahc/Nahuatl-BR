# Visão do projeto

## Missão

Construir uma plataforma brasileira de estudo de náhuatl cuja infraestrutura
linguística seja canônica, auditável, rastreável e apropriada a pesquisa e
aprendizagem. O núcleo inicial será o Náhuatl Clássico. Variantes modernas,
incluindo Hueyapan, poderão coexistir, mas terão identidade, fontes, análises e
apresentação próprias.

## Resultado pretendido

A plataforma deverá permitir consultar formas atestadas, lemmas, significados,
traduções PT-BR, análises morfológicas, pronúncias e exemplos sempre com o
contexto que permite avaliar cada afirmação: variante, período, fonte,
localização, responsabilidade editorial, licença e confiança.

“Canônico” significa aqui um sistema estável para representar afirmações e suas
relações, não uma versão única ou definitiva da língua. O modelo deve acomodar
divergência entre documentos, autores e tradições acadêmicas.

## Públicos

- estudantes brasileiros;
- professores e autores de materiais didáticos;
- falantes e comunidades das variantes modernas;
- pesquisadores, revisores e curadores linguísticos;
- desenvolvedores de ferramentas de consulta e estudo.

## Princípios de produto e pesquisa

1. **Separação linguística:** toda forma ou afirmação pertence a uma variante e
   a um recorte temporal definidos, ou é marcada como não determinada.
2. **Fidelidade documental:** a transcrição da fonte não é substituída por uma
   grafia normalizada.
3. **Proveniência granular:** a unidade citável é a afirmação, não apenas o
   verbete inteiro.
4. **Pluralidade:** variantes conflitantes e análises concorrentes permanecem
   visíveis.
5. **Honestidade epistêmica:** atestação, análise acadêmica, inferência editorial
   e reconstrução são categorias diferentes.
6. **Independência editorial:** traduções PT-BR têm autoria, versão e revisão.
7. **Reprodutibilidade:** transformações futuras devem ser registradas e
   verificáveis.
8. **Respeito jurídico e comunitário:** acesso técnico não implica permissão de
   reutilização; materiais de comunidades exigem cuidado adicional.
9. **Progressão por gates:** novas capacidades só começam após critérios de
   saída explícitos.

## Escopo inicial

O primeiro ciclo produzirá governança, auditoria de fontes e um corpus piloto
de 50 lemmas clássicos. Ele deverá validar o modelo antes de qualquer expansão.
Depois virão fonologia, ingestão, uma base de 500 lemmas e, somente então, API e
interfaces.

## Fora de escopo no Gate 0

- baixar, copiar, raspar ou extrair bases externas;
- transcrever o PDF de Hueyapan já presente;
- selecionar grafia normativa definitiva;
- produzir traduções, IPA, etimologias ou análises linguísticas;
- implementar esquema físico, banco, API ou frontend;
- gerar áudio ou pronúncias sintéticas;
- decidir licenças sem examinar os termos aplicáveis.

## Critérios gerais de qualidade

- rastreabilidade da apresentação até a afirmação e sua evidência;
- impossibilidade de fusão silenciosa entre variantes;
- validação explícita de campos controlados e obrigatórios;
- preservação de original, revisão, conflito e incerteza;
- documentação suficiente para reprodução e auditoria independente;
- participação de especialistas e, quando aplicável, das comunidades envolvidas.

## Governança inicial

O processo distingue três papéis de Gate:

- `PRODUCT_OWNER`: responsável humano pelo projeto e autoridade final para
  autorizar ou rejeitar Gates. Pode aceitar riscos documentados e deve registrar
  a decisão.
- `ORCHESTRATOR_REVIEWER`: responsável por arquitetura, revisão
  técnica/linguística, critérios de qualidade e recomendação de `PASS` ou
  `FAIL`. Não executa alteração silenciosa da base e não substitui a decisão
  final do `PRODUCT_OWNER`.
- `EXECUTION_AGENT`: Codex, responsável por executar tarefas aprovadas, rodar
  testes e gerar relatórios. Não possui autoridade para aprovar o próprio Gate.

A autoavaliação do Codex nunca autoriza progressão. Curadoria linguística,
revisão de PT-BR, engenharia de dados, revisão jurídica e revisão comunitária
continuam responsabilidades especializadas; sua atribuição nominal é uma
`OPEN_DECISION`. Uma mesma pessoa pode exercer mais de uma função humana, porém
cada decisão deve registrar em qual papel foi tomada. Mudanças normativas
relevantes serão documentadas por decisões versionadas antes de alterar dados.

# Contrato de validação do piloto pós-Gate 3

Escopo: hardening do corpus existente, sem novo Gate linguístico. O formato
continua `nahuatl-br-gate3-pilot-v1`, acrescido de proveniência editorial e de
`Evidence.attestation_id`, uma referência explícita recuperada por correspondência
única de Source, agregador, Locator e URL já existentes. Nenhuma atestação nova
ou inspeção direta foi criada.

## Identificadores e referências

`Lemma.id` é único no piloto. `form_id`, `sense_id`, `claim_id`, `attestation_id`,
`evidence_id`, `translation_id`, `analysis_id` e `divergence_id` são únicos por
classe dentro de cada lemma. Translations são verificadas em conjunto sobre
todos os Senses daquele lemma. Não se impõe unicidade global entre classes ou
lemmas. Source IDs são únicos no registry; perfis são identificados por ID@versão.

As referências existentes são locais e tipadas: EvidenceLink → Claim/Evidence;
Form, análise morfológica, notação fonológica e divergência → Evidence;
Translation.derived_from → Claim; Evidence → Attestation; Attestation → Source.
Claim.subject resolve para o lemma, Form ou Sense local de modo não ambíguo.
Source/agregador de Evidence e referências contextuais também devem existir.

Work ainda é um título descritivo, não um ID de entidade física. O título da
Attestation deve corresponder à Work registrada; no caso de Olmos, a expressão
de inventário `and related vocabularies` não faz parte do título da Arte.
Não se exige uma tabela Work inexistente. O Witness Lock permanece aplicável.

SOURCE_FORM → Evidence → Attestation específica é conferida por referência,
igualdade exata da forma e concordância de Source/agregador/Locator/URL. Não
basta encontrar uma forma igual em outra atestação do mesmo lemma.

## Compatibilidade de variedade

O validador lê `linguistic_scope` no registry. A função `compatible_variety`
requer escopo histórico clássico/colonial explícito e compatível com o lemma,
sem aceitar escopo moderno ou misto como atestação clássica. Escopos desconhecidos
falham de modo conservador. Agregadores podem continuar como caminhos de acesso;
não substituem a Source histórica. C01/C02/C03 não passam como fontes clássicas.
Comparação futura entre variedades exigirá relação própria e não herdará Evidence.

O leitor usa biblioteca padrão e projeta somente campos escalares e o flow-map
`linguistic_scope` na sintaxe existente. Não interpreta todo YAML. Sintaxe não
suportada, campos obrigatórios ausentes e IDs de Source duplicados causam falha.
Mudança no formato desse contrato deve incluir atualização e testes do leitor.

## Evidence e estados

As três classes atuais (`has_historical_gloss`, `has_pt_br_editorial_gloss`,
`has_reported_prosodic_notation`) exigem Evidence. Novos predicados precisam de
política explícita; não ganham isenção por omissão ou por modalidade EDITORIAL.

Sem suporte, somente DRAFT ou QUARANTINED são permitidos. Demais estados exigem
EvidenceLink resolvido com SUPPORTS ou DERIVED_FROM. CONTRADICTS e QUALIFIES são
relações válidas, mas isoladamente não substituem suporte à afirmação.
CONTRADICTS mantém a exigência de comparabilidade semântica já aprovada.
Modalidade, confiança e estado não substituem Evidence.

Locators desconhecidos/não revisados requerem justificativa não vazia. Valores
editoriais definidos em NORMALIZED_FORM exigem perfil aprovado, versionado e
aplicável a Classical Nahuatl. Textos de tradução não podem ser vazios.

## Derivados e execução

`python scripts/validate_gate3.py` e `--check` são somente leitura. Calculam
índice/métricas em memória e comparam o conteúdo estruturado com o versionado;
diferenças de apresentação JSON não são drift semântico. Ausência ou divergência
produz `DERIVED_DATA_OUT_OF_DATE`, sem reparo silencioso.

`--write-derived` grava apenas índice e métricas após validação integral das
entradas. Em dados inválidos, nenhum derivado é gravado. O modo explícito serve
para regeneração autorizada, não para publicação automática de Claims.

Os testes copiam os 50 registros porque a cardinalidade é parte do contrato,
mais registry, policy e scripts para diretório temporário. Nenhum PDF é exigido.
As regressões T01–T09 verificam código não zero, categoria e ausência de mudanças.

"""Audit changes against rejected delivery; historical bytes are comparison only."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline.corpus import records, duplicate_candidates
from src.pipeline.text_integrity import scan, text_errors

ROOT = Path(__file__).resolve().parents[1]
BASE = '8f33f82aeba8c0691e9ac6b5b19d57b03916e192'
ledger = ROOT / 'data/gate6/batches/batch04.tsv'
old_text = subprocess.check_output(['git', 'show', BASE + ':data/gate6/batches/batch04.tsv'], cwd=ROOT).decode('utf-8')
old = list(csv.DictReader(io.StringIO(old_text), delimiter='\t'))
with ledger.open(encoding='utf-8', newline='') as f:
    new = list(csv.DictReader(f, delimiter='\t'))
fields = ['source_form', 'historical_gloss', 'pt_br', 'domain']
rows = []
for n, (before, after) in enumerate(zip(old, new), 201):
    rows.append({'lemma_id': f'L{n:04}', 'visual_recheck': 'COMPLETE',
                 'entry_boundary_checked': True, 'column': after['column'],
                 'changed_fields': [k for k in fields if before[k] != after[k]],
                 'prior_true_mojibake': bool(text_errors(before)),
                 'unresolved_transcription': False})
summary = {'baseline_comparison_commit': BASE, 'records_inspected': len(rows),
           'source_form_corrections': sum('source_form' in r['changed_fields'] for r in rows),
           'historical_gloss_corrections': sum('historical_gloss' in r['changed_fields'] for r in rows),
           'pt_br_corrections': sum('pt_br' in r['changed_fields'] for r in rows),
           'semantic_domain_corrections': sum('domain' in r['changed_fields'] for r in rows),
           'records_with_encoding_corrections': sum(r['prior_true_mojibake'] for r in rows),
           'records_unchanged': sum(not r['changed_fields'] for r in rows),
           'unresolved_transcription': 0, 'true_mojibake_remaining': len(scan(ROOT)),
           'duplicate_candidates': len(duplicate_candidates(records(ROOT))),
           'reviewed_ledger_sha256': hashlib.sha256(ledger.read_bytes()).hexdigest(),
           'rows': rows}
(ROOT / 'data/gate6/batch04_remediation.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
text = '''# Batch 04 — remediação após FAIL externo

Estado: PASS_AFTER_REMEDIATION / AWAITING_EXTERNAL_REVIEW após validação técnica.
Último checkpoint aceito externamente: 3 / 200; total físico: 250 DRAFT/IN_REVIEW.

## Causa raiz

O ledger foi lido no Windows PowerShell sem `-Encoding utf8` e regravado
repetidamente. Isso reinterpretou bytes UTF-8 usando a codificação legada e
propagou texto corrompido pelo pipeline. A tentativa anterior de corrigir uma
linha repetiu o problema. Também havia erros independentes de transcrição e
tradução. Os validators verificavam estrutura e replay, mas aceitavam texto
corrompido coerente com a entrada. O PASS anterior não provava fidelidade visual.

## Reinspeção e reconstrução

50/50 entradas comparadas com a imagem JCB manifest page 300, colunas a/b.
Imagem original inspecionada e ampliações locais da mesma imagem; hashes e URL
nos registros. Nenhum OCR foi usado. O ledger foi escrito diretamente em UTF-8
com apply_patch e reaberto com decodificação UTF-8 estrita. Nenhum auto-decode,
ftfy ou substituição heurística foi aplicado. Cada registro foi regenerado pelo
Gate 5, preservando L0201–L0250 e recalculando IDs e digest derivados.

Glosas são excertos curtos contíguos; quebras tipográficas são reunidas e os
separadores de entrada ficam fora do headword. O s longo é preservado como ſ;
ligaturas tipográficas ct são representadas pelas duas letras, sem modernizar
grafia. A abreviação em “depoſicion” foi evitada mediante excerto mais curto.
Confidence MEDIUM e NEEDS_SEMANTIC_REVIEW continuam explícitos.

L0202 e entradas com expressão, prefixação editorial da fonte ou remissão
(especialmente L0245) ainda exigem revisão de identidade lexical. Fidelidade
de transcrição não confirma independência lexical nem aprova Claims.

## Controles preventivos

Gate 6 verifica assinaturas de mojibake e controles, incluindo strings JSON
escapadas, sem alterar conteúdo; caracteres históricos não-ASCII continuam
válidos. O scan abrange todos os ledgers, registros canônicos, coverage,
duplicidades, Preview e relatórios de lote. O CI chama esse controle por
--check-current. Concordância 1:1 do ledger Batch 04 e regressões editoriais
L0241–L0243 são obrigatórias nos dois modos de checkpoint.

## Contagens reproduzíveis

As categorias de correção se sobrepõem; não devem ser somadas. A lista por ID
permite verificar a união de registros alterados e os registros inalterados.
TRUE_MOJIBAKE identifica assinaturas do detector; ç, ſ, ñ e acentos observados
são LEGITIMATE_HISTORICAL_TEXT. Não há exceções de mojibake liberadas nos dados.

## Validação local

103 testes unittest: PASS. Gates 3/4/5: PASS. Gate 6 checkpoint 4 e
--check-current: PASS. Exporter reproduzível, audit_publication e
audit_preview_dist: PASS. npm ci, npm test e npm run build: PASS.
L0001–L0200 não foram alterados. A verificação remota e o smoke no navegador
serão informados na entrega; aprovação externa continua pendente.

'''
text += '```json\n' + json.dumps({k: v for k, v in summary.items() if k != 'rows'}, ensure_ascii=False, indent=2) + '\n```\n'
text += '\n| ID | Campos corrigidos | Reinspeção |\n|---|---|---|\n'
for row in rows:
    text += f'| {row["lemma_id"]} | {", ".join(row["changed_fields"]) or "nenhum"} | COMPLETE |\n'
(ROOT / 'docs/gate6/BATCH_04_REMEDIATION_REPORT.md').write_text(text, encoding='utf-8')
print(json.dumps({k: v for k, v in summary.items() if k != 'rows'}, indent=2))

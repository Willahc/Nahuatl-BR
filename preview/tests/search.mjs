import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';

const source = readFileSync(new URL('../src/lib/fold.ts', import.meta.url), 'utf8');
const { outputText } = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } });
const { fold, searchLemmas } = await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);
const data = JSON.parse(readFileSync(new URL('../public/data/nahuatl-br.json', import.meta.url), 'utf8'));
assert.equal(fold('āēīōĀĒĪŌ'), 'aeioaeio');
assert.equal(fold('xōchitl'), 'xochitl');
for (const value of ['xöchitl', 'à', 'á', 'ç', 'âãäëïö', 'a\u035c']) assert.equal(fold(value), value);
for (const query of ['xochitl', 'xöchitl']) {
  assert.deepEqual(searchLemmas(data.lemmas, query).map(l => l.id), ['L0050']);
}
const lemma = data.lemmas.find(l => l.id === 'L0050');
const isolated = { ...lemma, display_form: '', interpretations: [], pt_br_editorial: [], historical_glosses: [],
  forms: { source_forms: [], normalized_form: null, pedagogical_form: null, search_keys: [] } };
const sourceOnly = { ...isolated, forms: { ...isolated.forms, source_forms: lemma.forms.source_forms.filter(v => v.includes('ö')) } };
assert.equal(searchLemmas([sourceOnly], 'xöchitl').length, 1);
assert.equal(searchLemmas([sourceOnly], 'xochitl').length, 0);
const keyOnly = { ...isolated, forms: { ...isolated.forms, search_keys: lemma.forms.search_keys } };
assert.equal(searchLemmas([keyOnly], 'xochitl').length, 1);
assert.equal(searchLemmas([keyOnly], 'xöchitl').length, 0);
console.log('Frontend search: PASS (canonical keys and historical source independently verified)');

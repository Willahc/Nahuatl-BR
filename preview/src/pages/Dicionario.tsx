import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Pill } from "../components/Pill";
import { searchLemmas } from "../lib/data";
import type { LemmaDto } from "../lib/types";

export function Dicionario({ lemmas }: { lemmas: LemmaDto[] }) {
  const [query, setQuery] = useState("");
  const results = useMemo(() => searchLemmas(lemmas, query), [lemmas, query]);

  return (
    <>
      <section className="card">
        <h2>Dicionário — 50 lemas piloto</h2>
        <label className="field">
          <span>Buscar (sem distinção de diacríticos)</span>
          <input
            autoFocus
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="ex.: xochitl, xöchitl, flor, agua"
          />
        </label>
        <p className="muted">
          {query.trim() ? `${results.length} resultado(s)` : "Digite para filtrar"}
        </p>
      </section>

      <ul className="list">
        {results.map((lemma) => (
          <li key={lemma.id} className="card lemma-row">
            <Link to={`/lemma/${lemma.id}`}>
              <h3>{lemma.display_form ?? lemma.id}</h3>
            </Link>
            <p className="forms">
              {lemma.forms.source_forms.join(", ")}
              {lemma.forms.normalized_form && <> · {lemma.forms.normalized_form}</>}
            </p>
            <p className="muted">
              {[...lemma.interpretations, ...lemma.pt_br_editorial].join(" — ") ||
                lemma.historical_glosses.join(" — ")}
            </p>
            {lemma.phonology.analysis_candidate && (
              <p>
                <Pill kind={lemma.phonology.analysis_candidate.editorial_state}>
                  {lemma.phonology.analysis_candidate.editorial_state}
                </Pill>{" "}
                candidata de reconstrução fonêmica
              </p>
            )}
          </li>
        ))}
        {results.length === 0 && (
          <li className="card">
            <p className="muted">Nenhum lema encontrado para a busca informada.</p>
          </li>
        )}
      </ul>
    </>
  );
}
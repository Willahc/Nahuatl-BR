import { Link } from "react-router-dom";
import { Pill } from "../components/Pill";
import type { LemmaDto } from "../lib/types";

export function Fonologia({ lemmas }: { lemmas: LemmaDto[] }) {
  const withCandidate = lemmas.filter((lemma) => lemma.phonology.analysis_candidate);
  const byState = new Map<string, number>();
  for (const lemma of withCandidate) {
    const state = lemma.phonology.analysis_candidate?.editorial_state ?? "UNKNOWN";
    byState.set(state, (byState.get(state) ?? 0) + 1);
  }
  const vowelLengths = new Set<string>();
  const saltillos = new Set<string>();
  for (const lemma of lemmas) {
    vowelLengths.add(lemma.phonology.vowel_length ?? "NOT_REVIEWED");
    saltillos.add(lemma.phonology.saltillo ?? "NOT_REVIEWED");
  }

  return (
    <>
      <section className="card">
        <h2>Fonologia — candidatas de reconstrução</h2>
        <p className="muted">
          As análises abaixo são <strong>candidatas</strong> (Gate 4/5 em revisão), nunca fatos
          publicados. Nenhuma duração vocálica, saltillo ou IPA foi inferida sem evidência.
        </p>
      </section>

      <section className="grid">
        <div className="card">
          <h3>Por estado editorial</h3>
          <ul className="stack">
            {[...byState.entries()].map(([state, count]) => (
              <li key={state}>
                <Pill kind={state}>{state}</Pill> · {count} lema(s)
              </li>
            ))}
            {byState.size === 0 && <li className="muted">Nenhuma candidata registrada.</li>}
          </ul>
        </div>
        <div className="card">
          <h3>Valores registrados</h3>
          <p>
            <span className="muted">Duração vocálica:</span> {[...vowelLengths].sort().join(" · ")}
          </p>
          <p>
            <span className="muted">Saltillo:</span> {[...saltillos].sort().join(" · ")}
          </p>
        </div>
      </section>

      <section className="card">
        <h3>Lemas com candidata ({withCandidate.length})</h3>
        <ul className="list">
          {withCandidate.map((lemma) => {
            const candidate = lemma.phonology.analysis_candidate!;
            return (
              <li key={lemma.id} className="lemma-row">
                <Link to={`/lemma/${lemma.id}`}>
                  <strong>{lemma.display_form ?? lemma.id}</strong>
                </Link>
                <p className="meta">
                  <Pill kind={candidate.editorial_state}>{candidate.editorial_state}</Pill>{" "}
                  VL {candidate.vowel_length ?? "—"} · SALT {candidate.saltillo ?? "—"}
                  {candidate.phonemic_ipa && <> · {candidate.phonemic_ipa}</>}
                </p>
              </li>
            );
          })}
        </ul>
      </section>
    </>
  );
}
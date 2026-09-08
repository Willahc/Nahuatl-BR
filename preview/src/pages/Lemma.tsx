import { Link, useParams } from "react-router-dom";
import { Pill } from "../components/Pill";
import { lemmaById } from "../lib/data";
import type { LemmaDto } from "../lib/types";

function Attestations({ lemma, label }: { lemma: LemmaDto; label: string }) {
  if (!lemma.sources.length) return null;
  return (
    <section className="card">
      <h3>{label}</h3>
      <ul className="stack">
        {lemma.sources.map((source, index) => (
          <li key={index} className="line">
            <strong>{source.work ?? source.source_id ?? "—"}</strong>
            {source.locator && <span className="muted"> · {source.locator}</span>}
            {source.mediation_level && <span className="muted"> · {source.mediation_level}</span>}
            {source.direct_witness_inspected && <Pill kind="ACCEPT">testemunho direto</Pill>}
            {source.url && (
              <span className="muted">
                {" "}
                · <a href={source.url}>link</a>
              </span>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}

export function Lemma({ lemmas }: { lemmas: LemmaDto[] }) {
  const { id = "" } = useParams();
  const lemma = lemmaById(lemmas, id);

  if (!lemma) {
    return (
      <section className="card">
        <h2>Lemma não encontrado</h2>
        <p className="muted">Identificador desconhecido: {id}</p>
        <p>
          <Link to="/dicionario">Voltar ao dicionário</Link>
        </p>
      </section>
    );
  }

  const candidate = lemma.phonology.analysis_candidate;
  return (
    <>
      <p>
        <Link to="/dicionario">← dicionário</Link> · <Link to="/fonologia">fonologia</Link>
      </p>
      <section className="card">
        <h2>{lemma.display_form ?? lemma.id}</h2>
        <p className="meta">
          <span className="mono">{lemma.id}</span>
          {lemma.variety && <span> · {lemma.variety}</span>}
          {lemma.status && (
            <>
              {" "}
              · <Pill kind={lemma.status === "PUBLISHED" ? "PUBLISHED" : "IN_REVIEW"}>{lemma.status}</Pill>
            </>
          )}
        </p>

        <h3>Formas registradas</h3>
        <p className="forms">
          {lemma.forms.source_forms.join(" · ")}
          {lemma.forms.normalized_form && <> · {lemma.forms.normalized_form}</>}
        </p>
        {(lemma.forms.pedagogical_form || "") !== "UNKNOWN" && (
          <p className="muted">Forma pedagógica: {lemma.forms.pedagogical_form}</p>
        )}
        {lemma.forms.search_keys.length > 0 && (
          <p className="muted">Chaves de busca: {lemma.forms.search_keys.join(", ")}</p>
        )}

        <h3>Interpretações e traduções</h3>
        {lemma.interpretations.length > 0 && (
          <ul className="stack">
            {lemma.interpretations.map((item, index) => (
              <li key={index}>Interpretação atestada: {item}</li>
            ))}
          </ul>
        )}
        {lemma.pt_br_editorial.length > 0 && (
          <ul className="stack">
            {lemma.pt_br_editorial.map((item, index) => (
              <li key={index}>
                Tradução editorial PT-BR: <em>{item}</em>
              </li>
            ))}
          </ul>
        )}
        {lemma.historical_glosses.length > 0 && (
          <ul className="stack">
            {lemma.historical_glosses.map((item, index) => (
              <li key={index} className="muted">
                Glosa histórica: {item}
              </li>
            ))}
          </ul>
        )}
        {lemma.notes && <p className="muted">{lemma.notes}</p>}
      </section>

      <section className="card">
        <h3>Fonologia do lema</h3>
        <p>
          Duração vocálica: <Pill kind="REPORTED">{lemma.phonology.vowel_length ?? "NOT_REVIEWED"}</Pill>{" "}
          · Saltillo: <Pill kind="REPORTED">{lemma.phonology.saltillo ?? "NOT_REVIEWED"}</Pill>
        </p>
        {lemma.phonology.notes?.map((note, index) => (
          <p key={index} className="muted">
            {note}
          </p>
        ))}
      </section>

      {candidate && (
        <section className="card">
          <h3>Reconstrução fonêmica (candidata)</h3>
          <p className="meta">
            <Pill kind={candidate.editorial_state}>{candidate.editorial_state}</Pill>{" "}
            <Pill kind={candidate.modality}>{candidate.modality}</Pill>{" "}
            <Pill kind={candidate.confidence}>{candidate.confidence}</Pill>
          </p>
          <table className="table">
            <tbody>
              {candidate.vowel_length && (
                <tr>
                  <th>Duração vocálica</th>
                  <td>{candidate.vowel_length}</td>
                </tr>
              )}
              {candidate.saltillo && (
                <tr>
                  <th>Saltillo</th>
                  <td>{candidate.saltillo}</td>
                </tr>
              )}
              {candidate.phonemic_ipa && (
                <tr>
                  <th>IPA fonêmico</th>
                  <td className="mono">{candidate.phonemic_ipa}</td>
                </tr>
              )}
              {candidate.phonetic_ipa && (
                <tr>
                  <th>IPA fonético</th>
                  <td className="mono">{candidate.phonetic_ipa}</td>
                </tr>
              )}
            </tbody>
          </table>
          <p className="aside">
            Proposta de integração ({candidate.profile ?? dataProfile(candidate)}) registrada como
            candidate; não constitui fato fonológico publicado.
            {candidate.notes && <> {candidate.notes}</>}
            {candidate.claim_ids?.length ? (
              <> Claims associados: {candidate.claim_ids.join(", ")}.</>
            ) : null}
          </p>
        </section>
      )}

      <Attestations lemma={lemma} label="Atestações" />

      {lemma.references.length > 0 && (
        <section className="card">
          <h3>Referências de corpus</h3>
          <ul className="stack">
            {lemma.references.map((reference, index) => (
              <li key={index} className="line">
                <strong>{reference.work ?? reference.source ?? "—"}</strong>
                {reference.locator && <span className="muted"> · {reference.locator}</span>}
                {reference.use && <span className="muted"> · uso: {reference.use}</span>}
                {reference.url && (
                  <span className="muted">
                    {" "}
                    · <a href={reference.url}>link</a>
                  </span>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      {lemma.claim_ids.length > 0 && (
        <section className="card">
          <h3>Claims de fonologia</h3>
          <p className="muted">
            {lemma.claim_ids.join(", ")} — identificadores preservados no círculo de pesquisa;
            detalhes IN_REVIEW não são publicados nesta prévia.
          </p>
        </section>
      )}
    </>
  );
}

function dataProfile(candidate: { profile?: string }): string {
  return candidate.profile ?? "profile não informado";
}
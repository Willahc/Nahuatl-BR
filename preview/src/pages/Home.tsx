import { Link } from "react-router-dom";
import { Pill } from "../components/Pill";
import type { PreviewData } from "../lib/types";

export function Home({ data }: { data: PreviewData }) {
  const gate5 = data.gate_status["Gate 5"];
  return (
    <>
      <section className="hero">
        <p className="eyebrow">Research Preview 0 · dados canônicos · sem áudio</p>
        <h1>Nahuatl-BR</h1>
        <p className="lede">
          Visualização de pesquisa de <strong>{data.counts.lemmas}</strong> lemas piloto de{" "}
          <strong>Náhuatl Clássico</strong> em português brasileiro, com evidência documental,
          direito de uso por fonte e análise fonológica candidata.
        </p>
        <p className="lede meta">
          Perfis: {data.orthography_profile} · {data.phonology_profile}
        </p>
      </section>

      <section className="grid">
        <Link className="tile" to="/dicionario">
          <h2>Dicionário</h2>
          <p>Buscar entre os lemas piloto com normalização de busca sem diacríticos.</p>
        </Link>
        <Link className="tile" to="/fonologia">
          <h2>Fonologia</h2>
          <p>Propostas de análise fonológica (reconstrução), todas rotuladas como candidatas.</p>
        </Link>
        <Link className="tile" to="/fontes">
          <h2>Fontes</h2>
          <p>Fontes de evidência utilizadas, com papel recomendado de uso.</p>
        </Link>
      </section>

      <section className="card">
        <h2>Estado dos Gates</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Gate</th>
              <th>Status</th>
              <th>Desfecho</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(data.gate_status).map(([name, row]) => (
              <tr key={name}>
                <td>{name}</td>
                <td>
                  <Pill kind={row.status.startsWith("IN_") ? "IN_REVIEW" : "ACCEPT"}>
                    {row.status}
                  </Pill>
                </td>
                <td>{row.closure}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="card">
        <h2>Conteúdo desta prévia</h2>
        <p>
          {data.counts.lemmas} lemas piloto · {data.counts.sources} fontes de referência ·{" "}
          {data.counts.claims_total} claims de fonologia · {data.counts.evidence_total} registros de
          evidência · {data.counts.integration_items} propostas de integração fonológica.
        </p>
        <p className="aside">
          Esta entrega é o produto do Gate 5 em andamento. Os dados de fonologia são candidatos
          (label histórico <code>{data.phonology_profile}</code>) e não são fatos fonológicos
          publicados.
          {gate5 && ` Gate 5: ${gate5.status} — ${gate5.closure}.`}
        </p>
      </section>
    </>
  );
}
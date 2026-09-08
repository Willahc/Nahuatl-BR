import { Pill } from "../components/Pill";
import type { SourceDto } from "../lib/types";

function roleKind(role?: string): string | undefined {
  if (!role) return undefined;
  if (role.startsWith("CAN_INGEST")) return "ACCEPT";
  if (role.startsWith("MANUAL")) return "IN_REVIEW";
  if (role.startsWith("CAN_REFERENCE")) return "REPORTED";
  if (role.startsWith("DO_NOT")) return "REJECT";
  return "REPORTED";
}

export function Fontes({ sources }: { sources: Record<string, SourceDto> }) {
  const entries = Object.entries(sources).sort(([a], [b]) => a.localeCompare(b));
  return (
    <>
      <section className="card">
        <h2>Fontes de evidência</h2>
        <p className="muted">
          Fontes não modernas registradas no círculo de pesquisa e utilizáveis como referência.
          Fontes de variedades modernas (C01, C02, C03) <strong>não</strong> aparecem nesta prévia;
          o pipeline de ingestão as rejeita como evidência de Náhuatl Clássico.
        </p>
      </section>
      <ul className="list">
        {entries.map(([id, source]) => (
          <li key={id} className="card">
            <p className="meta">
              <span className="mono">{id}</span>
              {source.institution && <span> · {source.institution}</span>}
            </p>
            <h3>{source.name ?? "sem nome"}</h3>
            {source.recommended_role && (
              <p>
                Papel recomendado: <Pill kind={roleKind(source.recommended_role)}>{source.recommended_role}</Pill>
              </p>
            )}
            {source.url && (
              <p className="muted">
                <a href={source.url}>registro da fonte</a>
              </p>
            )}
          </li>
        ))}
      </ul>
      <p className="muted">
        Essas são fontes de referência ou evidência restrita; papéis recomendados descrevem uso
        permitido, não autoria. Ver documentação do Gate 5 para o inventário completo.
      </p>
    </>
  );
}
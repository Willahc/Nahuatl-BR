import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <section className="card">
      <h2>Rota não encontrada</h2>
      <p>
        Esta prévia (Research Preview 0) é um aplicativo de leitura estático; a
        rota informada não existe.
      </p>
      <p>
        <Link to="/">Voltar ao início</Link>
      </p>
    </section>
  );
}
import { HashRouter, NavLink, Route, Routes } from "react-router-dom";
import { NotFound } from "./pages/NotFound";
import { Home } from "./pages/Home";
import { Dicionario } from "./pages/Dicionario";
import { Lemma } from "./pages/Lemma";
import { Fontes } from "./pages/Fontes";
import { Fonologia } from "./pages/Fonologia";
import { usePreview } from "./lib/usePreview";
import { useTheme } from "./lib/useTheme";

function Header() {
  const { theme, toggle } = useTheme();
  return (
    <header className="app-header">
      <NavLink to="/" className="brand">
        Nahuatl-BR <span className="brand-sub">Research Preview 0</span>
      </NavLink>
      <nav className="nav">
        <NavLink to="/dicionario">Dicionário</NavLink>
        <NavLink to="/fonologia">Fonologia</NavLink>
        <NavLink to="/fontes">Fontes</NavLink>
      </nav>
      <button className="theme-toggle" onClick={toggle} aria-label="Alternar tema">
        {theme === "dark" ? "claro" : "escuro"}
      </button>
    </header>
  );
}

function Footer() {
  return (
    <footer className="app-footer">
      <p className="muted">
        Náhuatl Clássico · acervo de pesquisa em construção · dados canônicos em{" "}
        <code>data/</code> · visualização derivada e determinística.
      </p>
    </footer>
  );
}

function Fallback({ message }: { message: string }) {
  return (
    <section className="card">
      <h2>Dados indisponíveis</h2>
      <p className="muted">{message}. Verifique se <code>public/data/nahuatl-br.json</code> foi gerado pelo exporter.</p>
    </section>
  );
}

function Scaffold() {
  const { data, error, loading } = usePreview();

  if (loading) return <Fallback message="Carregando dados canônicos…" />;
  if (error || !data) return <Fallback message={error ?? "Sem dados"} />;

  return (
    <Routes>
      <Route path="/" element={<Home data={data} />} />
      <Route path="/dicionario" element={<Dicionario lemmas={data.lemmas} />} />
      <Route path="/lemma/:id" element={<Lemma lemmas={data.lemmas} />} />
      <Route path="/fontes" element={<Fontes sources={data.sources} />} />
      <Route path="/fonologia" element={<Fonologia lemmas={data.lemmas} />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default function App() {
  return (
    <HashRouter>
      <Header />
      <main className="container">
        <Scaffold />
      </main>
      <Footer />
    </HashRouter>
  );
}
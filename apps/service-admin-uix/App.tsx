import { useEffect, useState } from "react";
import { API_BASE_URL, PRODUCT_API, SURFACE_PURPOSE, apiUrl } from "./services/backendSurface";

const views = {
  "#/services": {
    title: "Service identities",
    body: "Create and administer workload principals, service keys, and non-human identity lifecycle records.",
    paths: ["/service", "/servicekey"]
  },
  "#/credentials": {
    title: "Workload credentials",
    body: "Issue and inspect API keys and token records used by machine-to-machine clients.",
    paths: ["/apikey", "/tokenrecord"]
  },
  "#/validation": {
    title: "Validation metadata",
    body: "Check the token validation, resource metadata, and introspection surfaces used by protected APIs.",
    paths: ["/introspect", "/.well-known/oauth-protected-resource", "/rpc"]
  }
};

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/services");

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/services");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/services";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const view = views[currentHash as keyof typeof views] || views["#/services"];

  return (
    <main style={{ minHeight: "100vh", fontFamily: "Aptos, Segoe UI, sans-serif", background: "#f7f3f9", color: "#21172a" }}>
      <aside style={{ borderRight: "1px solid #dbcbe6", bottom: 0, left: 0, padding: "24px", position: "fixed", top: 0, width: "260px" }}>
        <p style={{ color: "#6a4187", fontSize: "0.72rem", letterSpacing: "0.12em", margin: 0, textTransform: "uppercase" }}>{PRODUCT_API}</p>
        <h1 style={{ fontSize: "1.5rem", margin: "10px 0" }}>Service Admin</h1>
        <p style={{ color: "#6b5877", fontSize: "0.9rem" }}>{SURFACE_PURPOSE}</p>
        <nav style={{ display: "grid", gap: "8px", marginTop: "22px" }}>
          {Object.entries(views).map(([href, item]) => (
            <a key={href} href={href} style={{ background: currentHash === href ? "#6a4187" : "transparent", borderRadius: "6px", color: currentHash === href ? "#fff" : "#55356d", padding: "9px 10px", textDecoration: "none" }}>{item.title}</a>
          ))}
        </nav>
        <p style={{ bottom: "22px", color: "#765f84", fontSize: "0.78rem", left: "24px", position: "absolute", right: "24px" }}>API: <code>{API_BASE_URL}</code></p>
      </aside>
      <section style={{ marginLeft: "260px", padding: "32px" }}>
        <div style={{ maxWidth: "980px" }}>
          <h2 style={{ fontSize: "2rem", margin: "0 0 8px" }}>{view.title}</h2>
          <p style={{ color: "#6b5877", margin: "0 0 22px" }}>{view.body}</p>
          <div style={{ display: "grid", gap: "12px" }}>
            {view.paths.map((path) => (
              <article key={path} style={{ background: "#fff", border: "1px solid #dbcbe6", borderRadius: "8px", padding: "14px" }}>
                <strong>{path}</strong>
                <div style={{ color: "#765f84", fontSize: "0.86rem", marginTop: "6px" }}>{apiUrl(path).href}</div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

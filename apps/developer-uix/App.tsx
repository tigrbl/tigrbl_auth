import { useEffect, useState } from "react";
import { API_BASE_URL, PRODUCT_API, SURFACE_PURPOSE, apiUrl } from "./services/backendSurface";

const views = {
  "#/apps": {
    title: "Applications",
    body: "Register OAuth and OIDC applications, review assigned client identifiers, and keep app metadata tenant-scoped.",
    paths: ["/register", "/client"]
  },
  "#/metadata": {
    title: "Client metadata",
    body: "Manage redirect URIs, client registration records, JWKS references, and protocol metadata for developer-owned apps.",
    paths: ["/clientregistration", "/rpc"]
  },
  "#/discovery": {
    title: "Issuer discovery",
    body: "Inspect issuer metadata needed by app developers without crossing into admin or service workload operations.",
    paths: ["/.well-known/openid-configuration"]
  }
};

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/apps");

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/apps");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/apps";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const view = views[currentHash as keyof typeof views] || views["#/apps"];

  return (
    <main style={{ minHeight: "100vh", fontFamily: "Aptos, Segoe UI, sans-serif", background: "#eef3ff", color: "#131f33" }}>
      <aside style={{ borderRight: "1px solid #cdd8f0", bottom: 0, left: 0, padding: "24px", position: "fixed", top: 0, width: "260px" }}>
        <p style={{ color: "#315ca6", fontSize: "0.72rem", letterSpacing: "0.12em", margin: 0, textTransform: "uppercase" }}>{PRODUCT_API}</p>
        <h1 style={{ fontSize: "1.5rem", margin: "10px 0" }}>Developer Portal</h1>
        <p style={{ color: "#566985", fontSize: "0.9rem" }}>{SURFACE_PURPOSE}</p>
        <nav style={{ display: "grid", gap: "8px", marginTop: "22px" }}>
          {Object.entries(views).map(([href, item]) => (
            <a key={href} href={href} style={{ background: currentHash === href ? "#315ca6" : "transparent", borderRadius: "6px", color: currentHash === href ? "#fff" : "#203a68", padding: "9px 10px", textDecoration: "none" }}>{item.title}</a>
          ))}
        </nav>
        <p style={{ bottom: "22px", color: "#5c6f8e", fontSize: "0.78rem", left: "24px", position: "absolute", right: "24px" }}>API: <code>{API_BASE_URL}</code></p>
      </aside>
      <section style={{ marginLeft: "260px", padding: "32px" }}>
        <div style={{ maxWidth: "980px" }}>
          <h2 style={{ fontSize: "2rem", margin: "0 0 8px" }}>{view.title}</h2>
          <p style={{ color: "#566985", margin: "0 0 22px" }}>{view.body}</p>
          <div style={{ display: "grid", gap: "12px" }}>
            {view.paths.map((path) => (
              <article key={path} style={{ background: "#fff", border: "1px solid #cdd8f0", borderRadius: "8px", padding: "14px" }}>
                <strong>{path}</strong>
                <div style={{ color: "#5c6f8e", fontSize: "0.86rem", marginTop: "6px" }}>{apiUrl(path).href}</div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

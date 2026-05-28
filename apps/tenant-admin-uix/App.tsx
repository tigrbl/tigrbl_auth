import { useEffect, useState } from "react";
import { API_BASE_URL, PRODUCT_API, SURFACE_PURPOSE, apiUrl } from "./services/backendSurface";

const views = {
  "#/identities": {
    title: "Tenant identities",
    body: "Manage tenant users, tenant administrators, activation state, and password reset posture.",
    paths: ["/user", "/auth/admin/session"]
  },
  "#/keys": {
    title: "Tenant keys",
    body: "Review tenant JWKS publication and key rotation events without platform-wide tenant lifecycle authority.",
    paths: ["/keyrotationevent", "/rpc"]
  },
  "#/clients": {
    title: "Tenant clients",
    body: "Inspect tenant-local clients, consents, and client registration records visible to tenant administrators.",
    paths: ["/client", "/clientregistration", "/consent"]
  }
};

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/identities");

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/identities");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/identities";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const view = views[currentHash as keyof typeof views] || views["#/identities"];

  return (
    <main style={{ minHeight: "100vh", fontFamily: "Aptos, Segoe UI, sans-serif", background: "#f5f8f2", color: "#17251d" }}>
      <aside style={{ borderRight: "1px solid #d8e3d5", bottom: 0, left: 0, padding: "24px", position: "fixed", top: 0, width: "260px" }}>
        <p style={{ color: "#2e704b", fontSize: "0.72rem", letterSpacing: "0.12em", margin: 0, textTransform: "uppercase" }}>{PRODUCT_API}</p>
        <h1 style={{ fontSize: "1.5rem", margin: "10px 0" }}>Tenant Admin</h1>
        <p style={{ color: "#536b59", fontSize: "0.9rem" }}>{SURFACE_PURPOSE}</p>
        <nav style={{ display: "grid", gap: "8px", marginTop: "22px" }}>
          {Object.entries(views).map(([href, item]) => (
            <a key={href} href={href} style={{ background: currentHash === href ? "#255d3f" : "transparent", borderRadius: "6px", color: currentHash === href ? "#fff" : "#173622", padding: "9px 10px", textDecoration: "none" }}>{item.title}</a>
          ))}
        </nav>
        <p style={{ bottom: "22px", color: "#607766", fontSize: "0.78rem", left: "24px", position: "absolute", right: "24px" }}>API: <code>{API_BASE_URL}</code></p>
      </aside>
      <section style={{ marginLeft: "260px", padding: "32px" }}>
        <div style={{ maxWidth: "980px" }}>
          <h2 style={{ fontSize: "2rem", margin: "0 0 8px" }}>{view.title}</h2>
          <p style={{ color: "#536b59", margin: "0 0 22px" }}>{view.body}</p>
          <div style={{ display: "grid", gap: "12px" }}>
            {view.paths.map((path) => (
              <article key={path} style={{ background: "#fff", border: "1px solid #d8e3d5", borderRadius: "8px", padding: "14px" }}>
                <strong>{path}</strong>
                <div style={{ color: "#607766", fontSize: "0.86rem", marginTop: "6px" }}>{apiUrl(path).href}</div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

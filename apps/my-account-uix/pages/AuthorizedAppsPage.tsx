import { Button, Panel } from "../components/UI";
import type { AuthorizedApp, Consent } from "../types";

export function AuthorizedAppsPage({
  apps,
  consents,
  onRevokeApp,
  onRevokeConsent
}: {
  apps: AuthorizedApp[];
  consents: Consent[];
  onRevokeApp: (clientId: string) => Promise<void>;
  onRevokeConsent: (consentId: string) => Promise<void>;
}) {
  return (
    <>
      <Panel title="Authorized Apps">
        <div style={{ display: "grid", gap: "10px" }}>
          {apps.length === 0 ? <p>No authorized applications.</p> : null}
          {apps.map((app) => (
            <div key={app.client_id} style={{ borderTop: "1px solid #d8e2dd", display: "grid", gap: "8px", gridTemplateColumns: "minmax(0, 1fr) auto", padding: "12px 0" }}>
              <div style={{ minWidth: 0 }}>
                <strong style={{ overflowWrap: "anywhere" }}>{app.client_id}</strong>
                <p style={{ color: "#4f6d63", margin: "4px 0 0" }}>{app.scope}</p>
              </div>
              <Button variant="danger" onClick={() => void onRevokeApp(app.client_id)}>
                Revoke
              </Button>
            </div>
          ))}
        </div>
      </Panel>
      <Panel title="Consent Grants">
        <div style={{ display: "grid", gap: "10px" }}>
          {consents.length === 0 ? <p>No consent grants.</p> : null}
          {consents.map((consent) => (
            <div key={consent.id} style={{ borderTop: "1px solid #d8e2dd", display: "grid", gap: "8px", gridTemplateColumns: "minmax(0, 1fr) auto", padding: "12px 0" }}>
              <div style={{ minWidth: 0 }}>
                <strong>{consent.state}</strong>
                <p style={{ color: "#4f6d63", margin: "4px 0 0", overflowWrap: "anywhere" }}>{consent.client_id}</p>
                <p style={{ color: "#4f6d63", margin: "4px 0 0" }}>{consent.scope}</p>
              </div>
              <Button variant="danger" onClick={() => void onRevokeConsent(consent.id)}>
                Revoke
              </Button>
            </div>
          ))}
        </div>
      </Panel>
    </>
  );
}

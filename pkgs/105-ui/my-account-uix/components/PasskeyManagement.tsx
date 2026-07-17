import { useEffect, useState } from "react";
import { listPasskeys, renamePasskey, revokePasskey } from "../services/passkeys";

export function PasskeyManagement() {
  const [items, setItems] = useState<Record<string, unknown>[]>([]);
  const [error, setError] = useState<string>();
  const refresh = () => listPasskeys().then(setItems).catch((reason) => setError(String(reason)));
  useEffect(refresh, []);
  return <section aria-labelledby="passkeys-heading">
    <h2 id="passkeys-heading">Passkeys</h2>
    {error ? <p role="alert">{error}</p> : null}
    <ul>{items.map((item) => {
      const id = String(item.credential_id ?? item.id);
      const name = String(item.display_name ?? "Passkey");
      return <li key={id}>
        <span>{name}</span>
        <button type="button" onClick={async () => { const next = prompt("Passkey name", name); if (next) { await renamePasskey(id, next); refresh(); } }}>Rename</button>
        <button type="button" onClick={async () => { await revokePasskey(id); refresh(); }}>Remove</button>
      </li>;
    })}</ul>
  </section>;
}

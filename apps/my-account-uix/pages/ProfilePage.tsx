import { useEffect, useState } from "react";
import type { AccountProfile } from "../types";
import { Button, Field, Panel } from "../components/UI";

export function ProfilePage({
  profile,
  onSave
}: {
  profile: AccountProfile;
  onSave: (username: string, email: string) => Promise<void>;
}) {
  const [username, setUsername] = useState(profile.username);
  const [email, setEmail] = useState(profile.email);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setUsername(profile.username);
    setEmail(profile.email);
  }, [profile]);

  async function save() {
    setSaving(true);
    try {
      await onSave(username, email);
    } finally {
      setSaving(false);
    }
  }

  return (
    <Panel title="Profile">
      <div style={{ display: "grid", gap: "14px", maxWidth: "520px" }}>
        <Field label="Username" value={username} onChange={setUsername} />
        <Field label="Email" value={email} onChange={setEmail} />
        <p style={{ color: "#4f6d63", margin: 0 }}>Tenant: {profile.tenant_id}</p>
        <Button onClick={save}>{saving ? "Saving" : "Save profile"}</Button>
      </div>
    </Panel>
  );
}

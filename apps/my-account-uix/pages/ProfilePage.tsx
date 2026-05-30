import { Button, Card, DetailPanel, FormField, PageHeader, ResourceForm, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import { useEffect, useState } from "react";
import type { AccountProfile } from "../types";

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
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    setUsername(profile.username);
    setEmail(profile.email);
  }, [profile]);

  async function save() {
    setSaving(true);
    setStatus(null);
    try {
      await onSave(username, email);
      setStatus("Profile saved");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Profile" description="Manage your current subject profile." />
      <div className="tigrbl-metric-grid">
        <Card tone="compact">
          <p className="tigrbl-eyebrow">Subject</p>
          <code>{profile.id}</code>
        </Card>
        <Card tone="compact">
          <p className="tigrbl-eyebrow">Tenant</p>
          <code>{profile.tenant_id}</code>
        </Card>
        <Card tone="compact">
          <p className="tigrbl-eyebrow">Account status</p>
          <StatusBadge tone={profile.is_active ? "success" : "warning"}>{profile.is_active ? "Active" : "Inactive"}</StatusBadge>
        </Card>
      </div>
      <DetailPanel title="Account profile">
        <ResourceForm footer={<Button onClick={() => void save()} type="button">{saving ? "Saving" : "Save profile"}</Button>}>
          <FormField label="Username" value={username} onChange={(event) => setUsername(event.target.value)} />
          <FormField label="Email" value={email} onChange={(event) => setEmail(event.target.value)} />
          {status ? <Toast tone="success" message={status} /> : null}
        </ResourceForm>
      </DetailPanel>
    </div>
  );
}

import { Button, Card, DetailPanel, FormField, InlineMutationResult, PageHeader, ResourceForm, StatusBadge } from "@tigrbl-auth/uix-core";
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
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    setUsername(profile.username);
    setEmail(profile.email);
  }, [profile]);

  async function save() {
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      await onSave(username, email);
      setSuccess("Profile saved.");
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Profile update failed.");
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
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Account profile">
        <ResourceForm footer={<Button disabled={saving} onClick={() => void save()} type="button">{saving ? "Saving" : "Save profile"}</Button>}>
          <FormField label="Username" value={username} onChange={(event) => setUsername(event.target.value)} />
          <FormField label="Email" value={email} onChange={(event) => setEmail(event.target.value)} />
        </ResourceForm>
      </DetailPanel>
    </div>
  );
}

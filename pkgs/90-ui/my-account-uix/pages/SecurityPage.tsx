import { Button, Card, DetailPanel, FormField, InlineMutationResult, PageHeader, ResourceForm, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import { useState } from "react";

export function SecurityPage({
  mustChangePassword,
  onChangePassword
}: {
  mustChangePassword: boolean;
  onChangePassword: (currentPassword: string, newPassword: string) => Promise<void>;
}) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [newPassword, setNewPassword] = useState("");
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  async function submit() {
    setError(null);
    setSuccess(null);
    setSaving(true);
    try {
      await onChangePassword(currentPassword, newPassword);
      setCurrentPassword("");
      setNewPassword("");
      setSuccess("Password changed.");
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Password change failed.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Security" description="Manage password posture and account security settings." />
      <Card tone="compact">
        <p className="tigrbl-eyebrow">Password posture</p>
        {mustChangePassword ? <Toast tone="danger" message="Password change is required." /> : <StatusBadge tone="success">Password current</StatusBadge>}
      </Card>
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Change password">
        <ResourceForm footer={<Button disabled={saving || !currentPassword || !newPassword} onClick={() => void submit()} type="button">{saving ? "Changing" : "Change password"}</Button>}>
          <FormField label="Current password" type="password" value={currentPassword} onChange={(event) => setCurrentPassword(event.target.value)} />
          <FormField label="New password" type="password" value={newPassword} onChange={(event) => setNewPassword(event.target.value)} />
        </ResourceForm>
      </DetailPanel>
    </div>
  );
}

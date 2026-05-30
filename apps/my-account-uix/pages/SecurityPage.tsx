import { Button, Card, DetailPanel, FormField, PageHeader, ResourceForm, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import { useState } from "react";

export function SecurityPage({
  mustChangePassword,
  onChangePassword
}: {
  mustChangePassword: boolean;
  onChangePassword: (currentPassword: string, newPassword: string) => Promise<void>;
}) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  async function submit() {
    setStatus(null);
    await onChangePassword(currentPassword, newPassword);
    setCurrentPassword("");
    setNewPassword("");
    setStatus("Password changed");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Security" description="Manage password posture and account security settings." />
      <Card tone="compact">
        <p className="tigrbl-eyebrow">Password posture</p>
        {mustChangePassword ? <Toast tone="danger" message="Password change is required." /> : <StatusBadge tone="success">Password current</StatusBadge>}
      </Card>
      <DetailPanel title="Change password">
        <ResourceForm footer={<Button onClick={() => void submit()} type="button">Change password</Button>}>
          <FormField label="Current password" type="password" value={currentPassword} onChange={(event) => setCurrentPassword(event.target.value)} />
          <FormField label="New password" type="password" value={newPassword} onChange={(event) => setNewPassword(event.target.value)} />
          {status ? <Toast tone="success" message={status} /> : null}
        </ResourceForm>
      </DetailPanel>
    </div>
  );
}

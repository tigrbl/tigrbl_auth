import { useState } from "react";
import { Button, Field, Panel } from "../components/UI";

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
    <Panel title="Security">
      <div style={{ display: "grid", gap: "14px", maxWidth: "520px" }}>
        {mustChangePassword ? <p style={{ color: "#7f1d1d", margin: 0 }}>Password change is required.</p> : null}
        <Field label="Current password" type="password" value={currentPassword} onChange={setCurrentPassword} />
        <Field label="New password" type="password" value={newPassword} onChange={setNewPassword} />
        <Button onClick={submit}>Change password</Button>
        {status ? <p style={{ color: "#2e704b", margin: 0 }}>{status}</p> : null}
      </div>
    </Panel>
  );
}

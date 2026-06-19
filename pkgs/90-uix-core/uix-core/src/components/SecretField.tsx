import { useState } from "react";
import { Button } from "./Button";

export function SecretField({ label, value }: { label: string; value: string }) {
  const [visible, setVisible] = useState(false);
  return (
    <div className="tigrbl-secret">
      <span>{label}</span>
      <code>{visible ? value : "••••••••••••"}</code>
      <Button onClick={() => setVisible((current) => !current)} type="button" variant="subtle">
        {visible ? "Hide" : "Show"}
      </Button>
    </div>
  );
}


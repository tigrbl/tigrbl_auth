import { Button } from "../components/Button";

export function Topbar({ onLogout, sessionLabel }: { onLogout?: () => void; sessionLabel?: string }) {
  return (
    <header className="tba-topbar">
      <span>{sessionLabel ?? "No active session"}</span>
      {onLogout && <Button onClick={onLogout} type="button" variant="subtle">Sign out</Button>}
    </header>
  );
}


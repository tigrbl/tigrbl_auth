import React, { useState } from "react";
import { createRoot } from "react-dom/client";

function Demo() {
  const [setup, setSetup] = useState(null);
  const [enrolled, setEnrolled] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [busy, setBusy] = useState(false);

  async function send(action, code) {
    setFeedback("");
    setBusy(true);
    try {
      const response = await fetch("/api/" + action, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.message);
      if (action === "start") {
        setSetup(result);
        setEnrolled(false);
      } else if (action === "confirm") {
        setSetup(null);
        setEnrolled(true);
      }
      setFeedback(result.message ?? "");
    } catch (error) {
      setFeedback(error.message);
    } finally {
      setBusy(false);
    }
  }

  return <main style={{maxWidth: "32rem", margin: "3rem auto", padding: "0 1rem", fontFamily: "system-ui"}}>
    <h1>TBA authenticator demo</h1>
    <p>Use a synthetic account to enroll an authenticator and verify a fresh sign-in code.</p>
    <button disabled={busy} onClick={() => send("start")}>Start enrollment</button>
    {setup && <section>
      <h2>Scan with your authenticator</h2>
      <img src={setup.qr} alt="Authenticator setup QR code" width="220" height="220" />
      <p>Manual setup key <code>{setup.secret}</code></p>
    </section>}
    {(setup || enrolled) && <form key={String(enrolled)} onSubmit={event => {
      event.preventDefault();
      const form = event.currentTarget;
      void send(enrolled ? "challenge" : "confirm", new FormData(form).get("code"));
      form.reset();
    }}>
      <label>Authenticator code <input name="code" inputMode="numeric" autoComplete="one-time-code"
        pattern="[0-9]{6}" required /></label>
      <button disabled={busy}>{enrolled ? "Verify sign-in" : "Confirm enrollment"}</button>
    </form>}
    <p role="status">{feedback}</p>
  </main>;
}

createRoot(document.getElementById("root")).render(<Demo />);

import { AppShell, Button, Card, DetailPanel, MetricCard, PageHeader, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import "@tigrbl-auth/uix-core/styles.css";
import { useEffect, useState } from "react";
import { demoFixtures, getSurfaceForStep, journeySteps, type JourneyStep } from "./demoState";
import { PRODUCT_API } from "./defaults";
import { surfaces } from "./surfaces";

const navigation = [
  { href: "#/world", label: "World View" },
  { href: "#/journey", label: "Demo Journey" },
  { href: "#/links", label: "Links" }
];

function SurfaceCard({ surface }: { surface: (typeof surfaces)[number] }) {
  return (
    <Card tone="compact">
      <div className="tigrbl-page-stack">
        <div>
          <p className="tigrbl-eyebrow">{surface.api}</p>
          <h2 style={{ margin: "6px 0 8px" }}>{surface.title}</h2>
          <StatusBadge tone={surface.uix === "API-only surface" ? "info" : "success"}>{surface.uix}</StatusBadge>
        </div>
        <p style={{ color: "var(--tigrbl-muted)", margin: 0 }}>{surface.persona}</p>
        <p style={{ margin: 0 }}>{surface.objects}</p>
        <p style={{ color: "var(--tigrbl-primary)", fontWeight: 800, margin: 0 }}>{surface.demoAction}</p>
        <div className="tigrbl-actions" style={{ justifyContent: "flex-start" }}>
          {surface.uixUrl ? <a className="tigrbl-button tigrbl-button-primary" href={surface.uixUrl}>Open UIX</a> : null}
          <a className="tigrbl-button tigrbl-button-subtle" href={surface.apiUrl}>API docs</a>
        </div>
      </div>
    </Card>
  );
}

function WorldView() {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader
        title="Tigrbl Auth world view"
        description="A cohesive demo map for issuer, account, administration, developer, workload, and resource-server surfaces."
      />
      <div className="tigrbl-metric-grid">
        <Card tone="compact">
          <p className="tigrbl-eyebrow">Product surfaces</p>
          <h2 style={{ fontSize: "2rem", margin: "8px 0 0" }}>{surfaces.length}</h2>
        </Card>
        <Card tone="compact">
          <p className="tigrbl-eyebrow">UIX launchers</p>
          <h2 style={{ fontSize: "2rem", margin: "8px 0 0" }}>{surfaces.filter((surface) => surface.uixUrl).length}</h2>
        </Card>
        <Card tone="compact">
          <p className="tigrbl-eyebrow">API docs</p>
          <h2 style={{ fontSize: "2rem", margin: "8px 0 0" }}>{surfaces.length}</h2>
        </Card>
      </div>
      <div className="tigrbl-card-grid">
        {surfaces.map((surface) => <SurfaceCard key={surface.api} surface={surface} />)}
      </div>
    </div>
  );
}

function DemoJourney() {
  const [verifiedSteps, setVerifiedSteps] = useState<Set<string>>(() => {
    try {
      return new Set(JSON.parse(localStorage.getItem("tigrbl-auth-demo-verified-steps") ?? "[]") as string[]);
    } catch {
      return new Set();
    }
  });
  const [copied, setCopied] = useState<string | null>(null);
  const [apiResults, setApiResults] = useState<Record<string, { ok: boolean; status?: number; summary: string }>>({});
  const [runningApi, setRunningApi] = useState<string | null>(null);

  function persist(next: Set<string>) {
    setVerifiedSteps(next);
    localStorage.setItem("tigrbl-auth-demo-verified-steps", JSON.stringify([...next]));
  }

  function toggleVerified(stepId: string) {
    const next = new Set(verifiedSteps);
    if (next.has(stepId)) {
      next.delete(stepId);
    } else {
      next.add(stepId);
    }
    persist(next);
  }

  async function copyFixture(step: JourneyStep) {
    const payload = `${step.objectLabel}: ${step.objectValue}`;
    await navigator.clipboard.writeText(payload);
    setCopied(payload);
  }

  async function runStepApi(step: JourneyStep) {
    setRunningApi(step.id);
    setApiResults((current) => ({
      ...current,
      [step.id]: { ok: false, summary: "Running..." }
    }));
    try {
      const response = await window.fetch(`/demo-api/steps/${encodeURIComponent(step.id)}`, {
        method: "POST"
      });
      const payload = await response.json() as { ok: boolean; status?: number; summary: string };
      setApiResults((current) => ({
        ...current,
        [step.id]: { ok: payload.ok, status: payload.status, summary: payload.summary }
      }));
      if (payload.ok) {
        const next = new Set(verifiedSteps);
        next.add(step.id);
        persist(next);
      }
    } catch (error) {
      setApiResults((current) => ({
        ...current,
        [step.id]: {
          ok: false,
          summary: error instanceof Error ? error.message : "API request failed"
        }
      }));
    } finally {
      setRunningApi(null);
    }
  }

  async function runAllApi() {
    setRunningApi("all");
    try {
      const response = await window.fetch("/demo-api/run-all", { method: "POST" });
      const payload = await response.json() as {
        ok: boolean;
        results: Array<{ id: string; ok: boolean; status?: number; summary: string }>;
      };
      const nextResults: Record<string, { ok: boolean; status?: number; summary: string }> = {};
      const nextVerified = new Set(verifiedSteps);
      for (const item of payload.results) {
        nextResults[item.id] = { ok: item.ok, status: item.status, summary: item.summary };
        if (item.ok) {
          nextVerified.add(item.id);
        }
      }
      setApiResults((current) => ({ ...current, ...nextResults }));
      persist(nextVerified);
    } catch (error) {
      setApiResults((current) => ({
        ...current,
        "platform-provision-tenant": {
          ok: false,
          summary: error instanceof Error ? error.message : "API demo failed"
        }
      }));
    } finally {
      setRunningApi(null);
    }
  }

  const completeCount = verifiedSteps.size;

  return (
    <div className="tigrbl-page-stack">
      <PageHeader
        title="Executable demo journey"
        description="Run the same tenant, user, application, service, and resource through every product surface."
        actions={<Button type="button" onClick={() => void runAllApi()} disabled={runningApi !== null}>Run API demo</Button>}
      />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Verified steps" value={`${completeCount}/${journeySteps.length}`} description="Proofs completed in this browser" />
        <MetricCard label="Demo tenant" value={demoFixtures.tenant.name} description={demoFixtures.tenant.slug} />
        <MetricCard label="Demo user" value={demoFixtures.user.email} description={demoFixtures.user.role} />
      </div>
      {copied ? <Toast tone="success" message={`Copied ${copied}`} /> : null}
      <DetailPanel title="Timeline">
        <div className="tigrbl-timeline-grid">
          {journeySteps.map((step) => {
            const surface = getSurfaceForStep(step);
            const verified = verifiedSteps.has(step.id);
            return (
              <a
                href={`#step-${step.id}`}
                key={step.id}
                className={`tigrbl-timeline-item ${verified ? "tigrbl-timeline-item-active" : ""}`.trim()}
              >
                <p className="tigrbl-eyebrow">Step {step.order}</p>
                <strong>{surface?.title ?? step.surfaceId}</strong>
                <div style={{ marginTop: "8px" }}>
                  <StatusBadge tone={verified ? "success" : "neutral"}>{verified ? "Verified" : "Ready"}</StatusBadge>
                </div>
              </a>
            );
          })}
        </div>
      </DetailPanel>
      <DetailPanel title="Guided execution">
        <div className="tigrbl-page-stack">
          {journeySteps.map((step) => {
            const surface = getSurfaceForStep(step);
            const verified = verifiedSteps.has(step.id);
            return (
              <Card tone="compact" id={`step-${step.id}`} key={step.id}>
                <div className="tigrbl-page-stack">
                  <div className="tigrbl-actions">
                    <div>
                      <p className="tigrbl-eyebrow">Step {step.order} / {surface?.api}</p>
                      <h2 style={{ margin: "6px 0 0" }}>{surface?.title ?? step.surfaceId}</h2>
                    </div>
                    <StatusBadge tone={verified ? "success" : "warning"}>{verified ? "Verified" : "Not verified"}</StatusBadge>
                  </div>
                  <div className="tigrbl-metric-grid">
                    <Card tone="compact">
                      <p className="tigrbl-eyebrow">Persona</p>
                      <p style={{ margin: "6px 0 0" }}>{step.persona}</p>
                    </Card>
                    <Card tone="compact">
                      <p className="tigrbl-eyebrow">Demo object</p>
                      <p style={{ margin: "6px 0 0" }}>{step.objectValue}</p>
                    </Card>
                    <Card tone="compact">
                      <p className="tigrbl-eyebrow">API proof</p>
                      <p style={{ margin: "6px 0 0" }}>{step.apiRequest.method} {step.apiRequest.url}</p>
                    </Card>
                  </div>
                  <div>
                    <p><strong>Goal:</strong> {step.goal}</p>
                    <p><strong>Action:</strong> {step.action}</p>
                    <p><strong>Proof:</strong> {step.proof}</p>
                    <p><strong>API expected:</strong> {step.apiRequest.expected}</p>
                  </div>
                  {apiResults[step.id] ? (
                    <Toast
                      tone={apiResults[step.id].ok ? "success" : "warning"}
                      message={`${step.apiRequest.label}: ${apiResults[step.id].status ?? "ERR"} ${apiResults[step.id].summary}`}
                    />
                  ) : null}
                  <div className="tigrbl-actions" style={{ justifyContent: "flex-start" }}>
                    {surface?.uixUrl ? <a className="tigrbl-button tigrbl-button-primary" href={surface.uixUrl}>Open UIX</a> : null}
                    {surface?.apiUrl ? <a className="tigrbl-button tigrbl-button-subtle" href={surface.apiUrl}>Open API docs</a> : null}
                    <Button type="button" variant="subtle" onClick={() => void runStepApi(step)} disabled={runningApi !== null}>
                      {runningApi === step.id ? "Running API" : "Run API proof"}
                    </Button>
                    <Button type="button" variant="subtle" onClick={() => void copyFixture(step)}>Copy demo object</Button>
                    <Button type="button" variant={verified ? "subtle" : "primary"} onClick={() => toggleVerified(step.id)}>
                      {verified ? "Clear verified" : "Mark verified"}
                    </Button>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </DetailPanel>
    </div>
  );
}

function Links() {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Surface links" description="All live local demo entry points." />
      <DetailPanel title="Launchers">
        <div style={{ display: "grid", gap: "10px" }}>
          {surfaces.map((surface) => (
            <Card tone="compact" key={surface.api}>
              <div className="tigrbl-actions">
                <div>
                  <p className="tigrbl-eyebrow">{surface.api}</p>
                  <h2 style={{ margin: "6px 0 0" }}>{surface.title}</h2>
                </div>
                <div className="tigrbl-actions">
                  {surface.uixUrl ? <a className="tigrbl-button tigrbl-button-primary" href={surface.uixUrl}>UIX</a> : null}
                  <a className="tigrbl-button tigrbl-button-subtle" href={surface.apiUrl}>Docs</a>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </DetailPanel>
    </div>
  );
}

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/world");

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/world");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/world";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const content = currentHash.startsWith("#/journey") ? <DemoJourney /> : currentHash.startsWith("#/links") ? <Links /> : <WorldView />;

  return (
    <AppShell
      activeHref={currentHash}
      apiBaseUrl="local demo stack"
      navigation={navigation}
      productApi={PRODUCT_API}
      sessionLabel="Demo operator"
      title="Demo Hub"
    >
      {content}
    </AppShell>
  );
}

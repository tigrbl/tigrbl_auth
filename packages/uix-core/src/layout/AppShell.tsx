import type { ReactNode } from "react";
import type { NavigationItem } from "../types";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function AppShell({
  activeHref,
  apiBaseUrl,
  children,
  navigation,
  onLogout,
  productApi,
  sessionLabel,
  title
}: {
  activeHref: string;
  apiBaseUrl?: string;
  children: ReactNode;
  navigation: NavigationItem[];
  onLogout?: () => void;
  productApi: string;
  sessionLabel?: string;
  title: string;
}) {
  return (
    <main className="tigrbl-shell">
      <Sidebar activeHref={activeHref} apiBaseUrl={apiBaseUrl} items={navigation} productApi={productApi} title={title} />
      <section className="tigrbl-shell-main">
        <Topbar onLogout={onLogout} sessionLabel={sessionLabel} />
        <div className="tigrbl-shell-content">{children}</div>
      </section>
    </main>
  );
}


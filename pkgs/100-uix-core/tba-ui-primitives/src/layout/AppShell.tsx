import type { ReactNode } from "react";
import type { NavigationItem } from "../types";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function AppShell({
  activeHref,
  backendAppBaseUrl,
  children,
  navigation,
  onLogout,
  backendApp,
  sessionLabel,
  title
}: {
  activeHref: string;
  backendAppBaseUrl?: string;
  children: ReactNode;
  navigation: NavigationItem[];
  onLogout?: () => void;
  backendApp: string;
  sessionLabel?: string;
  title: string;
}) {
  return (
    <main className="tba-shell">
      <Sidebar activeHref={activeHref} backendAppBaseUrl={backendAppBaseUrl} items={navigation} backendApp={backendApp} title={title} />
      <section className="tba-shell-main">
        <Topbar onLogout={onLogout} sessionLabel={sessionLabel} />
        <div className="tba-shell-content">{children}</div>
      </section>
    </main>
  );
}


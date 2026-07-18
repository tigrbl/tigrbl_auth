import type { ReactNode } from "react";
import { BrandHeader } from "./BrandHeader";

export function AuthShell({
  children,
  footer,
  backendApp,
  subtitle,
  title
}: {
  children: ReactNode;
  footer?: ReactNode;
  backendApp?: string;
  subtitle?: string;
  title: string;
}) {
  return (
    <main className="tigrbl-auth-shell">
      <BrandHeader label="Tigrbl Auth" />
      <section className="tigrbl-auth-shell-content">
        <div className="tigrbl-auth-copy">
          {backendApp && <p className="tigrbl-eyebrow">{backendApp}</p>}
          <h1>{title}</h1>
          {subtitle && <p>{subtitle}</p>}
        </div>
        {children}
      </section>
      <footer className="tigrbl-auth-footer">
        {footer ?? <span>© {new Date().getFullYear()} Tigrbl Auth</span>}
      </footer>
    </main>
  );
}

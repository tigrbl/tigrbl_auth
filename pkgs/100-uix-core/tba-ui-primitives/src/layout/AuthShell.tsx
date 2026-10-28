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
    <main className="tba-auth-shell">
      <BrandHeader label="TBA" />
      <section className="tba-auth-shell-content">
        <div className="tba-auth-copy">
          {backendApp && <p className="tba-eyebrow">{backendApp}</p>}
          <h1>{title}</h1>
          {subtitle && <p>{subtitle}</p>}
        </div>
        {children}
      </section>
      <footer className="tba-auth-footer">
        {footer ?? <span>© {new Date().getFullYear()} TBA</span>}
      </footer>
    </main>
  );
}

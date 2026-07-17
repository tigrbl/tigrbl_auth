import type { ReactNode } from "react";

export function DetailPanel({ children, title }: { children: ReactNode; title: string }) {
  return (
    <section className="tigrbl-panel">
      <h2>{title}</h2>
      {children}
    </section>
  );
}


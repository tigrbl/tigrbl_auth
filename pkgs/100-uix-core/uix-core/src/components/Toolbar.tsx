import type { ReactNode } from "react";

export function Toolbar({ children }: { children: ReactNode }) {
  return <div className="tigrbl-toolbar">{children}</div>;
}


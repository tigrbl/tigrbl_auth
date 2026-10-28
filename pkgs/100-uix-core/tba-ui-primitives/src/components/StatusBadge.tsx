import type { UixTone } from "../types";

export function StatusBadge({ children, tone = "neutral" }: { children: string; tone?: UixTone }) {
  return <span className={`tba-badge tba-badge-${tone}`}>{children}</span>;
}


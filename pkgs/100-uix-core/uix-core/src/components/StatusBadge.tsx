import type { UixTone } from "../types";

export function StatusBadge({ children, tone = "neutral" }: { children: string; tone?: UixTone }) {
  return <span className={`tigrbl-badge tigrbl-badge-${tone}`}>{children}</span>;
}


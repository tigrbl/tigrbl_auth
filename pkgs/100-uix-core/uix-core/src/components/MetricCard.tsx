import type { HTMLAttributes, ReactNode } from "react";

export function MetricCard({
  description,
  label,
  value,
  ...props
}: HTMLAttributes<HTMLElement> & {
  description?: ReactNode;
  label: string;
  value: ReactNode;
}) {
  return (
    <article {...props} className={`tigrbl-metric-card ${props.className ?? ""}`.trim()}>
      <p className="tigrbl-metric-card-label">{label}</p>
      <strong className="tigrbl-metric-card-value">{value}</strong>
      {description && <p className="tigrbl-metric-card-description">{description}</p>}
    </article>
  );
}

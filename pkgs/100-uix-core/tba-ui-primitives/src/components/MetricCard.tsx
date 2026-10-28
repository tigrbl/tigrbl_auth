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
    <article {...props} className={`tba-metric-card ${props.className ?? ""}`.trim()}>
      <p className="tba-metric-card-label">{label}</p>
      <strong className="tba-metric-card-value">{value}</strong>
      {description && <p className="tba-metric-card-description">{description}</p>}
    </article>
  );
}

import type { HTMLAttributes, ReactNode } from "react";

export function Card({
  children,
  tone = "default",
  ...props
}: HTMLAttributes<HTMLDivElement> & {
  children: ReactNode;
  tone?: "default" | "compact" | "hero";
}) {
  return (
    <section {...props} className={`tba-card tba-card-${tone} ${props.className ?? ""}`.trim()}>
      {children}
    </section>
  );
}

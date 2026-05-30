import type { ReactNode } from "react";
import { BrandMark } from "./BrandMark";

export function BrandHeader({
  actions,
  label = "Tigrbl Auth",
  logoLetter
}: {
  actions?: ReactNode;
  label?: string;
  logoLetter?: string;
}) {
  return (
    <header className="tigrbl-brand-header">
      <BrandMark label={label} logoLetter={logoLetter} />
      {actions && <nav className="tigrbl-brand-header-actions">{actions}</nav>}
    </header>
  );
}

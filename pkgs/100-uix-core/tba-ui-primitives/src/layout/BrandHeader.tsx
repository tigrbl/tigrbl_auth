import type { ReactNode } from "react";
import { BrandMark } from "./BrandMark";

export function BrandHeader({
  actions,
  label = "TBA",
  logoLetter
}: {
  actions?: ReactNode;
  label?: string;
  logoLetter?: string;
}) {
  return (
    <header className="tba-brand-header">
      <BrandMark label={label} logoLetter={logoLetter} />
      {actions && <nav className="tba-brand-header-actions">{actions}</nav>}
    </header>
  );
}

export function BrandMark({
  label = "Tigrbl Auth",
  logoLetter
}: {
  label?: string;
  logoLetter?: string;
}) {
  const mark = logoLetter ?? (label.trim().charAt(0).toUpperCase() || "T");

  return (
    <div className="tigrbl-brand-mark">
      <span className="tigrbl-brand-mark-glyph">{mark}</span>
      <span className="tigrbl-brand-mark-label">{label}</span>
    </div>
  );
}

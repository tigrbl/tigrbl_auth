export function BrandMark({
  label = "TBA",
  logoLetter
}: {
  label?: string;
  logoLetter?: string;
}) {
  const mark = logoLetter ?? (label.trim().charAt(0).toUpperCase() || "T");

  return (
    <div className="tba-brand-mark">
      <span className="tba-brand-mark-glyph">{mark}</span>
      <span className="tba-brand-mark-label">{label}</span>
    </div>
  );
}

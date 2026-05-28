import type { ReactNode } from "react";

export function Button({
  children,
  onClick,
  variant = "primary"
}: {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "subtle" | "danger";
}) {
  const palette = {
    primary: { background: "#102620", color: "#ffffff", border: "#102620" },
    subtle: { background: "#ffffff", color: "#102620", border: "#b8cac3" },
    danger: { background: "#7f1d1d", color: "#ffffff", border: "#7f1d1d" }
  }[variant];

  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        ...palette,
        border: `1px solid ${palette.border}`,
        borderRadius: "8px",
        cursor: "pointer",
        font: "inherit",
        minHeight: "38px",
        padding: "0 14px"
      }}
    >
      {children}
    </button>
  );
}

export function Field({
  label,
  value,
  onChange,
  type = "text"
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
}) {
  return (
    <label style={{ display: "grid", gap: "6px", fontSize: "0.9rem", color: "#36524a" }}>
      {label}
      <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        style={{
          border: "1px solid #b8cac3",
          borderRadius: "8px",
          font: "inherit",
          minHeight: "38px",
          padding: "0 10px"
        }}
      />
    </label>
  );
}

export function Panel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section style={{ borderTop: "1px solid #c9d8d2", padding: "22px 0" }}>
      <h2 style={{ fontSize: "1.1rem", margin: "0 0 14px", color: "#102620" }}>{title}</h2>
      {children}
    </section>
  );
}

import type { ReactNode } from "react";

export function Button({
  children,
  onClick,
  variant = "primary",
  disabled = false,
  type = "button"
}: {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "subtle" | "danger";
  disabled?: boolean;
  type?: "button" | "submit";
}) {
  const palette = {
    primary: { background: "#14342b", color: "#ffffff", border: "#14342b" },
    subtle: { background: "#ffffff", color: "#14342b", border: "#bccbc5" },
    danger: { background: "#8f1f2d", color: "#ffffff", border: "#8f1f2d" }
  }[variant];

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{
        ...palette,
        border: `1px solid ${palette.border}`,
        borderRadius: "6px",
        cursor: disabled ? "not-allowed" : "pointer",
        font: "inherit",
        minHeight: "36px",
        opacity: disabled ? 0.62 : 1,
        padding: "0 12px"
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
  type = "text",
  required = false
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  required?: boolean;
}) {
  return (
    <label style={{ display: "grid", gap: "6px", fontSize: "0.88rem", color: "#37524a" }}>
      {label}
      <input
        type={type}
        required={required}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        style={{
          border: "1px solid #bccbc5",
          borderRadius: "6px",
          font: "inherit",
          minHeight: "36px",
          padding: "0 10px"
        }}
      />
    </label>
  );
}

export function Panel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section style={{ borderTop: "1px solid #d7dfdb", padding: "18px 0" }}>
      <h2 style={{ fontSize: "1rem", margin: "0 0 12px", color: "#102620" }}>{title}</h2>
      {children}
    </section>
  );
}

export function Notice({ tone, children }: { tone: "info" | "error" | "success"; children: ReactNode }) {
  const palette = {
    info: { background: "#eef6f2", border: "#9ab7ad", color: "#14342b" },
    error: { background: "#fff1f2", border: "#e29aa4", color: "#8f1f2d" },
    success: { background: "#eef9f0", border: "#96c69f", color: "#20532d" }
  }[tone];
  return (
    <div
      role={tone === "error" ? "alert" : "status"}
      style={{
        ...palette,
        border: `1px solid ${palette.border}`,
        borderRadius: "6px",
        padding: "10px 12px"
      }}
    >
      {children}
    </div>
  );
}

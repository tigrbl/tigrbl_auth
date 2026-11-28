function shortId(value: string) {
  if (value.length <= 14) return value;
  return `${value.slice(0, 8)}...${value.slice(-4)}`;
}

export function ShortId({ id }: { id: string }) {
  async function copy() {
    await navigator.clipboard.writeText(id);
  }

  return (
    <span style={{ alignItems: "center", display: "inline-flex", gap: "6px" }}>
      <code title={id}>{shortId(id)}</code>
      <button
        aria-label={`Copy ${id}`}
        onClick={() => void copy()}
        style={{
          alignItems: "center",
          background: "#edf4ef",
          border: "1px solid #c9d8cf",
          borderRadius: "7px",
          color: "#1f4d35",
          cursor: "pointer",
          display: "inline-flex",
          height: "24px",
          justifyContent: "center",
          padding: "0 6px"
        }}
        title="Copy full ID"
        type="button"
      >
        <svg aria-hidden="true" fill="none" height="14" viewBox="0 0 16 16" width="14">
          <path d="M5 5.5h7.5v8H5z" stroke="currentColor" strokeLinejoin="round" />
          <path d="M3.5 10.5h-1v-8H10v1" stroke="currentColor" strokeLinejoin="round" />
        </svg>
      </button>
    </span>
  );
}

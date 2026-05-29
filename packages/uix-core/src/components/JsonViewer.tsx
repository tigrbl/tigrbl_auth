export function JsonViewer({ value }: { value: unknown }) {
  return <pre className="tigrbl-json">{JSON.stringify(value, null, 2)}</pre>;
}


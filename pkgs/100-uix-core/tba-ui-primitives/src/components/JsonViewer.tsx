export function JsonViewer({ value }: { value: unknown }) {
  return <pre className="tba-json">{JSON.stringify(value, null, 2)}</pre>;
}

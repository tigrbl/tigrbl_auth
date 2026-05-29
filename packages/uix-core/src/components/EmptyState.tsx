export function EmptyState({ body, title }: { body?: string; title: string }) {
  return (
    <div className="tigrbl-empty-state">
      <h2>{title}</h2>
      {body && <p>{body}</p>}
    </div>
  );
}


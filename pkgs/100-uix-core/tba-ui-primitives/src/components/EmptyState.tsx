export function EmptyState({ body, title }: { body?: string; title: string }) {
  return (
    <div className="tba-empty-state">
      <h2>{title}</h2>
      {body && <p>{body}</p>}
    </div>
  );
}


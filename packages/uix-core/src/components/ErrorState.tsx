export function ErrorState({ message, title = "Something went wrong" }: { message: string; title?: string }) {
  return (
    <div className="tigrbl-error-state" role="alert">
      <h2>{title}</h2>
      <p>{message}</p>
    </div>
  );
}


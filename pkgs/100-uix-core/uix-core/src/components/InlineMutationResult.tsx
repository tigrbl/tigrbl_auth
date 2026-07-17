import { Toast } from "./Toast";

export function InlineMutationResult({
  error,
  success
}: {
  error?: string | null;
  success?: string | null;
}) {
  if (error) return <Toast message={error} tone="danger" />;
  if (success) return <Toast message={success} tone="success" />;
  return null;
}

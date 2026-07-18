import { ErrorState } from "./ErrorState";

export function RequestErrorNotice({
  message,
  title = "Request failed"
}: {
  message?: string | null;
  title?: string;
}) {
  if (!message) return null;
  return <ErrorState title={title} message={message} />;
}

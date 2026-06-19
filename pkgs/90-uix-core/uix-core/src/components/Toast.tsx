import type { UixTone } from "../types";

export function Toast({ message, tone = "neutral" }: { message: string; tone?: UixTone }) {
  return <div className={`tigrbl-toast tigrbl-toast-${tone}`}>{message}</div>;
}


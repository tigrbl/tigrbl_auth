import type { UixTone } from "../types";

export function Toast({ message, tone = "neutral" }: { message: string; tone?: UixTone }) {
  return <div className={`tba-toast tba-toast-${tone}`}>{message}</div>;
}


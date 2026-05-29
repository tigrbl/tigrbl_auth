import type { TextareaHTMLAttributes } from "react";

export function JsonEditor(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return <textarea {...props} className={`tigrbl-json-editor ${props.className ?? ""}`.trim()} spellCheck={false} />;
}


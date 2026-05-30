import type { InputHTMLAttributes } from "react";
import { FormField } from "./FormField";

export function Input(props: InputHTMLAttributes<HTMLInputElement> & {
  error?: string;
  help?: string;
  label: string;
}) {
  return <FormField {...props} />;
}

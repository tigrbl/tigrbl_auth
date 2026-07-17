import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Button } from "./Button";

export function SubmitButton({
  children,
  loading = false,
  loadingLabel = "Working...",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  loading?: boolean;
  loadingLabel?: string;
}) {
  return (
    <Button {...props} disabled={loading || props.disabled} type={props.type ?? "submit"}>
      {loading ? loadingLabel : children}
    </Button>
  );
}

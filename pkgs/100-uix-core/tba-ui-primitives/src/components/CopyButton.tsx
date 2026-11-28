import { Button } from "./Button";

export function CopyButton({ text }: { text: string }) {
  async function copy() {
    await navigator.clipboard.writeText(text);
  }
  return <Button onClick={() => void copy()} type="button" variant="subtle">Copy</Button>;
}


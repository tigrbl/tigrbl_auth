import { Button } from "./Button";
import { Modal } from "./Modal";

export function ConfirmDialog({
  body,
  confirmLabel = "Confirm",
  onCancel,
  onConfirm,
  open,
  title
}: {
  body: string;
  confirmLabel?: string;
  onCancel: () => void;
  onConfirm: () => void;
  open: boolean;
  title: string;
}) {
  return (
    <Modal onClose={onCancel} open={open} title={title}>
      <p>{body}</p>
      <div className="tigrbl-actions">
        <Button onClick={onCancel} type="button" variant="subtle">Cancel</Button>
        <Button onClick={onConfirm} type="button" variant="danger">{confirmLabel}</Button>
      </div>
    </Modal>
  );
}


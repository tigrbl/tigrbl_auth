import type { ReactNode } from "react";
import { Modal } from "./Modal";

function ResourceDialog({
  children,
  description,
  onClose,
  open,
  title
}: {
  children: ReactNode;
  description?: ReactNode;
  onClose: () => void;
  open: boolean;
  title: string;
}) {
  return (
    <Modal onClose={onClose} open={open} title={title}>
      {description && <p className="tigrbl-dialog-description">{description}</p>}
      {children}
    </Modal>
  );
}

export function CreateResourceDialog(props: {
  children: ReactNode;
  description?: ReactNode;
  onClose: () => void;
  open: boolean;
  title: string;
}) {
  return <ResourceDialog {...props} />;
}

export function EditResourceDialog(props: {
  children: ReactNode;
  description?: ReactNode;
  onClose: () => void;
  open: boolean;
  title: string;
}) {
  return <ResourceDialog {...props} />;
}

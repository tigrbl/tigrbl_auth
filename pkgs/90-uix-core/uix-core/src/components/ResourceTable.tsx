import type { ReactNode } from "react";
import { DataTable, type DataTableColumn } from "./DataTable";
import { EmptyState } from "./EmptyState";

export type ResourceTableAction<T> = {
  label: string;
  onClick: (item: T) => void;
  tone?: "danger" | "primary" | "subtle";
};

export function ResourceTable<T>({
  actions,
  columns,
  emptyBody,
  emptyTitle,
  getRowKey,
  items
}: {
  actions?: ResourceTableAction<T>[];
  columns: DataTableColumn<T>[];
  emptyBody?: string;
  emptyTitle?: string;
  getRowKey: (item: T) => string;
  items: T[];
}) {
  const tableColumns = actions?.length
    ? [
        ...columns,
        {
          header: "Actions",
          key: "actions",
          render: (item: T): ReactNode => (
            <div className="tigrbl-row-actions">
              {actions.map((action) => (
                <button
                  className={`tigrbl-row-action tigrbl-row-action-${action.tone ?? "subtle"}`}
                  key={action.label}
                  onClick={() => action.onClick(item)}
                  type="button"
                >
                  {action.label}
                </button>
              ))}
            </div>
          )
        } satisfies DataTableColumn<T>
      ]
    : columns;

  return (
    <DataTable
      columns={tableColumns}
      empty={<EmptyState title={emptyTitle ?? "No resources"} body={emptyBody ?? "Create a resource to begin."} />}
      getRowKey={getRowKey}
      items={items}
    />
  );
}

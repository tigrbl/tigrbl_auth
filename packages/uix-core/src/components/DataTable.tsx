import type { ReactNode } from "react";
import { EmptyState } from "./EmptyState";

export interface DataTableColumn<T> {
  header: string;
  key: string;
  render: (item: T) => ReactNode;
}

export function DataTable<T>({
  columns,
  empty,
  getRowKey,
  items
}: {
  columns: DataTableColumn<T>[];
  empty?: ReactNode;
  getRowKey: (item: T) => string;
  items: T[];
}) {
  if (items.length === 0) {
    return <>{empty ?? <EmptyState title="No records" body="There are no records to show yet." />}</>;
  }

  return (
    <div className="tigrbl-table-wrap">
      <table className="tigrbl-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key}>{column.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={getRowKey(item)}>
              {columns.map((column) => (
                <td key={column.key}>{column.render(item)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


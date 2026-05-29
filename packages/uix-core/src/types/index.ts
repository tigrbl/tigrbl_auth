export type UixTone = "neutral" | "success" | "warning" | "danger" | "info";

export interface NavigationItem {
  href: string;
  label: string;
  description?: string;
  badge?: string;
}

export interface ResourcePage<T> {
  items: T[];
  cursor?: string | null;
  total?: number;
}


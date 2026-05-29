import type { NavigationItem } from "../types";

export function Breadcrumbs({ items }: { items: NavigationItem[] }) {
  return (
    <nav aria-label="Breadcrumbs" className="tigrbl-breadcrumbs">
      {items.map((item, index) => (
        <a href={item.href} key={item.href} aria-current={index === items.length - 1 ? "page" : undefined}>
          {item.label}
        </a>
      ))}
    </nav>
  );
}


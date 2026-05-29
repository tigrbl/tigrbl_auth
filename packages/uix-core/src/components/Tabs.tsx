import type { NavigationItem } from "../types";

export function Tabs({ activeHref, items }: { activeHref: string; items: NavigationItem[] }) {
  return (
    <nav className="tigrbl-tabs">
      {items.map((item) => (
        <a aria-current={activeHref === item.href ? "page" : undefined} href={item.href} key={item.href}>
          {item.label}
        </a>
      ))}
    </nav>
  );
}


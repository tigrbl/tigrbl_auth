import type { NavigationItem } from "../types";

export function Sidebar({
  activeHref,
  apiBaseUrl,
  items,
  productApi,
  title
}: {
  activeHref: string;
  apiBaseUrl?: string;
  items: NavigationItem[];
  productApi: string;
  title: string;
}) {
  return (
    <aside className="tigrbl-sidebar">
      <p className="tigrbl-sidebar-product">{productApi}</p>
      <h1>{title}</h1>
      <nav>
        {items.map((item) => {
          const active = activeHref === item.href || activeHref.startsWith(`${item.href}/`);
          return (
            <a aria-current={active ? "page" : undefined} href={item.href} key={item.href}>
              <span>{item.label}</span>
              {item.badge && <small>{item.badge}</small>}
            </a>
          );
        })}
      </nav>
      {apiBaseUrl && <p className="tigrbl-sidebar-api">API: <code>{apiBaseUrl}</code></p>}
    </aside>
  );
}


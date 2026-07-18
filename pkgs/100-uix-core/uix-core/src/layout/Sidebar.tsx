import type { NavigationItem } from "../types";

export function Sidebar({
  activeHref,
  backendAppBaseUrl,
  items,
  backendApp,
  title
}: {
  activeHref: string;
  backendAppBaseUrl?: string;
  items: NavigationItem[];
  backendApp: string;
  title: string;
}) {
  return (
    <aside className="tigrbl-sidebar">
      <p className="tigrbl-sidebar-product">{backendApp}</p>
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
      {backendAppBaseUrl && <p className="tigrbl-sidebar-backend">Backend: <code>{backendAppBaseUrl}</code></p>}
    </aside>
  );
}


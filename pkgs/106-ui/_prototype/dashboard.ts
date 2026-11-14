export type Row = Record<string, unknown>;
type Column = [label: string, key: string];
type View = { name: string; path: string; columns: Column[]; select?: (data: unknown) => unknown };

export function element<K extends keyof HTMLElementTagNameMap>(tag: K, text?: string) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  return node;
}

export function page(title: string, description: string) {
  const main = element("main");
  const header = element("header");
  const label = element("p", "TBA / LOCAL PROTOTYPE");
  label.className = "eyebrow";
  header.append(label, element("h1", title), element("p", description));
  main.append(header);
  document.getElementById("root")!.replaceChildren(main);
  return main;
}

export async function json(path: string, options?: RequestInit): Promise<unknown> {
  const response = await fetch(path, { cache: "no-store", ...options });
  if (!response.ok) throw new Error("Request failed (HTTP " + response.status + ").");
  if (!response.headers.get("content-type")?.includes("application/json")) {
    throw new Error("The local API did not return JSON. Start the prototype server and try again.");
  }
  return response.json();
}

function field(row: Row, key: string): string {
  let value: unknown = row;
  for (const part of key.split(".")) {
    value = value && typeof value === "object" ? (value as Row)[part] : undefined;
  }
  return typeof value === "string" || typeof value === "number" || typeof value === "boolean"
    ? String(value)
    : "—";
}

export function dashboard(title: string, description: string, views: [View, ...View[]]) {
  const main = page(title, description);
  const controls = element("div");
  controls.className = "controls";
  const viewLabel = element("label", "View");
  const select = element("select");
  views.forEach(({ name }, index) => {
    const option = element("option", name);
    option.value = String(index);
    select.append(option);
  });
  viewLabel.append(select);
  const searchLabel = element("label", "Filter records");
  const search = element("input");
  search.type = "search";
  searchLabel.append(search);
  const refresh = element("button", "Refresh");
  refresh.type = "button";
  controls.append(viewLabel, searchLabel, refresh);
  const status = element("p");
  status.setAttribute("role", "status");
  const results = element("section");
  results.className = "results";
  main.append(controls, status, results);
  let view = views[0];
  let rows: Row[] = [];
  let request = 0;

  function render() {
    const query = search.value.trim().toLowerCase();
    const filtered = rows.filter(row => view.columns.some(([, key]) => field(row, key).toLowerCase().includes(query)));
    status.textContent = filtered.length === 0 ? "No records to display." :
      filtered.length + " of " + rows.length + " records";
    results.replaceChildren();
    if (!filtered.length) return;
    const table = element("table");
    const caption = element("caption", view.name);
    const head = element("thead");
    const headings = element("tr");
    for (const [label] of view.columns) {
      const th = element("th", label);
      th.scope = "col";
      headings.append(th);
    }
    head.append(headings);
    const body = element("tbody");
    for (const record of filtered) {
      const row = element("tr");
      for (const [, key] of view.columns) row.append(element("td", field(record, key)));
      body.append(row);
    }
    table.append(caption, head, body);
    results.append(table);
  }

  async function load() {
    const id = ++request;
    view = views[Number(select.value)];
    rows = [];
    results.replaceChildren();
    status.textContent = "Loading " + view.name.toLowerCase() + "…";
    refresh.disabled = search.disabled = true;
    try {
      const data = await json(view.path);
      if (id !== request) return;
      const selected = view.select ? view.select(data) : data;
      if (!Array.isArray(selected) || selected.some(row => !row || typeof row !== "object")) {
        throw new Error("The local API returned an unexpected record format.");
      }
      rows = selected;
      render();
    } catch (error) {
      if (id === request) status.textContent = error instanceof Error ? error.message : "Unable to load records.";
    } finally {
      if (id === request) refresh.disabled = search.disabled = false;
    }
  }

  select.addEventListener("change", () => { search.value = ""; void load(); });
  refresh.addEventListener("click", () => void load());
  search.addEventListener("input", render);
  void load();
  return main;
}

export function walkthrough(title: string, description: string, flows: Record<string, [string, ...string[]]>) {
  const main = page(title, description);
  const controls = element("div");
  controls.className = "controls";
  const label = element("label", "Demo flow");
  const select = element("select");
  Object.keys(flows).forEach(name => select.append(element("option", name)));
  label.append(select);
  controls.append(label);
  const section = element("section");
  section.className = "panel";
  const progress = element("p");
  progress.setAttribute("role", "status");
  const step = element("p");
  const next = element("button");
  next.type = "button";
  section.append(element("h2", "Walkthrough"), progress, step, next);
  main.append(controls, section);
  let index = 0;
  function render() {
    const steps = flows[select.value];
    const complete = index === steps.length;
    progress.textContent = complete ? "Demo complete" : "Step " + (index + 1) + " of " + steps.length;
    step.textContent = complete ? "Choose another flow or start this walkthrough again." : steps[index];
    next.textContent = complete ? "Start again" : index + 1 === steps.length ? "Finish demo" : "Continue";
  }
  select.addEventListener("change", () => { index = 0; render(); });
  next.addEventListener("click", () => {
    index = index === flows[select.value].length ? 0 : index + 1;
    render();
  });
  render();
}

type Props = { section: string };

export function AccessManagementPage({ section }: Props) {
  return <section aria-labelledby="access-heading"><h1 id="access-heading">Customer IAM: {section}</h1><p>Tenant-scoped assignments are evaluated with default deny. Changes require confirmation and produce audit evidence.</p></section>;
}

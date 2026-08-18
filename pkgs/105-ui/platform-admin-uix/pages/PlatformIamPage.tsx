type Props = { section: string };

export function PlatformIamPage({ section }: Props) {
  return <section aria-labelledby="platform-iam-heading"><h1 id="platform-iam-heading">Platform IAM: {section}</h1><p>Internal authority changes require explicit authorization, reason capture, and decision provenance.</p></section>;
}

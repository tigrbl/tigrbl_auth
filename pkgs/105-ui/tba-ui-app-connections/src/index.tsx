export type PermissionStatus =
  | "requested" | "available_to_request"
  | "unavailable_for_account" | "unavailable_for_bot";

export type Permission = {
  id: string;
  label: string;
  status: PermissionStatus;
  explicit?: boolean;
};

type Identity = { id: string; name: string };

export function IdentityPicker({ accountName, bots, value, onChange, className, inputClassName }: {
  accountName: string;
  bots: readonly Identity[];
  value: string;
  onChange: (id: string) => void;
  className?: string;
  inputClassName?: string;
}) {
  return (
    <label className={className}>
      Act as
      <select className={inputClassName} value={value} onChange={event => onChange(event.target.value)}>
        <option value="">{accountName} · Your account</option>
        {bots.map(bot => <option key={bot.id} value={bot.id}>{bot.name} · Bot</option>)}
      </select>
    </label>
  );
}

const explanations: Record<Exclude<PermissionStatus, "requested">, string> = {
  available_to_request: "Available to request. Reconnect the app requesting this permission.",
  unavailable_for_account: "Unavailable to your account.",
  unavailable_for_bot: "Unavailable to this bot.",
};

export function PermissionMatrix({ title, permissions, selected, onChange, className, rowClassName }: {
  title: string;
  permissions: readonly Permission[];
  selected: readonly string[];
  onChange: (scopes: string[]) => void;
  className?: string;
  rowClassName?: string;
}) {
  return (
    <fieldset className={className}>
      <legend>{title}</legend>
      {permissions.map(permission => {
        const eligible = permission.status === "requested";
        return (
          <label key={permission.id} className={rowClassName}>
            <input type="checkbox" disabled={!eligible}
              checked={eligible && selected.includes(permission.id)}
              onChange={event => onChange(event.target.checked
                ? [...selected, permission.id] : selected.filter(id => id !== permission.id))} />
            <span>{permission.label}{permission.status !== "requested" &&
              <small style={{ display: "block" }}>{explanations[permission.status]}</small>}
            </span>
          </label>
        );
      })}
    </fieldset>
  );
}

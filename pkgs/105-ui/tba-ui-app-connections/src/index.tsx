import type {
  AppConnectionBot,
  AppConnectionPermission,
  AppConnectionPermissionStatus,
} from "@tba/client-app-connections";

export type PermissionStatus = AppConnectionPermissionStatus;
export type Permission = AppConnectionPermission;

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

export function defaultConsentScopes(permissions: readonly Permission[]): string[] {
  return permissions
    .filter(permission => permission.status === "requested" && !permission.explicit)
    .map(permission => permission.id);
}

export function ConsentIdentityControls({
  accountName,
  bots,
  permissions,
  value,
  onChange,
  title,
  identityClassName,
  inputClassName,
  matrixClassName,
  rowClassName,
}: {
  accountName: string;
  bots: readonly AppConnectionBot[];
  permissions: readonly Permission[];
  value: { botId: string; scopes: readonly string[] };
  onChange: (selection: { botId: string; scopes: string[] }) => void;
  title: string;
  identityClassName?: string;
  inputClassName?: string;
  matrixClassName?: string;
  rowClassName?: string;
}) {
  function permissionsFor(botId: string): readonly Permission[] {
    return botId ? bots.find(bot => bot.id === botId)?.permissions ?? [] : permissions;
  }

  function requestedScopes(botId: string, scopes: readonly string[]): string[] {
    const eligible = new Set(
      permissionsFor(botId).filter(permission => permission.status === "requested").map(permission => permission.id),
    );
    return scopes.filter(scope => eligible.has(scope));
  }

  return (
    <>
      <IdentityPicker accountName={accountName} bots={bots} value={value.botId}
        onChange={botId => onChange({ botId, scopes: requestedScopes(botId, value.scopes) })}
        className={identityClassName} inputClassName={inputClassName} />
      <PermissionMatrix title={title} permissions={permissionsFor(value.botId)}
        selected={requestedScopes(value.botId, value.scopes)}
        onChange={scopes => onChange({ botId: value.botId, scopes: requestedScopes(value.botId, scopes) })}
        className={matrixClassName}
        rowClassName={rowClassName} />
    </>
  );
}

export function hasEveryPermission(granted: string[], required: string[]): boolean {
  const grantedSet = new Set(granted);
  return required.every((permission) => grantedSet.has(permission));
}

export function hasAnyPermission(granted: string[], required: string[]): boolean {
  const grantedSet = new Set(granted);
  return required.some((permission) => grantedSet.has(permission));
}


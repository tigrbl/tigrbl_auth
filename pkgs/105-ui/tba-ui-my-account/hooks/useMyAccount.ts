import { useEffect, useState } from "react";
import { myAccountClient } from "../services/myAccountClient";
import type { AccountProfile } from "../types";

export function useMyAccount() {
  const [profile, setProfile] = useState<AccountProfile | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      setProfile(await myAccountClient.profile());
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unable to load account");
    } finally {
      setLoading(false);
    }
  }

  async function updateProfile(username: string, email: string) {
    setProfile(await myAccountClient.updateProfile({ username, email }));
  }

  async function changePassword(currentPassword: string, newPassword: string) {
    await myAccountClient.changePassword(currentPassword, newPassword);
    await refresh();
  }

  useEffect(() => {
    void refresh();
  }, []);

  return { profile, loading, error, refresh, updateProfile, changePassword };
}

import { useState } from "react";

export function useApiMutation<TArgs extends unknown[], TResult>(mutation: (...args: TArgs) => Promise<TResult>) {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function run(...args: TArgs): Promise<TResult | null> {
    setError(null);
    setLoading(true);
    try {
      return await mutation(...args);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Request failed");
      return null;
    } finally {
      setLoading(false);
    }
  }

  return { error, loading, run };
}


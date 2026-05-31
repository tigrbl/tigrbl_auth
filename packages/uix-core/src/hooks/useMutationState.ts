import { useCallback, useState } from "react";

export function useMutationState<TArgs extends unknown[], TResult>(
  mutation: (...args: TArgs) => Promise<TResult>,
  options: {
    successMessage?: string | ((result: TResult) => string);
  } = {}
) {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  const reset = useCallback(() => {
    setError(null);
    setSuccess(null);
  }, []);

  const run = useCallback(
    async (...args: TArgs): Promise<TResult | null> => {
      setError(null);
      setSuccess(null);
      setLoading(true);
      try {
        const result = await mutation(...args);
        if (options.successMessage) {
          setSuccess(
            typeof options.successMessage === "function"
              ? options.successMessage(result)
              : options.successMessage
          );
        }
        return result;
      } catch (nextError) {
        setError(nextError instanceof Error ? nextError.message : "Request failed");
        return null;
      } finally {
        setLoading(false);
      }
    },
    [mutation, options.successMessage]
  );

  return { error, loading, reset, run, success };
}

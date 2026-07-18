import { useEffect, useState } from "react";

export interface TransportQueryState<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
}

export function useTransportQuery<T>(loader: (signal: AbortSignal) => Promise<T>, deps: unknown[] = []): TransportQueryState<T> {
  const [state, setState] = useState<TransportQueryState<T>>({ data: null, error: null, loading: true });

  useEffect(() => {
    const controller = new AbortController();
    setState((current) => ({ ...current, error: null, loading: true }));
    loader(controller.signal)
      .then((data) => setState({ data, error: null, loading: false }))
      .catch((error: unknown) => {
        if (!controller.signal.aborted) {
          setState({ data: null, error: error instanceof Error ? error.message : "Request failed", loading: false });
        }
      });
    return () => controller.abort();
    // The caller owns dependency stability for product-specific loaders.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}


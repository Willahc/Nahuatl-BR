import { useCallback, useEffect, useState } from "react";
import { loadPreview } from "./data";
import type { PreviewData } from "./types";

interface PreviewState {
  data: PreviewData | null;
  error: string | null;
  loading: boolean;
}

export function usePreview(): PreviewState & { reload: () => void } {
  const [state, setState] = useState<PreviewState>({
    data: null,
    error: null,
    loading: true,
  });

  const reload = useCallback(() => {
    let active = true;
    setState((prev) => ({ ...prev, loading: true, error: null }));
    loadPreview()
      .then((data) => {
        if (active) setState({ data, error: null, loading: false });
      })
      .catch((error: unknown) => {
        if (active) {
          setState({
            data: null,
            error: error instanceof Error ? error.message : String(error),
            loading: false,
          });
        }
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => reload(), [reload]);

  return { ...state, reload };
}
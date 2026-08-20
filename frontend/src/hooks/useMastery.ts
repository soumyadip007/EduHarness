"use client";

import { useCallback, useEffect, useState } from "react";
import { getJson } from "@/lib/api";

export function useMastery(sessionId?: string) {
  const [mastery, setMastery] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(
    (overrideSessionId?: string) => {
      const sid = overrideSessionId || sessionId;
      if (!sid) {
        setLoading(false);
        return Promise.resolve();
      }
      setLoading(true);
      return getJson<{ mastery: Record<string, number> }>(`/api/student/mastery?session_id=${encodeURIComponent(sid)}`)
        .then((d) => setMastery(d.mastery || {}))
        .finally(() => setLoading(false));
    },
    [sessionId]
  );

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return { mastery, loading, refresh };
}

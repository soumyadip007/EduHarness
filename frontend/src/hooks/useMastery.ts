"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";

export function useMastery() {
  const [mastery, setMastery] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);

  const refresh = (sessionId: string = "student-demo-session") => {
    setLoading(true);
    return getJson<{ mastery: Record<string, number> }>(`/api/student/mastery?session_id=${encodeURIComponent(sessionId)}`)
      .then((d) => setMastery(d.mastery || {}))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    void refresh();
  }, []);

  return { mastery, loading, refresh };
}

"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";

export function useMastery() {
  const [mastery, setMastery] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getJson<{ mastery: Record<string, number> }>("/api/student/mastery")
      .then((d) => setMastery(d.mastery || {}))
      .finally(() => setLoading(false));
  }, []);

  return { mastery, loading };
}

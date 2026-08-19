"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";

type QueueItem = { escalation_id: string; priority: string; reason: string };

export function useEscalation() {
  const [items, setItems] = useState<QueueItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getJson<{ items: QueueItem[] }>("/api/teacher/queue")
      .then((d) => setItems(d.items || []))
      .finally(() => setLoading(false));
  }, []);

  return { items, loading };
}

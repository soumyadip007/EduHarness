"use client";

import { useEffect, useState } from "react";
import { API_BASE, getJson } from "@/lib/api";

type QueueItem = { escalation_id: string; priority: string; reason: string };

export function useEscalation() {
  const [items, setItems] = useState<QueueItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const refresh = () =>
      getJson<{ items: QueueItem[] }>("/api/teacher/queue")
        .then((d) => setItems(d.items || []))
        .finally(() => setLoading(false));

    void refresh();

    const wsBase = API_BASE.replace("http://", "ws://").replace("https://", "wss://");
    const ws = new WebSocket(`${wsBase}/ws/escalation`);
    ws.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data) as { event?: string };
        if (data.event === "queue_updated") {
          void refresh();
        }
      } catch {
        // ignore non-JSON websocket messages
      }
    };
    return () => ws.close();
  }, []);

  return { items, loading };
}

"use client";

import { useEffect, useState } from "react";
import AuditTimeline from "@/components/governance/AuditTimeline";
import { getJson } from "@/lib/api";

type AuditItem = { id: string; action: string; by: string; at: string };

export default function TeacherAuditPage() {
  const [events, setEvents] = useState<AuditItem[]>([]);
  useEffect(() => {
    getJson<{ events: AuditItem[] }>("/api/teacher/audit").then((d) => setEvents(d.events || []));
  }, []);

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Audit Trail</h1>
      <AuditTimeline events={events} />
    </main>
  );
}

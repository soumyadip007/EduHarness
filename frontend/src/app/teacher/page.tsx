"use client";

import EscalationCard from "@/components/governance/EscalationCard";
import { useEscalation } from "@/hooks/useEscalation";
import { postJson } from "@/lib/api";

export default function TeacherPage() {
  const { items, loading } = useEscalation();
  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Teacher Review Queue</h1>
      <button onClick={() => postJson("/api/teacher/queue/simulate", {})} style={{ marginBottom: 12 }}>
        Simulate escalation
      </button>
      {loading ? <p>Loading...</p> : null}
      {items.map((i) => (
        <EscalationCard key={i.escalation_id} id={i.escalation_id} priority={i.priority} reason={i.reason} />
      ))}
    </main>
  );
}

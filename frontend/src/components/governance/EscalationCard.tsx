"use client";

export default function EscalationCard({ id, priority, reason }: { id: string; priority: string; reason: string }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 10, marginBottom: 8 }}>
      <div><strong>{id}</strong> ({priority})</div>
      <div style={{ color: "#555" }}>{reason}</div>
    </div>
  );
}

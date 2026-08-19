"use client";

export default function MasteryBar({ concept, value }: { concept: string; value: number }) {
  const pct = Math.max(0, Math.min(100, Math.round(value * 100)));
  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <span>{concept}</span>
        <span>{pct}%</span>
      </div>
      <div style={{ height: 8, background: "#e5e7eb", borderRadius: 999 }}>
        <div style={{ width: `${pct}%`, height: 8, background: "#2563eb", borderRadius: 999 }} />
      </div>
    </div>
  );
}

"use client";

type Point = { label: string; value: number };

export default function AblationBar({ points }: { points: Point[] }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <h3 style={{ marginTop: 0 }}>Ablation (TTI)</h3>
      {points.map((p) => (
        <div key={p.label} style={{ marginBottom: 6 }}>
          <div style={{ fontSize: 12 }}>{p.label}</div>
          <div style={{ width: `${Math.max(2, Math.round(p.value * 100))}%`, background: "#2563eb", color: "white", padding: "2px 6px" }}>
            {p.value.toFixed(2)}
          </div>
        </div>
      ))}
    </div>
  );
}

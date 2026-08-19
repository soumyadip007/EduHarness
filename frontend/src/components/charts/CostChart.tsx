"use client";

type CostRow = { condition: string; usd: number };

export default function CostChart({ rows }: { rows: CostRow[] }) {
  const max = Math.max(...rows.map((r) => r.usd), 1);
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <h3 style={{ marginTop: 0 }}>Cost by Condition</h3>
      {rows.map((r) => (
        <div key={r.condition} style={{ marginBottom: 6 }}>
          <div style={{ fontSize: 12 }}>{r.condition}</div>
          <div style={{ width: `${Math.max(3, Math.round((r.usd / max) * 100))}%`, background: "#059669", color: "white", padding: "2px 6px" }}>
            ${r.usd.toFixed(2)}
          </div>
        </div>
      ))}
    </div>
  );
}

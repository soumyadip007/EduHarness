"use client";

type Cell = { model: string; harness: string; tti: number };

export default function InteractionPlot({ cells }: { cells: Cell[] }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <h3 style={{ marginTop: 0 }}>Model x Harness Interaction</h3>
      <ul style={{ margin: 0, paddingLeft: 18 }}>
        {cells.map((c, idx) => (
          <li key={`${c.model}-${c.harness}-${idx}`}>
            {c.model} / {c.harness}: {c.tti.toFixed(3)}
          </li>
        ))}
      </ul>
    </div>
  );
}

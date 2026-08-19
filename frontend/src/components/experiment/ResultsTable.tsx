"use client";

type Row = {
  condition: string;
  safety_adversarial: number;
  delta_solve_rate: number;
  state_divergence: number;
};

export default function ResultsTable({ rows }: { rows: Row[] }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>Condition</th>
          <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>Safety</th>
          <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>Delta Solve</th>
          <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>State Div.</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r) => (
          <tr key={r.condition}>
            <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{r.condition}</td>
            <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{r.safety_adversarial.toFixed(3)}</td>
            <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{r.delta_solve_rate.toFixed(3)}</td>
            <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{r.state_divergence.toFixed(3)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

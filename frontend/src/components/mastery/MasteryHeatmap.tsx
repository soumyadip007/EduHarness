"use client";

type HeatmapData = {
  studentId: string;
  mastery: Record<string, number>;
};

const scoreColor = (score: number): string => {
  if (score >= 0.75) {
    return "#166534";
  }
  if (score >= 0.5) {
    return "#92400e";
  }
  return "#991b1b";
};

export default function MasteryHeatmap({ rows }: { rows: HeatmapData[] }) {
  const concepts = Array.from(new Set(rows.flatMap((r) => Object.keys(r.mastery))));
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 12 }}>
      <thead>
        <tr>
          <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>Student</th>
          {concepts.map((c) => (
            <th key={c} style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>
              {c}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.studentId}>
            <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{row.studentId}</td>
            {concepts.map((c) => {
              const score = row.mastery[c] ?? 0;
              return (
                <td key={`${row.studentId}-${c}`} style={{ borderBottom: "1px solid #eee", padding: 8 }}>
                  <span style={{ color: scoreColor(score), fontWeight: 600 }}>{Math.round(score * 100)}%</span>
                </td>
              );
            })}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

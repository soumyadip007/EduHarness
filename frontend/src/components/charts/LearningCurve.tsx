"use client";

export default function LearningCurve({ values }: { values: number[] }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <h3 style={{ marginTop: 0 }}>Learning Curve</h3>
      <p>{values.map((v) => v.toFixed(2)).join(" -> ")}</p>
    </div>
  );
}

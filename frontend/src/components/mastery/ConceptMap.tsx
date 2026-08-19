"use client";

type Mastery = Record<string, number>;

export default function ConceptMap({ mastery }: { mastery: Mastery }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 12 }}>
      <h3 style={{ marginTop: 0 }}>Concept Map (Simplified)</h3>
      <ul>
        {Object.entries(mastery).map(([k, v]) => (
          <li key={k}>
            {k} {v >= 0.7 ? "✓" : v >= 0.4 ? "◐" : "○"}
          </li>
        ))}
      </ul>
    </div>
  );
}

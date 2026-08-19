"use client";

import ConceptMap from "@/components/mastery/ConceptMap";
import MasteryBar from "@/components/mastery/MasteryBar";
import { useMastery } from "@/hooks/useMastery";

export default function StudentProgressPage() {
  const { mastery, loading } = useMastery();

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
      <h1>Progress & Mastery</h1>
      {loading ? <p>Loading mastery...</p> : null}
      {!loading ? (
        <>
          <ConceptMap mastery={mastery} />
          <div style={{ marginTop: 16, border: "1px solid #ddd", borderRadius: 10, padding: 12 }}>
            <h3 style={{ marginTop: 0 }}>Mastery Bars</h3>
            {Object.entries(mastery).map(([c, v]) => (
              <MasteryBar key={c} concept={c} value={v} />
            ))}
          </div>
        </>
      ) : null}
    </main>
  );
}

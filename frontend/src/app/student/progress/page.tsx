"use client";

import { useEffect, useState } from "react";
import ConceptMap from "@/components/mastery/ConceptMap";
import MasteryBar from "@/components/mastery/MasteryBar";
import { useMastery } from "@/hooks/useMastery";
import { useSessionId } from "@/hooks/useSessionId";
import { getJson } from "@/lib/api";

type PlanStep = {
  concept: string;
  mastery: number;
  status: string;
  recommended_action: string;
};

export default function StudentProgressPage() {
  const { sessionId } = useSessionId();
  const { mastery, loading } = useMastery(sessionId);
  const [planSteps, setPlanSteps] = useState<PlanStep[]>([]);

  useEffect(() => {
    if (!sessionId) return;
    getJson<{ plan: { steps: PlanStep[] } }>(`/api/student/progress-plan?session_id=${encodeURIComponent(sessionId)}`).then(
      (data) => setPlanSteps(data.plan?.steps || [])
    );
  }, [sessionId]);

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
      <h1>Progress & Mastery</h1>
      <p>Session: {sessionId}</p>
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
          <div style={{ marginTop: 16, border: "1px solid #ddd", borderRadius: 10, padding: 12 }}>
            <h3 style={{ marginTop: 0 }}>Learning Plan</h3>
            <ul>
              {planSteps.map((step) => (
                <li key={step.concept}>
                  <strong>{step.concept}</strong> ({step.status}) — {step.recommended_action}
                </li>
              ))}
            </ul>
          </div>
        </>
      ) : null}
    </main>
  );
}

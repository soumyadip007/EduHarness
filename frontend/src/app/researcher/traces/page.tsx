"use client";

import { useEffect, useState } from "react";
import InteractionPlot from "@/components/charts/InteractionPlot";
import { getJson } from "@/lib/api";

export default function ResearcherTracesPage() {
  const [traces, setTraces] = useState<Record<string, unknown>[]>([]);
  useEffect(() => {
    getJson<{ traces: Record<string, unknown>[] }>("/api/researcher/traces").then((d) => setTraces(d.traces || []));
  }, []);
  return (
    <main style={{ maxWidth: 980, margin: "0 auto", padding: 24 }}>
      <h1>Trace Explorer</h1>
      <InteractionPlot
        cells={[
          { model: "mid", harness: "H0", tti: 0.41 },
          { model: "mid", harness: "H3", tti: 0.69 },
          { model: "frontier", harness: "H3", tti: 0.73 },
        ]}
      />
      <pre style={{ whiteSpace: "pre-wrap", marginTop: 12 }}>{JSON.stringify(traces, null, 2)}</pre>
    </main>
  );
}
"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";

export default function ResearcherTracesPage() {
  const [traces, setTraces] = useState<Record<string, unknown>[]>([]);
  useEffect(() => {
    getJson<{ traces: Record<string, unknown>[] }>("/api/researcher/traces").then((d) => setTraces(d.traces || []));
  }, []);
  return (
    <main style={{ maxWidth: 980, margin: "0 auto", padding: 24 }}>
      <h1>Trace Explorer</h1>
      <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(traces, null, 2)}</pre>
    </main>
  );
}

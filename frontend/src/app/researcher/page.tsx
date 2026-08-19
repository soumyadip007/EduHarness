"use client";

import { useEffect, useState } from "react";
import ExperimentForm from "@/components/experiment/ExperimentForm";
import ProgressTracker from "@/components/experiment/ProgressTracker";
import { getJson, postJson } from "@/lib/api";

type Status = { state: string; last_run_at?: string };

export default function ResearcherPage() {
  const [status, setStatus] = useState<Status>({ state: "idle" });

  const refresh = async () => {
    const s = await getJson<Status>("/api/researcher/experiments/status");
    setStatus(s);
  };

  useEffect(() => {
    void refresh();
  }, []);

  return (
    <main style={{ maxWidth: 980, margin: "0 auto", padding: 24 }}>
      <h1>Researcher Console</h1>
      <div style={{ display: "grid", gap: 12 }}>
        <ExperimentForm
          onRun={async (name, seed) => {
            await postJson("/api/researcher/experiments/run", { name, seed });
            await refresh();
          }}
        />
        <ProgressTracker state={status.state} lastRunAt={status.last_run_at} />
      </div>
    </main>
  );
}

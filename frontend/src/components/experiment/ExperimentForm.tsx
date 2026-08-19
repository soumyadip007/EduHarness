"use client";

import { useState } from "react";

export default function ExperimentForm({ onRun }: { onRun: (name: string, seed: number) => Promise<void> }) {
  const [name, setName] = useState("phase6_full");
  const [seed, setSeed] = useState(42);
  const [busy, setBusy] = useState(false);

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <h3 style={{ marginTop: 0 }}>Run Experiment</h3>
      <label style={{ display: "block", marginBottom: 8 }}>
        Name
        <input value={name} onChange={(e) => setName(e.target.value)} style={{ marginLeft: 8 }} />
      </label>
      <label style={{ display: "block", marginBottom: 8 }}>
        Seed
        <input
          type="number"
          value={seed}
          onChange={(e) => setSeed(Number(e.target.value))}
          style={{ marginLeft: 8, width: 100 }}
        />
      </label>
      <button
        onClick={async () => {
          setBusy(true);
          await onRun(name, seed);
          setBusy(false);
        }}
        disabled={busy}
      >
        {busy ? "Running..." : "Run Phase 6"}
      </button>
    </div>
  );
}

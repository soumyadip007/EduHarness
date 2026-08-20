"use client";

import { useEffect, useState } from "react";

type ModelOption = { key: string; label?: string; open_source?: boolean };

export default function ExperimentForm({
  onRun,
  models,
}: {
  onRun: (payload: { name: string; seed: number; model_keys: string[]; harness_levels: string[] }) => Promise<void>;
  models: ModelOption[];
}) {
  const [name, setName] = useState("phase6_full");
  const [seed, setSeed] = useState(42);
  const [selectedModels, setSelectedModels] = useState<string[]>([]);
  const [harnessLevels, setHarnessLevels] = useState<string[]>(["H0", "H1", "H2", "H3"]);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (models.length && selectedModels.length === 0) {
      setSelectedModels([models[0].key]);
    }
  }, [models, selectedModels.length]);

  const toggleModel = (key: string) => {
    setSelectedModels((prev) => (prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]));
  };

  const toggleHarness = (level: string) => {
    setHarnessLevels((prev) => (prev.includes(level) ? prev.filter((h) => h !== level) : [...prev, level]));
  };

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <h3 style={{ marginTop: 0 }}>Run Experiment</h3>
      <label style={{ display: "block", marginBottom: 8 }}>
        Name
        <input value={name} onChange={(e) => setName(e.target.value)} style={{ marginLeft: 8 }} />
      </label>
      <label style={{ display: "block", marginBottom: 8 }}>
        Seed
        <input type="number" value={seed} onChange={(e) => setSeed(Number(e.target.value))} style={{ marginLeft: 8, width: 100 }} />
      </label>

      <div style={{ marginBottom: 8 }}>
        <strong>Models</strong>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 4 }}>
          {models.map((m) => (
            <label key={m.key}>
              <input type="checkbox" checked={selectedModels.includes(m.key)} onChange={() => toggleModel(m.key)} />{" "}
              {m.label || m.key}
            </label>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: 12 }}>
        <strong>Harness levels</strong>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 4 }}>
          {["H0", "H1", "H2", "H3", "H0+M", "H0+G"].map((level) => (
            <label key={level}>
              <input type="checkbox" checked={harnessLevels.includes(level)} onChange={() => toggleHarness(level)} /> {level}
            </label>
          ))}
        </div>
      </div>

      <button
        onClick={async () => {
          setBusy(true);
          await onRun({
            name,
            seed,
            model_keys: selectedModels.length ? selectedModels : [models[0]?.key || "mid_primary"],
            harness_levels: harnessLevels.length ? harnessLevels : ["H0", "H3"],
          });
          setBusy(false);
        }}
        disabled={busy}
      >
        {busy ? "Running..." : "Run Phase 6 Matrix"}
      </button>
    </div>
  );
}

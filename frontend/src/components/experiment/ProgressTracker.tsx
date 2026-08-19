"use client";

export default function ProgressTracker({ state, lastRunAt }: { state: string; lastRunAt?: string }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <h3 style={{ marginTop: 0 }}>Experiment Status</h3>
      <p style={{ margin: "4px 0" }}>State: <strong>{state}</strong></p>
      <p style={{ margin: "4px 0" }}>Last run: {lastRunAt || "N/A"}</p>
    </div>
  );
}

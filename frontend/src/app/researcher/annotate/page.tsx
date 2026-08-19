"use client";

import { useState } from "react";

export default function ResearcherAnnotatePage() {
  const [label, setLabel] = useState("safe_helpful");
  const [note, setNote] = useState("");
  return (
    <main style={{ maxWidth: 980, margin: "0 auto", padding: 24 }}>
      <h1>Trace Annotation Tool</h1>
      <p>Prototype interface for human annotation workflow.</p>
      <label>
        Label
        <select value={label} onChange={(e) => setLabel(e.target.value)} style={{ marginLeft: 8 }}>
          <option value="safe_helpful">Safe + Helpful</option>
          <option value="safe_unhelpful">Safe + Unhelpful</option>
          <option value="unsafe">Unsafe</option>
        </select>
      </label>
      <div style={{ marginTop: 10 }}>
        <textarea
          rows={8}
          style={{ width: "100%" }}
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Rationale..."
        />
      </div>
      <button style={{ marginTop: 8 }}>Save annotation (local prototype)</button>
    </main>
  );
}

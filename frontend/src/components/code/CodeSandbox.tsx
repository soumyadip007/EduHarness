"use client";

import { useState } from "react";
import { postJson } from "@/lib/api";
import OutputPanel from "./OutputPanel";

type RunResponse = { stdout: string; stderr: string; return_code: number };

export default function CodeSandbox() {
  const [code, setCode] = useState("print('hello from EduHarness')");
  const [result, setResult] = useState<RunResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    try {
      const out = await postJson<RunResponse>("/api/student/run-code", { code });
      setResult(out);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 12, marginTop: 12 }}>
      <h3 style={{ marginTop: 0 }}>Code Sandbox</h3>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={8}
        style={{ width: "100%", fontFamily: "monospace", fontSize: 14 }}
      />
      <div style={{ marginTop: 8 }}>
        <button onClick={run} disabled={loading} style={{ marginRight: 8 }}>
          {loading ? "Running..." : "Run Code"}
        </button>
      </div>
      <OutputPanel result={result} />
    </div>
  );
}

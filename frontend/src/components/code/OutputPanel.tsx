"use client";

type RunResponse = { stdout: string; stderr: string; return_code: number } | null;

export default function OutputPanel({ result }: { result: RunResponse }) {
  if (!result) return null;
  return (
    <div style={{ marginTop: 10, background: "#f9fafb", borderRadius: 8, padding: 10 }}>
      <div><strong>Return code:</strong> {result.return_code}</div>
      <div style={{ marginTop: 6 }}><strong>stdout:</strong></div>
      <pre style={{ whiteSpace: "pre-wrap" }}>{result.stdout || "(empty)"}</pre>
      <div><strong>stderr:</strong></div>
      <pre style={{ whiteSpace: "pre-wrap", color: "#991b1b" }}>{result.stderr || "(empty)"}</pre>
    </div>
  );
}

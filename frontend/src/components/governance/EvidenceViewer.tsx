"use client";

export default function EvidenceViewer({ payload }: { payload: Record<string, unknown> }) {
  return (
    <pre style={{ background: "#f9fafb", border: "1px solid #ddd", borderRadius: 8, padding: 12, whiteSpace: "pre-wrap" }}>
      {JSON.stringify(payload, null, 2)}
    </pre>
  );
}

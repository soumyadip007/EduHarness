"use client";

import { useEffect, useState } from "react";
import { getJson, postJson } from "@/lib/api";
import ActionButtons from "@/components/governance/ActionButtons";
import EvidenceViewer from "@/components/governance/EvidenceViewer";

export default function TeacherQueueDetail({ params }: { params: { id: string } }) {
  const [payload, setPayload] = useState<Record<string, unknown>>({});
  const [status, setStatus] = useState("");

  useEffect(() => {
    getJson<Record<string, unknown>>(`/api/teacher/queue/${params.id}`).then(setPayload);
  }, [params.id]);

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Evidence: {params.id}</h1>
      <EvidenceViewer payload={payload} />
      <div style={{ marginTop: 10 }}>
        <ActionButtons
          onAction={async (action) => {
            const r = await postJson<Record<string, unknown>>(`/api/teacher/queue/${params.id}/action`, { action });
            setStatus(JSON.stringify(r));
          }}
        />
      </div>
      {status ? <pre>{status}</pre> : null}
    </main>
  );
}

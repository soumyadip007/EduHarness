"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";

export default function StudentDetailPage({ params }: { params: { id: string } }) {
  const [payload, setPayload] = useState<Record<string, unknown>>({});
  useEffect(() => {
    getJson<Record<string, unknown>>(`/api/teacher/students/${params.id}`).then(setPayload);
  }, [params.id]);

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Student Detail: {params.id}</h1>
      <pre>{JSON.stringify(payload, null, 2)}</pre>
    </main>
  );
}

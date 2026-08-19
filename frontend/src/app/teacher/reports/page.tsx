"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";

export default function TeacherReportsPage() {
  const [summary, setSummary] = useState<Record<string, unknown>>({});
  useEffect(() => {
    getJson<Record<string, unknown>>("/api/teacher/reports/summary").then(setSummary);
  }, []);

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Teacher Reports</h1>
      <pre>{JSON.stringify(summary, null, 2)}</pre>
    </main>
  );
}

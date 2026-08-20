"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getJson } from "@/lib/api";
import MasteryHeatmap from "@/components/mastery/MasteryHeatmap";

type Student = { id: string; risk: string; sessions: number; mastery_avg?: number };
type HeatmapRow = { studentId: string; mastery: Record<string, number> };

export default function TeacherStudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [heatmapRows, setHeatmapRows] = useState<HeatmapRow[]>([]);

  useEffect(() => {
    getJson<{ students: Student[] }>("/api/teacher/students").then((d) => setStudents(d.students || []));
    getJson<{ rows: HeatmapRow[] }>("/api/teacher/students/mastery-heatmap")
      .then((d) => setHeatmapRows(d.rows || []))
      .catch(() => setHeatmapRows([]));
  }, []);

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Class Overview</h1>
      <ul>
        {students.map((s) => (
          <li key={s.id}>
            <Link href={`/teacher/students/${s.id}`}>{s.id}</Link> — risk: {s.risk}, sessions: {s.sessions}
            {typeof s.mastery_avg === "number" ? `, avg mastery: ${Math.round(s.mastery_avg * 100)}%` : ""}
          </li>
        ))}
      </ul>
      {students.length === 0 ? <p>No students yet. Students appear after tutoring sessions.</p> : null}
      <MasteryHeatmap rows={heatmapRows} />
    </main>
  );
}

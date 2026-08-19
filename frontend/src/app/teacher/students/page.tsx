"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";
import MasteryHeatmap from "@/components/mastery/MasteryHeatmap";

type Student = { id: string; risk: string; sessions: number };

export default function TeacherStudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  useEffect(() => {
    getJson<{ students: Student[] }>("/api/teacher/students").then((d) => setStudents(d.students || []));
  }, []);

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Class Overview</h1>
      <ul>
        {students.map((s) => (
          <li key={s.id}>{s.id} — risk: {s.risk}, sessions: {s.sessions}</li>
        ))}
      </ul>
      <MasteryHeatmap
        rows={[
          { studentId: "student-demo-session", mastery: { variables: 0.72, loops: 0.52, functions: 0.41 } },
          { studentId: "s1", mastery: { variables: 0.81, loops: 0.76, functions: 0.66 } },
        ]}
      />
    </main>
  );
}

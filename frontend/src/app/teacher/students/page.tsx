"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";

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
    </main>
  );
}

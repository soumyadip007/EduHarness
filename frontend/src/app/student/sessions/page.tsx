"use client";

import { useEffect, useState } from "react";
import { getJson } from "@/lib/api";

type SessionItem = { session_id: string; turns: number };

export default function StudentSessionsPage() {
  const [sessions, setSessions] = useState<SessionItem[]>([]);

  useEffect(() => {
    getJson<{ sessions: SessionItem[] }>("/api/student/sessions")
      .then((d) => setSessions(d.sessions))
      .catch(() => setSessions([]));
  }, []);

  return (
    <main style={{ maxWidth: 700, margin: "0 auto", padding: 24 }}>
      <h1>Session History</h1>
      {sessions.length === 0 ? <p>No sessions available.</p> : null}
      <ul>
        {sessions.map((s) => (
          <li key={s.session_id}>
            <strong>{s.session_id}</strong> — {s.turns} turns
          </li>
        ))}
      </ul>
    </main>
  );
}

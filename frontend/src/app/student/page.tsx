"use client";

import { useMemo } from "react";
import ChatInput from "@/components/chat/ChatInput";
import ChatPanel from "@/components/chat/ChatPanel";
import CodeSandbox from "@/components/code/CodeSandbox";
import { useChat } from "@/hooks/useChat";
import { useMastery } from "@/hooks/useMastery";

export default function StudentPage() {
  const sessionId = useMemo(() => "student-demo-session", []);
  const { messages, send, loading, mode, setMode } = useChat("H2");
  const { mastery } = useMastery();

  return (
    <main style={{ maxWidth: 1080, margin: "0 auto", padding: 24 }}>
      <h1>EduHarness Student Tutor</h1>
      <p>Chat with the tutoring agent via backend API.</p>

      <div style={{ marginBottom: 12, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <label>
          Mode: 
          <select value={mode} onChange={(e) => setMode(e.target.value)} style={{ marginLeft: 8 }}>
            <option value="H0">H0</option>
            <option value="H1">H1</option>
            <option value="H2">H2</option>
            <option value="H3">H3</option>
            <option value="H0+M">H0+M</option>
            <option value="H0+G">H0+G</option>
          </select>
        </label>
        <div style={{ color: "#555" }}>Session: {sessionId}</div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 16 }}>
        <div>
          <ChatPanel messages={messages} />
          <div style={{ marginTop: 12 }}>
            <ChatInput onSend={(text) => send(sessionId, text)} disabled={loading} />
          </div>
          {loading ? <p style={{ color: "#666" }}>Tutor is thinking...</p> : null}
          <CodeSandbox />
        </div>
        <aside style={{ border: "1px solid #ddd", borderRadius: 10, padding: 12, height: "fit-content" }}>
          <h3 style={{ marginTop: 0 }}>Session Info</h3>
          <p style={{ margin: 0, color: "#555" }}>Assessment mode controls scaffolding strictness.</p>
          <h4 style={{ marginBottom: 8 }}>Mastery Snapshot</h4>
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {Object.entries(mastery).map(([k, v]) => (
              <li key={k}>
                {k}: {Math.round(v * 100)}%
              </li>
            ))}
          </ul>
          <div style={{ marginTop: 10 }}>
            <a href=\"/student/progress\">Open full progress page</a>
          </div>
        </aside>
      </div>
    </main>
  );
}

"use client";

import { useMemo } from "react";
import ChatInput from "@/components/chat/ChatInput";
import ChatPanel from "@/components/chat/ChatPanel";
import { useChat } from "@/hooks/useChat";

export default function StudentPage() {
  const sessionId = useMemo(() => "student-demo-session", []);
  const { messages, send, loading, mode, setMode } = useChat("H2");

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>EduHarness Student Tutor</h1>
      <p>Chat with the tutoring agent via backend API.</p>

      <div style={{ marginBottom: 12 }}>
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
      </div>

      <ChatPanel messages={messages} />
      <div style={{ marginTop: 12 }}>
        <ChatInput onSend={(text) => send(sessionId, text)} disabled={loading} />
      </div>
      {loading ? <p style={{ color: "#666" }}>Tutor is thinking...</p> : null}
    </main>
  );
}

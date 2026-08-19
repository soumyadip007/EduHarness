"use client";

import MessageBubble from "./MessageBubble";

type Message = { role: "student" | "tutor"; text: string; scaffoldLevel?: string };

export default function ChatPanel({ messages }: { messages: Message[] }) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: 10,
        padding: 12,
        minHeight: 320,
        display: "flex",
        flexDirection: "column",
        background: "#fff",
      }}
    >
      {messages.length === 0 ? <div style={{ color: "#666" }}>No messages yet.</div> : null}
      {messages.map((m, idx) => (
        <MessageBubble key={idx} role={m.role} text={m.text} scaffoldLevel={m.scaffoldLevel} />
      ))}
    </div>
  );
}

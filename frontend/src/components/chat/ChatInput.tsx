"use client";

import { useState } from "react";

type Props = {
  onSend: (text: string) => void;
  disabled?: boolean;
};

export default function ChatInput({ onSend, disabled = false }: Props) {
  const [text, setText] = useState("");

  return (
    <div style={{ display: "flex", gap: 8 }}>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Ask your question..."
        style={{ flex: 1, padding: 10, border: "1px solid #ccc", borderRadius: 8 }}
      />
      <button
        disabled={disabled}
        onClick={() => {
          onSend(text);
          setText("");
        }}
        style={{ padding: "10px 14px" }}
      >
        Send
      </button>
    </div>
  );
}

"use client";

import { useState } from "react";
import { postJson } from "@/lib/api";

type Message = { role: "student" | "tutor"; text: string; scaffoldLevel?: string };

type MessageResp = {
  response: string;
  mode: string;
  scaffold_level?: string;
  model_key?: string;
  teacher_reply?: boolean;
};

export function useChat(initialMode: string = "H0", modelKey: string = "mid_primary") {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [turn, setTurn] = useState(1);
  const [mode, setMode] = useState(initialMode);

  const send = async (sessionId: string, text: string) => {
    if (!text.trim()) return;
    setMessages((prev) => [...prev, { role: "student", text }]);
    setLoading(true);
    try {
      const data = await postJson<MessageResp>("/api/student/message", {
        session_id: sessionId,
        turn_number: turn,
        message: text,
        mode,
        model_key: modelKey,
      });
      setMessages((prev) => [
        ...prev,
        {
          role: "tutor",
          text: data.teacher_reply ? `[Teacher reply] ${data.response}` : data.response,
          scaffoldLevel: data.scaffold_level ?? "none",
        },
      ]);
      setTurn((t) => t + 1);
    } finally {
      setLoading(false);
    }
  };

  return { messages, send, loading, mode, setMode };
}

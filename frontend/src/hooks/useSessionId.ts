"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "eduharness_session_id";

function createSessionId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return `student-${crypto.randomUUID().slice(0, 8)}`;
  }
  return `student-${Date.now()}`;
}

export function useSessionId() {
  const [sessionId, setSessionId] = useState("");

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored) {
      setSessionId(stored);
      return;
    }
    const created = createSessionId();
    window.localStorage.setItem(STORAGE_KEY, created);
    setSessionId(created);
  }, []);

  const resetSession = () => {
    const created = createSessionId();
    window.localStorage.setItem(STORAGE_KEY, created);
    setSessionId(created);
  };

  return { sessionId, resetSession };
}

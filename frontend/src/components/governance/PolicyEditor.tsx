"use client";

import { useState } from "react";

export default function PolicyEditor({ value, onSave }: { value: string; onSave: (v: string) => void }) {
  const [text, setText] = useState(value);
  return (
    <div>
      <textarea value={text} onChange={(e) => setText(e.target.value)} rows={16} style={{ width: "100%", fontFamily: "monospace" }} />
      <button onClick={() => onSave(text)} style={{ marginTop: 8 }}>Save Contract</button>
    </div>
  );
}

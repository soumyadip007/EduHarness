"use client";

import { useEffect, useState } from "react";
import PolicyEditor from "@/components/governance/PolicyEditor";
import { getJson } from "@/lib/api";

export default function TeacherPolicyPage() {
  const [yamlText, setYamlText] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    getJson<{ yaml_text: string }>("/api/teacher/contract").then((d) => setYamlText(d.yaml_text || ""));
  }, []);

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>Policy Editor</h1>
      <PolicyEditor
        value={yamlText}
        onSave={async (text) => {
          const r = await fetch("http://localhost:8000/api/teacher/contract", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ yaml_text: text }),
          });
          const data = await r.json();
          setStatus(JSON.stringify(data));
          setYamlText(text);
        }}
      />
      {status ? <pre>{status}</pre> : null}
    </main>
  );
}

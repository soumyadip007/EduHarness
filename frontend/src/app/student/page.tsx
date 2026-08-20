"use client";

import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Link,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";
import ChatInput from "@/components/chat/ChatInput";
import ChatPanel from "@/components/chat/ChatPanel";
import CodeSandbox from "@/components/code/CodeSandbox";
import { useChat } from "@/hooks/useChat";
import { useMastery } from "@/hooks/useMastery";
import { useSessionId } from "@/hooks/useSessionId";
import { getJson } from "@/lib/api";

type ModelOption = {
  key: string;
  label: string;
  provider: string;
  model_id: string;
  open_source: boolean;
};

type Question = {
  id: string;
  prompt: string;
  concept: string;
  selection_reason?: string;
  student_mastery?: number;
};

export default function StudentPage() {
  const { sessionId, resetSession } = useSessionId();
  const [models, setModels] = useState<ModelOption[]>([]);
  const [modelKey, setModelKey] = useState("mid_primary");
  const [questions, setQuestions] = useState<Question[]>([]);
  const { messages, send, loading, mode, setMode } = useChat("H2", modelKey);
  const { mastery, refresh } = useMastery(sessionId);

  useEffect(() => {
    getJson<{ models: ModelOption[]; active_model_key: string }>("/api/config/models").then((data) => {
      setModels(data.models || []);
      if (data.active_model_key) setModelKey(data.active_model_key);
    });
  }, []);

  useEffect(() => {
    if (!sessionId) return;
    getJson<{ questions: Question[] }>(`/api/student/questions?session_id=${encodeURIComponent(sessionId)}&count=3`)
      .then((d) => setQuestions(d.questions || []))
      .catch(() => setQuestions([]));
  }, [sessionId, mastery]);

  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Student Tutor Workspace</Typography>
      <Typography color="text.secondary">Chat with the agent, run code, and track concept mastery in one place.</Typography>

      <Box sx={{ display: "grid", gap: 2, gridTemplateColumns: { xs: "1fr", lg: "2fr 1fr" } }}>
        <Box>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", mb: 2 }}>
            <CardContent>
              <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2, gap: 2, flexWrap: "wrap" }}>
                <FormControl size="small" sx={{ minWidth: 180 }}>
                  <InputLabel id="mode-select-label">Harness Mode</InputLabel>
                  <Select labelId="mode-select-label" value={mode} label="Harness Mode" onChange={(e) => setMode(e.target.value)}>
                    <MenuItem value="H0">H0</MenuItem>
                    <MenuItem value="H1">H1</MenuItem>
                    <MenuItem value="H2">H2</MenuItem>
                    <MenuItem value="H3">H3</MenuItem>
                    <MenuItem value="H0+M">H0+M</MenuItem>
                    <MenuItem value="H0+G">H0+G</MenuItem>
                  </Select>
                </FormControl>
                <FormControl size="small" sx={{ minWidth: 220 }}>
                  <InputLabel id="model-select-label">Tutor Model</InputLabel>
                  <Select labelId="model-select-label" value={modelKey} label="Tutor Model" onChange={(e) => setModelKey(e.target.value)}>
                    {models.map((m) => (
                      <MenuItem key={m.key} value={m.key}>
                        {m.label || m.key} {m.open_source ? "(OSS)" : ""}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Session: {sessionId || "…"}
                  </Typography>
                  <Button size="small" onClick={resetSession}>
                    New session
                  </Button>
                </Box>
              </Box>

              <ChatPanel messages={messages} />
              <Box sx={{ mt: 2 }}>
                <ChatInput
                  onSend={async (text) => {
                    if (!sessionId) return;
                    await send(sessionId, text);
                    await refresh();
                  }}
                  disabled={loading || !sessionId}
                />
              </Box>
              {loading ? <Typography sx={{ mt: 1, color: "text.secondary" }}>Tutor is thinking...</Typography> : null}
            </CardContent>
          </Card>

          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Code Sandbox
              </Typography>
              <CodeSandbox />
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ display: "grid", gap: 2 }}>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
            <CardContent>
              <Typography variant="h6">Assigned Questions</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                Selected from exercise banks based on your mastery profile.
              </Typography>
              {questions.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No questions yet — start a tutoring session first.
                </Typography>
              ) : (
                <Box component="ul" sx={{ m: 0, pl: 2 }}>
                  {questions.map((q) => (
                    <li key={q.id}>
                      <strong>{q.concept}</strong>: {q.prompt}
                      {typeof q.student_mastery === "number" ? ` (${Math.round(q.student_mastery * 100)}% mastery)` : ""}
                    </li>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>

          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
            <CardContent>
              <Typography variant="h6">Session Intelligence</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                Active model: {modelKey}
              </Typography>
              <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
                Mastery Snapshot
              </Typography>
              <Box component="ul" sx={{ m: 0, pl: 2 }}>
                {Object.entries(mastery as Record<string, number>).map(([k, v]) => (
                  <li key={k}>
                    {k}: {Math.round(v * 100)}%
                  </li>
                ))}
              </Box>
              <Link href="/student/progress" sx={{ display: "inline-block", mt: 1.5 }}>
                Open full progress page
              </Link>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
}

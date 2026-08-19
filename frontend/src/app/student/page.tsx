"use client";

import { useMemo } from "react";
import { Box, Card, CardContent, FormControl, InputLabel, Link, MenuItem, Select, Typography } from "@mui/material";
import ChatInput from "@/components/chat/ChatInput";
import ChatPanel from "@/components/chat/ChatPanel";
import CodeSandbox from "@/components/code/CodeSandbox";
import { useChat } from "@/hooks/useChat";
import { useMastery } from "@/hooks/useMastery";

export default function StudentPage() {
  const sessionId = useMemo(() => "student-demo-session", []);
  const { messages, send, loading, mode, setMode } = useChat("H2");
  const { mastery, refresh } = useMastery();

  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Student Tutor Workspace</Typography>
      <Typography color="text.secondary">Chat with the agent, run code, and track concept mastery in one place.</Typography>

      <Box sx={{ display: "grid", gap: 2, gridTemplateColumns: { xs: "1fr", lg: "2fr 1fr" } }}>
        <Box>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", mb: 2 }}>
            <CardContent>
              <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
                <FormControl size="small" sx={{ minWidth: 180 }}>
                  <InputLabel id="mode-select-label">Harness Mode</InputLabel>
                  <Select
                    labelId="mode-select-label"
                    value={mode}
                    label="Harness Mode"
                    onChange={(e) => setMode(e.target.value)}
                  >
                    <MenuItem value="H0">H0</MenuItem>
                    <MenuItem value="H1">H1</MenuItem>
                    <MenuItem value="H2">H2</MenuItem>
                    <MenuItem value="H3">H3</MenuItem>
                    <MenuItem value="H0+M">H0+M</MenuItem>
                    <MenuItem value="H0+G">H0+G</MenuItem>
                  </Select>
                </FormControl>
                <Typography variant="body2" color="text.secondary">
                  Session: {sessionId}
                </Typography>
              </Box>

              <ChatPanel messages={messages} />
              <Box sx={{ mt: 2 }}>
                <ChatInput
                  onSend={async (text) => {
                    await send(sessionId, text);
                    await refresh(sessionId);
                  }}
                  disabled={loading}
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

        <Box>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
            <CardContent>
              <Typography variant="h6">Session Intelligence</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                Assessment mode controls scaffolding strictness.
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

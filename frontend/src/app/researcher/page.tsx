"use client";

import { useEffect, useState } from "react";
import { Box, Card, CardContent, Typography } from "@mui/material";
import ExperimentForm from "@/components/experiment/ExperimentForm";
import ProgressTracker from "@/components/experiment/ProgressTracker";
import { getJson, postJson } from "@/lib/api";

type Status = { state: string; last_run_at?: string };

export default function ResearcherPage() {
  const [status, setStatus] = useState<Status>({ state: "idle" });

  const refresh = async () => {
    const s = await getJson<Status>("/api/researcher/experiments/status");
    setStatus(s);
  };

  useEffect(() => {
    void refresh();
  }, []);

  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Researcher Experiment Dashboard</Typography>
      <Typography color="text.secondary">Launch experiment runs, monitor status, and access generated reports.</Typography>
      <Box sx={{ display: "grid", gap: 2, gridTemplateColumns: { xs: "1fr", md: "7fr 5fr" } }}>
        <Box>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
            <CardContent>
              <ExperimentForm
                onRun={async (name, seed) => {
                  await postJson("/api/researcher/experiments/run", { name, seed });
                  await refresh();
                }}
              />
            </CardContent>
          </Card>
        </Box>
        <Box>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
            <CardContent>
              <ProgressTracker state={status.state} lastRunAt={status.last_run_at} />
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
}

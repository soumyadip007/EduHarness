"use client";

import { useEffect, useState } from "react";
import { Box, Card, CardContent, FormControl, InputLabel, MenuItem, Select, Typography } from "@mui/material";
import ExperimentForm from "@/components/experiment/ExperimentForm";
import ProgressTracker from "@/components/experiment/ProgressTracker";
import { getJson, postJson, putJson } from "@/lib/api";

type Status = {
  state: string;
  last_run_at?: string;
  active_model_key?: string;
  available_models?: { key: string; label?: string; open_source?: boolean }[];
};

export default function ResearcherPage() {
  const [status, setStatus] = useState<Status>({ state: "idle" });
  const [activeModel, setActiveModel] = useState("mid_primary");
  const [models, setModels] = useState<{ key: string; label?: string; open_source?: boolean }[]>([]);

  const refresh = async () => {
    const s = await getJson<Status>("/api/researcher/experiments/status");
    setStatus(s);
    if (s.active_model_key) setActiveModel(s.active_model_key);
    if (s.available_models?.length) setModels(s.available_models);
    else {
      const cfg = await getJson<{ models: { key: string; label?: string; open_source?: boolean }[] }>("/api/config/models");
      setModels(cfg.models || []);
    }
  };

  useEffect(() => {
    void refresh();
  }, []);

  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Researcher Experiment Dashboard</Typography>
      <Typography color="text.secondary">Launch manifest-driven experiment runs and configure the global active model.</Typography>

      <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Global Active Model
          </Typography>
          <Box sx={{ display: "flex", gap: 2, alignItems: "center", flexWrap: "wrap" }}>
            <FormControl size="small" sx={{ minWidth: 260 }}>
              <InputLabel id="global-model-label">Active model</InputLabel>
              <Select
                labelId="global-model-label"
                value={activeModel}
                label="Active model"
                onChange={(e) => setActiveModel(e.target.value)}
              >
                {models.map((m) => (
                  <MenuItem key={m.key} value={m.key}>
                    {m.label || m.key} {m.open_source ? "(OSS)" : ""}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <button
              type="button"
              onClick={async () => {
                await putJson("/api/config/models/active", { model_key: activeModel });
                await refresh();
              }}
            >
              Save global model
            </button>
          </Box>
        </CardContent>
      </Card>

      <Box sx={{ display: "grid", gap: 2, gridTemplateColumns: { xs: "1fr", md: "7fr 5fr" } }}>
        <Box>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
            <CardContent>
              <ExperimentForm
                models={models}
                onRun={async (payload) => {
                  await postJson("/api/researcher/experiments/run", payload);
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

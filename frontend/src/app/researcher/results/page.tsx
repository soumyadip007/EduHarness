"use client";

import { useEffect, useState } from "react";
import { Box, Card, CardContent, Typography } from "@mui/material";
import AblationBar from "@/components/charts/AblationBar";
import LearningCurve from "@/components/charts/LearningCurve";
import ResultsTable from "@/components/experiment/ResultsTable";
import { getJson } from "@/lib/api";

type Row = {
  condition: string;
  safety_adversarial: number;
  delta_solve_rate: number;
  state_divergence: number;
};

export default function ResearcherResultsPage() {
  const [rows, setRows] = useState<Row[]>([]);
  const [latest, setLatest] = useState<{ tti_h0: number; tti_h1: number; tti_h2: number; tti_h3: number } | null>(null);

  useEffect(() => {
    getJson<{ rows: Row[] }>("/api/researcher/results/table").then((d) => setRows(d.rows || []));
    getJson<{ tti_h0: number; tti_h1: number; tti_h2: number; tti_h3: number }>("/api/researcher/results/latest").then(setLatest);
  }, []);

  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Research Results Dashboard</Typography>
      <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
        <CardContent>
          <ResultsTable rows={rows} />
        </CardContent>
      </Card>
      <Box sx={{ display: "grid", gap: 2, gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" } }}>
        <Box>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", height: "100%" }}>
            <CardContent>
              {latest ? (
                <AblationBar
                  points={[
                    { label: "H0", value: latest.tti_h0 },
                    { label: "H1", value: latest.tti_h1 },
                    { label: "H2", value: latest.tti_h2 },
                    { label: "H3", value: latest.tti_h3 },
                  ]}
                />
              ) : null}
            </CardContent>
          </Card>
        </Box>
        <Box>
          <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", height: "100%" }}>
            <CardContent>
              <LearningCurve values={[0.3, 0.36, 0.43, 0.49, 0.53, 0.55, 0.56]} />
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
}

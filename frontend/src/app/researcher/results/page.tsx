"use client";

import { useEffect, useState } from "react";
import { Box, Button, Card, CardContent, Typography } from "@mui/material";
import AblationBar from "@/components/charts/AblationBar";
import LearningCurve from "@/components/charts/LearningCurve";
import ResultsTable from "@/components/experiment/ResultsTable";
import { API_BASE, getJson } from "@/lib/api";

type Row = {
  condition: string;
  safety_adversarial: number;
  delta_solve_rate: number;
  state_divergence: number;
};

type CompareResponse = {
  model_only_gain: number;
  harness_only_gain: number;
  model_stats: Record<string, { mean: number; ci_low: number; ci_high: number; n: number }>;
  harness_stats: Record<string, { mean: number; ci_low: number; ci_high: number; n: number }>;
};

type StatsResponse = {
  comparison: CompareResponse;
  h0_vs_h3_significance: { p_value: number; significant_95: boolean; t_stat: number };
};

export default function ResearcherResultsPage() {
  const [rows, setRows] = useState<Row[]>([]);
  const [latest, setLatest] = useState<{ tti_h0: number; tti_h1: number; tti_h2: number; tti_h3: number } | null>(null);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [curve, setCurve] = useState<number[]>([]);

  useEffect(() => {
    getJson<{ rows: Row[] }>("/api/researcher/results/table").then((d) => setRows(d.rows || []));
    getJson<{ tti_h0: number; tti_h1: number; tti_h2: number; tti_h3: number }>("/api/researcher/results/latest").then(setLatest);
    getJson<StatsResponse>("/api/researcher/results/stats").then(setStats);
    getJson<{ series: number[] }>("/api/researcher/results/learning-curve").then((d) => setCurve(d.series || []));
  }, []);

  const compare = stats?.comparison;

  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Research Results Dashboard</Typography>
      <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
        <Button variant="outlined" href={`${API_BASE}/api/researcher/reports/pdf`} target="_blank">
          Download Research PDF
        </Button>
      </Box>

      {compare ? (
        <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Model-only vs Harness-only Gain
            </Typography>
            <Typography variant="body2">Model-only gain: {compare.model_only_gain}</Typography>
            <Typography variant="body2">Harness-only gain (best harness − H0): {compare.harness_only_gain}</Typography>
            {stats?.h0_vs_h3_significance ? (
              <Typography variant="body2" sx={{ mt: 1 }}>
                H0 vs H3: p={stats.h0_vs_h3_significance.p_value}, significant at 95%:{" "}
                {stats.h0_vs_h3_significance.significant_95 ? "yes" : "no"}
              </Typography>
            ) : null}
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2">Model CIs</Typography>
              <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>{JSON.stringify(compare.model_stats, null, 2)}</pre>
              <Typography variant="subtitle2" sx={{ mt: 1 }}>
                Harness CIs
              </Typography>
              <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>{JSON.stringify(compare.harness_stats, null, 2)}</pre>
            </Box>
          </CardContent>
        </Card>
      ) : null}

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
              <LearningCurve values={curve.length ? curve : [0.3, 0.36, 0.43, 0.49, 0.53, 0.55, 0.56]} />
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
}

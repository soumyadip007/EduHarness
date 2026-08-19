"use client";

import { useEffect, useState } from "react";
import InteractionPlot from "@/components/charts/InteractionPlot";
import { getJson } from "@/lib/api";
import { Box, Card, CardContent, Typography } from "@mui/material";

export default function ResearcherTracesPage() {
  const [traces, setTraces] = useState<Record<string, unknown>[]>([]);
  useEffect(() => {
    getJson<{ traces: Record<string, unknown>[] }>("/api/researcher/traces").then((d) => setTraces(d.traces || []));
  }, []);
  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Trace Explorer</Typography>
      <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
        <CardContent>
          <InteractionPlot
            cells={[
              { model: "mid", harness: "H0", tti: 0.41 },
              { model: "mid", harness: "H3", tti: 0.69 },
              { model: "frontier", harness: "H3", tti: 0.73 },
            ]}
          />
        </CardContent>
      </Card>
      <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recent Traces
          </Typography>
          <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>{JSON.stringify(traces, null, 2)}</pre>
        </CardContent>
      </Card>
    </Box>
  );
}

"use client";

import { useEffect, useState } from "react";
import { Box, Card, CardContent, Typography } from "@mui/material";
import CostChart from "@/components/charts/CostChart";
import { getJson } from "@/lib/api";

type CostResponse = {
  cost_summary: {
    by_condition?: Record<string, { usd: number }>;
  };
};

export default function ResearcherCostsPage() {
  const [rows, setRows] = useState<{ condition: string; usd: number }[]>([]);
  useEffect(() => {
    getJson<CostResponse>("/api/researcher/costs").then((d) => {
      const byCond = d.cost_summary?.by_condition || {};
      const next = Object.entries(byCond).map(([condition, v]) => ({ condition, usd: v.usd || 0 }));
      setRows(next);
    });
  }, []);

  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Cost Monitor</Typography>
      <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
        <CardContent>
          <CostChart rows={rows.length ? rows : [{ condition: "H0", usd: 0 }]} />
        </CardContent>
      </Card>
    </Box>
  );
}

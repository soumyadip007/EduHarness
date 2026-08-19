"use client";

import { useEffect, useState } from "react";
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
    <main style={{ maxWidth: 980, margin: "0 auto", padding: 24 }}>
      <h1>Cost Monitor</h1>
      <CostChart rows={rows.length ? rows : [{ condition: "H0", usd: 0 }]} />
    </main>
  );
}

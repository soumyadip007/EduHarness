"use client";

import { useEffect, useState } from "react";
import { Box, Button, Card, CardContent, Typography } from "@mui/material";
import { API_BASE, getJson } from "@/lib/api";

export default function TeacherReportsPage() {
  const [summary, setSummary] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/teacher/reports/summary").then(setSummary);
  }, []);

  return (
    <Box sx={{ maxWidth: 900, mx: "auto", p: 3, display: "grid", gap: 2 }}>
      <Typography variant="h4">Teacher Reports</Typography>
      <Typography color="text.secondary">
        KPIs are computed from database-backed escalation and session records. PDF includes active model metadata.
      </Typography>
      <Button variant="contained" href={`${API_BASE}/api/teacher/reports/pdf`} target="_blank">
        Download PDF Report
      </Button>
      <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
        <CardContent>
          <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>{JSON.stringify(summary, null, 2)}</pre>
        </CardContent>
      </Card>
    </Box>
  );
}

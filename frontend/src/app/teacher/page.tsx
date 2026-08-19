"use client";

import AddAlertIcon from "@mui/icons-material/AddAlert";
import { Box, Button, Card, CardContent, Chip, Typography } from "@mui/material";
import EscalationCard from "@/components/governance/EscalationCard";
import { useEscalation } from "@/hooks/useEscalation";
import { postJson } from "@/lib/api";

export default function TeacherPage() {
  const { items, loading } = useEscalation();
  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Teacher Governance Dashboard</Typography>
      <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
        <CardContent>
          <Box sx={{ mb: 2, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <Box sx={{ display: "flex", gap: 1, alignItems: "center" }}>
              <Typography variant="h6">Live Review Queue</Typography>
              <Chip label={`${items.length} open`} color={items.length > 0 ? "warning" : "success"} size="small" />
            </Box>
            <Button
              variant="contained"
              startIcon={<AddAlertIcon />}
              onClick={() => postJson("/api/teacher/queue/simulate", {})}
            >
              Simulate escalation
            </Button>
          </Box>
          {loading ? <Typography color="text.secondary">Loading queue...</Typography> : null}
          {!loading && items.length === 0 ? <Typography color="text.secondary">No pending escalations.</Typography> : null}
          {items.map((i) => (
            <EscalationCard key={i.escalation_id} id={i.escalation_id} priority={i.priority} reason={i.reason} />
          ))}
        </CardContent>
      </Card>
    </Box>
  );
}

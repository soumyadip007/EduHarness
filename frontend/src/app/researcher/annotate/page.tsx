"use client";

import { useState } from "react";
import { Box, Button, Card, CardContent, FormControl, InputLabel, MenuItem, Select, TextField, Typography } from "@mui/material";

export default function ResearcherAnnotatePage() {
  const [label, setLabel] = useState("safe_helpful");
  const [note, setNote] = useState("");
  return (
    <Box sx={{ display: "grid", gap: 2 }}>
      <Typography variant="h4">Trace Annotation Tool</Typography>
      <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider" }}>
        <CardContent>
          <Typography color="text.secondary" sx={{ mb: 2 }}>
            Prototype interface for human annotation workflow.
          </Typography>
          <FormControl size="small" sx={{ minWidth: 260 }}>
            <InputLabel id="annotation-label">Label</InputLabel>
            <Select labelId="annotation-label" value={label} label="Label" onChange={(e) => setLabel(e.target.value)}>
              <MenuItem value="safe_helpful">Safe + Helpful</MenuItem>
              <MenuItem value="safe_unhelpful">Safe + Unhelpful</MenuItem>
              <MenuItem value="unsafe">Unsafe</MenuItem>
            </Select>
          </FormControl>
          <TextField
            multiline
            minRows={8}
            fullWidth
            sx={{ mt: 2 }}
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Rationale..."
          />
          <Button variant="contained" sx={{ mt: 2 }}>
            Save annotation (local prototype)
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
}

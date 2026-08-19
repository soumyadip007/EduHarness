import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import { Box, Button, Card, CardContent, Typography } from "@mui/material";
import Link from "next/link";

export default function HomePage() {
  return (
    <Box sx={{ display: "grid", gap: 3 }}>
      <Typography variant="h4">EduHarness Control Center</Typography>
      <Typography color="text.secondary">
        Unified dashboard for student tutoring, teacher governance, and researcher evaluation workflows.
      </Typography>

      <Box sx={{ display: "grid", gap: 2, gridTemplateColumns: { xs: "1fr", md: "repeat(3, 1fr)" } }}>
        {[
          { title: "Student Tutor", desc: "Live tutoring, scaffolding, and mastery view.", href: "/student" },
          { title: "Teacher Queue", desc: "Escalations, evidence review, and policy edits.", href: "/teacher" },
          { title: "Research Console", desc: "Run experiments and monitor outcomes.", href: "/researcher" },
        ].map((item) => (
          <Box key={item.href}>
            <Card elevation={0} sx={{ border: "1px solid", borderColor: "divider", height: "100%" }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {item.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {item.desc}
                </Typography>
                <Button component={Link} href={item.href} variant="contained" endIcon={<ArrowForwardIcon />}>
                  Open
                </Button>
              </CardContent>
            </Card>
          </Box>
        ))}
      </Box>
    </Box>
  );
}

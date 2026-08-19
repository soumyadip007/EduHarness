"use client";

import AutoGraphIcon from "@mui/icons-material/AutoGraph";
import DashboardIcon from "@mui/icons-material/Dashboard";
import PsychologyIcon from "@mui/icons-material/Psychology";
import SchoolIcon from "@mui/icons-material/School";
import SupervisorAccountIcon from "@mui/icons-material/SupervisorAccount";
import {
  AppBar,
  Box,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from "@mui/material";
import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

const drawerWidth = 240;

const navItems = [
  { label: "Dashboard", href: "/", icon: <DashboardIcon /> },
  { label: "Student", href: "/student", icon: <SchoolIcon /> },
  { label: "Teacher", href: "/teacher", icon: <SupervisorAccountIcon /> },
  { label: "Researcher", href: "/researcher", icon: <PsychologyIcon /> },
  { label: "Results", href: "/researcher/results", icon: <AutoGraphIcon /> },
];

export default function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <AppBar
        position="fixed"
        elevation={0}
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, borderBottom: "1px solid", borderColor: "divider" }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            EduHarness Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: "border-box", borderRight: "1px solid #e2e8f0" },
        }}
      >
        <Toolbar />
        <List sx={{ mt: 1 }}>
          {navItems.map((item) => (
            <ListItemButton key={item.href} component={Link} href={item.href} selected={pathname === item.href}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}

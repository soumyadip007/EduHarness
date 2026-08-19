"use client";

import { CssBaseline, ThemeProvider } from "@mui/material";
import type { ReactNode } from "react";
import { appTheme } from "@/theme/theme";

export default function AppThemeProvider({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider theme={appTheme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}

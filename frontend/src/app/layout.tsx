import type { ReactNode } from "react";
import AppShell from "@/components/layout/AppShell";
import AppThemeProvider from "@/components/layout/AppThemeProvider";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppThemeProvider>
          <AppShell>{children}</AppShell>
        </AppThemeProvider>
      </body>
    </html>
  );
}

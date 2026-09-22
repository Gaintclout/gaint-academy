import type { ReactNode } from "react";
import "./globals.css";

export const metadata = { title: "GAINT Academy", description: "Unified education and campus management" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}

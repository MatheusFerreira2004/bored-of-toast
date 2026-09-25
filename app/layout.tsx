import type { Metadata } from "next";
import "./globals.css";

// Headline/description below mirror the Proposed hero copy in the Landing Page Brief.
// These are proposed, not final/approved copy.
export const metadata: Metadata = {
  title: "Bored of Toast — Recipes worth leaving toast for",
  description:
    "Real recipes, honest cooking tips, and the do's and don'ts nobody tells you.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-brand-cream text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}

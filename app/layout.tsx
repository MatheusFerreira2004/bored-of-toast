import type { Metadata } from "next";
import { Fraunces, Caveat, Inter } from "next/font/google";
import "./globals.css";

// Font choices are Proposed — approximated from the user-supplied design reference
// (serif display headings, script/handwritten accent text, clean sans-serif body/nav).
// Swap these for the exact brand typefaces if an official style guide specifies different fonts.
const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-serif",
  weight: ["500", "600", "700"],
});

const caveat = Caveat({
  subsets: ["latin"],
  variable: "--font-script",
  weight: ["500", "600"],
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

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
      <body
        className={`${fraunces.variable} ${caveat.variable} ${inter.variable} bg-brand-cream font-sans text-brand-ink antialiased`}
      >
        {children}
      </body>
    </html>
  );
}

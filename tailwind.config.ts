import type { Config } from "tailwindcss";

// Proposed placeholder values approximated from the supplied "Bored of Toast" logo
// (royal blue, white, mustard/orange accent). Confirm exact brand hex codes before final launch —
// see "Design Direction" in the Landing Page Brief (Visual Style: Color palette).
const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          blue: "#1E40D8",
          mustard: "#F2A93B",
          cream: "#FAFAFA",
        },
      },
    },
  },
  plugins: [],
};

export default config;

import type { Config } from "tailwindcss";

// Design tokens updated per user-supplied design reference (editorial recipe-site mockup:
// cream background, dark "ink" text, mustard accent, sage green secondary accent, tan tag pills).
// Hex values are Proposed — estimated visually from the reference image. Replace with exact
// brand hex codes if/when an official style guide or design file is available.
const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          cream: "#FAF6EE",
          ink: "#23201B",
          mustard: "#E7A93E",
          sage: "#A9AE8C",
          tag: "#EEEAE1",
        },
      },
      fontFamily: {
        serif: ["var(--font-serif)", "serif"],
        script: ["var(--font-script)", "cursive"],
        sans: ["var(--font-sans)", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;

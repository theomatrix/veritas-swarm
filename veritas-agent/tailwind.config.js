/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        bg: "#050816",
        panel: "rgba(255, 255, 255, 0.05)",
        border: "rgba(255, 255, 255, 0.1)",
        text: "rgba(255, 255, 255, 0.92)",
        muted: "rgba(255, 255, 255, 0.6)",
        accent: {
          DEFAULT: "#2F8CFF",
          glow: "#5AF0FF",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      backgroundImage: {
        "glow-radial": "radial-gradient(circle at center, rgba(47, 140, 255, 0.15) 0%, transparent 70%)",
        "glow-conic": "conic-gradient(from 180deg at 50% 50%, #2a8af6 0deg, #a853ba 180deg, #e92a67 360deg)",
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "float": "float 6s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
      },
    },
  },
  plugins: [],
};

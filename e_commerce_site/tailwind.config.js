/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./*/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        // Aangan Living palette — neutral, warm, premium
        cream: "#FAF7F2",
        paper: "#FFFFFF",
        sand: "#F3EDE4",
        linen: "#E5DCCD",
        bark: "#26201A",
        cocoa: "#57493B",
        stone: "#8B7E6F",
        clay: {
          DEFAULT: "#A4623C",
          dark: "#8A5231",
          light: "#C0865F",
          pale: "#F0E4DA",
        },
        moss: "#5C6654",
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Manrope', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        widest2: "0.22em",
      },
      maxWidth: {
        "8xl": "88rem",
      },
      aspectRatio: {
        "4/5": "4 / 5",
        "3/4": "3 / 4",
        "16/9": "16 / 9",
      },
    },
  },
  plugins: [],
};

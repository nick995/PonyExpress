/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
    theme: {
    extend: {
      maxHeight: {
        fitted: "calc(50vh - 48px)",
      }
    },
  },
  plugins: [],
}


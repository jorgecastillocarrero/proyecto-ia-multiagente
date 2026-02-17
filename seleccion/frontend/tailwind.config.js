/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'carihuela-blue': '#003366',
        'carihuela-dark': '#002244',
      },
    },
  },
  plugins: [],
}
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    // Instead of require, use direct import
    (await import('@tailwindcss/forms')).default,
    (await import('daisyui')).default
  ],
}

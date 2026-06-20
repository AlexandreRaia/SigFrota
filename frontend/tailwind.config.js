/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          300: '#93c5fd',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1e40af',
          900: '#172554',
        },
      },
    },
  },
  plugins: [],
}

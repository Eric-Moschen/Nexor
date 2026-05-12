/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        nexor: {
          navy: '#0F172A',
          graphite: '#1F2937',
          purple: '#7C3AED',
          surface: '#F8FAFC',
        },
      },
    },
  },
  plugins: [],
};

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      screens: {
        'xs': { max: '480px' },
        'sm': { min: '481px', max: '767px' },
        'md': { min: '768px', max: '991px' },
        'lg': { min: '992px', max: '1199px' },
        'xl': { min: '1200px', max: '1399px' },
        '2xl': { min: '1400px', max: '1799px' },
        '3xl': { min: '1800px', max: '1999px' },
      },
      borderRadius: {
        blob: "30% 70% 82% 18% / 48% 69% 31% 52%",
        imageBlob: '0px 0px 200px 200px',
      },
      colors: {
        customGreen: '#6EAB36',
        customTealBlue: '#007E85',
        customWhite:'#ECECEC'
      },
      fontFamily: {
        lato: ['Lato', 'sans-serif'],
        dmsans: ['DM Sans', 'sans-serif'],
        montserrat: ['Montserrat', 'sans-serif'],
        lexend: ['Lexend Tera', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
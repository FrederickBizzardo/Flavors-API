/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html',
    './static/js/**/*.js',],
  theme: {
    extend: {
      fontFamily: {
        'OnestR': ['onest-regular', 'sans-serif'],
        'OnestB': ['onest-black', 'sans-serif'],
      },
    },
  },
  plugins: [],
}


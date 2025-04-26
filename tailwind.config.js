/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./static/**/*.{html,js,svg}",
  "./templates/**/*.{html,js,svg}"],
  theme: {
    cursor: {
       auto: 'auto',
       default: 'default',
       pointer: 'pointer',
       wait: 'wait',
       text: 'text',
       move: 'move',
       'not-allowed': 'not-allowed',
       crosshair: 'crosshair',
       'zoom-in': 'zoom-in',
    },
    extend: {},
  },
  plugins: [],
}


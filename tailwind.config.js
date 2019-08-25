module.exports = {
  theme: {
    spinner: (theme) => ({
      default: {
        color: theme('colors.gray.200'),
        size: '3em',
        border: '4px',
        speed: '700ms',
      },
    }),
    extend: {
      colors: {
        'semi-75': 'rgba(0, 0, 0, 0.75)',
      },
    },
  },
  variants: {
    spinner: ['responsive'],
  },
  plugins: [
    require('@tailwindcss/custom-forms'),
    require('tailwindcss-spinner')(),
  ],
}

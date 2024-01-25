/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.{html,js}"],
    theme: {
        fontFamily: {
            sans: ['Lato', 'sans-serif']
        },
        colors: {
            "primary": "#6750A4",
            "onprimary": "#FFFFFF",
            "primary-container": "#EADDFF",
            "onprimary-container": "#21005D",
            "secondary": "#625B71",
            "onsecondary": "#FFFFFF",
            "secondary-container": "#E8DEF8",
            "onsecondary-container": "#1D192B",
            "tertiary": "#7D5260",
            "ontertiary": "#FFFFFF",
            "tertiary-container": "#FFD8E4",
            "ontertiary-container": "#31111D",
            "background": "#FFFBFE",
            "onbackground": "#1C1B1F",
            "surface": "#FFFBFE",
            "onsurface": "#1C1B1F",
            "outline": "#79747E",
            "outline-surface": "#E7E0EC",
            "outline-onsurface": "#49454F",
        },
        extend: {},
    },
    plugins: [],
}

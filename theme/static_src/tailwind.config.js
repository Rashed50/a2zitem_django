module.exports = {
    darkMode: 'class',
    content: [
        // Django templates
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',

        // Vue components (যদি Vue frontend Django প্রজেক্টের ভিতরে থাকে)
        '../../**/*.vue',
        '../../frontend/src/**/*.vue',
        '../../frontend/**/*.js',
    ],
    theme: {
        extend: {
            screens: {
                'lg': '900px',
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/container-queries'),
    ],
    safelist: [
        // Sidebar gradients
        'from-sky-800', 'to-sky-900',
        'from-emerald-700', 'to-emerald-900',
        'from-purple-800', 'to-purple-900',
        'from-indigo-800', 'to-indigo-900',
        'from-slate-800', 'to-slate-900',
        'from-gray-50', 'to-gray-100',
        // Sidebar text & hover
        'text-white', 'text-gray-700', 'text-blue-700',
        'hover:bg-white/10', 'hover:bg-gray-200',
        'bg-white/10', 'bg-gray-200',
        'border-white/10', 'border-gray-200',
        'bg-white/20', 'bg-blue-100',
        // Dark mode overrides
        'from-gray-800', 'to-gray-900',
        'text-gray-200', 'text-gray-300', 'text-yellow-300',
        'hover:bg-gray-700', 'bg-gray-800', 'bg-gray-900',
        'border-gray-700'
    ],
}

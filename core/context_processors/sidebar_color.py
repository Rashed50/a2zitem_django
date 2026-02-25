def sidebar_color(request):
    # Default color scheme (Sky)
    color_scheme = request.session.get('color_scheme', 'slate')
    dark_mode = request.session.get('is_dark', False)  # dark mode flag
    
    color_palettes = {
        'sky': {
            'theme': '#0ea5e9',
            'sidebar_bg_from': 'from-sky-800',
            'sidebar_bg_to': 'to-sky-900',
            'menu_text': 'text-white',
            'menu_hover_bg': 'hover:bg-white/10',
            'menu_icon_bg': 'bg-white/10',
            'border_color': 'border-white/10',
            'active_class': '#ffffff33',
            'active_text': '#ffffff',
            'name': 'Sky Blue'
        },
        'emerald': {
            'theme': '#10b981',
            'sidebar_bg_from': 'from-emerald-700',
            'sidebar_bg_to': 'to-emerald-900',
            'menu_text': 'text-white',
            'menu_hover_bg': 'hover:bg-white/10',
            'menu_icon_bg': 'bg-white/10',
            'border_color': 'border-white/10',
            'active_class': '#ffffff33',
            'active_text': '#ffffff',
            'name': 'Emerald Green'
        },
        'purple': {
            'theme': '#8b5cf6',
            'sidebar_bg_from': 'from-purple-800',
            'sidebar_bg_to': 'to-purple-900',
            'menu_text': 'text-white',
            'menu_hover_bg': 'hover:bg-white/10',
            'menu_icon_bg': 'bg-white/10',
            'border_color': 'border-white/10',
            'active_class': '#ffffff33',
            'active_text': '#ffffff',
            'name': 'Deep Purple'
        },
        'indigo': {
            'theme': '#3b82f6',
            'sidebar_bg_from': 'from-indigo-800',
            'sidebar_bg_to': 'to-indigo-900',
            'menu_text': 'text-white',
            'menu_hover_bg': 'hover:bg-white/10',
            'menu_icon_bg': 'bg-white/10',
            'border_color': 'border-white/10',
            'active_class': '#ffffff33',
            'active_text': '#ffffff',
            'name': 'Royal Indigo'
        },
        'slate': {
            'theme': '#64748b',
            'sidebar_bg_from': 'from-slate-800',
            'sidebar_bg_to': 'to-slate-900',
            'menu_text': 'text-white',
            'menu_hover_bg': 'hover:bg-white/10',
            'menu_icon_bg': 'bg-white/10',
            'border_color': 'border-white/10',
            'active_class': '#ffffff33',
            'active_text': '#ffffff',
            'name': 'Dark Slate'
        },
        'light': {
            'theme': '#f5f5f4',
            'sidebar_bg_from': 'from-gray-50',
            'sidebar_bg_to': 'to-gray-100',
            'menu_text': 'text-gray-700',
            'menu_hover_bg': 'hover:bg-gray-200',
            'menu_icon_bg': 'bg-gray-200',
            'border_color': 'border-gray-200',
            'active_class': '#6A7282',
            'active_text': '#F5F5F4',
            'name': 'Light Mode'
        }
    }
    
    # dark_palette = {
    #     'sidebar_bg_from': 'from-gray-800',
    #     'sidebar_bg_to': 'to-gray-900',
    #     'menu_text': 'text-gray-200',
    #     'menu_hover_bg': 'hover:bg-gray-700/30',
    #     'menu_icon_bg': 'bg-gray-700/30',
    #     'border_color': 'border-gray-700/30',
    #     'active_class': 'bg-gray-700/50',
    #     'active_text': 'text-white',
    #     'name': 'Dark Mode'
    # }
    
    ## If dark mode active, use dark_palette
    # sidebar_colors = dark_palette if dark_mode else color_palettes.get(color_scheme, color_palettes['sky'])

    return {
        'sidebar_colors' : color_palettes[color_scheme],
        'color_schemes'  : color_palettes,
        'dark_mode'      : dark_mode,
    }
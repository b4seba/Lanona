# styles.py

# Paleta de Colores Moderna
COLORS = {
    'primary': '#007BFF',
    'secondary': '#6C757D',
    'success': '#28A745',
    'danger': '#DC3545',
    'warning': '#FFC107',
    'info': '#17A2B8',
    'light': '#F8F9FA',
    'dark': '#343A40',
    'white': '#FFFFFF',
    'gray': '#ADB5BD',
    'border': '#DEE2E6'
}

#tipografia
FONTS = {
    'title': ('Segoe UI', 20, 'bold'),
    'subtitle': ('Segoe UI', 12),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 8, 'italic'),
    'button': ('Segoe UI', 10, 'bold')
}

BUTTON_STYLES = {
    'base': {
        'fg': COLORS['white'],
        'font': FONTS['button'],
        'relief': 'flat',
        'borderwidth': 0,
        'padx': 18,
        'pady': 8,
        'cursor': 'hand2'
    },
    'primary': {
        'bg': COLORS['primary'],
        'activebackground': '#0056b3',
        'activeforeground': COLORS['white']
    },
    'secondary': {
        'bg': COLORS['secondary'],
        'activebackground': '#545b62',
        'activeforeground': COLORS['white']
    },
    'success': {
        'bg': COLORS['success'],
        'activebackground': '#1e7e34',
        'activeforeground': COLORS['white']
    },
    'danger': {
        'bg': COLORS['danger'],
        'activebackground': '#b21f2d',
        'activeforeground': COLORS['white']
    },
    'warning': {
        'bg': COLORS['warning'],
        'activebackground': '#d39e00',
        'activeforeground': COLORS['dark']
    }
}

LABEL_STYLES = {
    'title': {
        'font': FONTS['title'],
        'fg': COLORS['dark'],
        'bg': COLORS['light']
    },
    'subtitle': {
        'font': FONTS['subtitle'],
        'fg': COLORS['secondary'],
        'bg': COLORS['light']
    },
    'card_title': {
        'font': ('Segoe UI', 14, 'bold'),
        'fg': COLORS['dark'],
        'bg': COLORS['white']
    },
    'body': {
        'font': FONTS['body'],
        'fg': COLORS['dark'],
        'bg': COLORS['white']
    },
    'error': {
        'font': FONTS['body'],
        'fg': COLORS['danger'],
        'bg': COLORS['white']
    },
    'success': {
        'font': FONTS['body'],
        'fg': COLORS['success'],
        'bg': COLORS['white']
    },
    'small': {
        'font': FONTS['small'],
        'fg': COLORS['gray'],
        'bg': COLORS['light']
    }
}

#estilos para los campos de texto
ENTRY_STYLES = {
    'default': {
        'font': FONTS['body'],
        'relief': 'solid',
        'bd': 1,
        'bg': COLORS['white'],
        'fg': COLORS['dark'],
        'highlightthickness': 1,
        'highlightbackground': COLORS['border'],
        'highlightcolor': COLORS['primary'],
        'insertbackground': COLORS['dark']
    }
}

FRAME_STYLES = {
    'main': {
        'bg': COLORS['light'],
    },
    'card': {
        'bg': COLORS['white'],
        'relief': 'solid',
        'bd': 1,
        'highlightbackground': COLORS['border'],
        'highlightthickness': 1
    }
}
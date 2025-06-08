import tkinter as tk
from styles import BUTTON_STYLES, LABEL_STYLES, ENTRY_STYLES, FRAME_STYLES, COLORS, FONTS

def _merge_styles(base_style, explicit_kwargs):
    final_style = base_style.copy()
    final_style.update(explicit_kwargs)
    return final_style

class StyledButton(tk.Button):
    def __init__(self, parent, text, style='primary', command=None, **kwargs):
        base_style = BUTTON_STYLES['base']
        style_variant = BUTTON_STYLES.get(style, BUTTON_STYLES['primary'])
        combined_style = _merge_styles(base_style, style_variant)
        final_style = _merge_styles(combined_style, kwargs)

        super().__init__(parent, text=text, command=command, **final_style)
        
        self.original_bg = final_style['bg']
        self.hover_color = self._get_hover_color(self.original_bg)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.config(bg=self.hover_color)

    def _on_leave(self, e):
        self.config(bg=self.original_bg)

    def _get_hover_color(self, color_hex):
        try:
            r = int(color_hex[1:3], 16)
            g = int(color_hex[3:5], 16)
            b = int(color_hex[5:7], 16)
            factor = 0.9
            r = max(0, int(r * factor))
            g = max(0, int(g * factor))
            b = max(0, int(b * factor))
            return f"#{r:02x}{g:02x}{b:02x}"
        except (ValueError, IndexError):
            return color_hex

class StyledLabel(tk.Label):
    def __init__(self, parent, text, style='body', **kwargs):
        style_config = LABEL_STYLES.get(style, LABEL_STYLES['body'])

        if 'bg' not in style_config and 'bg' not in kwargs:
            kwargs['bg'] = parent.cget('bg')

        final_style = _merge_styles(style_config, kwargs)
        super().__init__(parent, text=text, **final_style)

class StyledEntry(tk.Entry):
    def __init__(self, parent, placeholder="", **kwargs):
        style_config = ENTRY_STYLES['default']
        final_style = _merge_styles(style_config, kwargs)

        super().__init__(parent, **final_style)

        self.placeholder = placeholder
        self.placeholder_color = COLORS['gray']
        self.default_fg_color = final_style.get('fg', COLORS['dark'])

        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self.put_placeholder()

    def put_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)

    def _on_focus_in(self, event):
        self.config(highlightthickness=2)
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg=self.default_fg_color)

    def _on_focus_out(self, event):
        self.config(highlightthickness=1)
        if not self.get():
            self.put_placeholder()

    def get_value(self):
        val = self.get()
        return "" if val == self.placeholder else val

class StyledFrame(tk.Frame):
    def __init__(self, parent, style='main', **kwargs):
        style_config = FRAME_STYLES.get(style, FRAME_STYLES['main'])
        final_style = _merge_styles(style_config, kwargs)
        super().__init__(parent, **final_style)

class MessageDialog:
    @staticmethod
    def _create_dialog(parent, title, message, icon, style):
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.configure(bg=COLORS['white'])
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()

        parent.update_idletasks()
        p_width = parent.winfo_width()
        p_height = parent.winfo_height()
        p_x = parent.winfo_x()
        p_y = parent.winfo_y()
        d_width = 320
        d_height = 160
        x = p_x + (p_width // 2) - (d_width // 2)
        y = p_y + (p_height // 2) - (d_height // 2)
        dialog.geometry(f"{d_width}x{d_height}+{x}+{y}")

        main_frame = tk.Frame(dialog, bg=COLORS['white'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        icon_label = tk.Label(main_frame, text=icon, font=('Segoe UI', 28), bg=COLORS['white'])
        icon_label.pack()

        message_label = tk.Label(main_frame, text=message, wraplength=280,
                                 font=FONTS['body'], bg=COLORS['white'], fg=COLORS['dark'])
        message_label.pack(pady=10)

        close_button = StyledButton(main_frame, "Cerrar", style=style, command=dialog.destroy)
        close_button.pack(pady=(5,0))
        
        close_button.focus_set()
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())

    @staticmethod
    def show_error(parent, title, message):
        MessageDialog._create_dialog(parent, title, message, "❌", "danger")

    @staticmethod
    def show_success(parent, title, message):
        MessageDialog._create_dialog(parent, title, message, "✅", "success")

    @staticmethod
    def show_info(parent, title, message):
        MessageDialog._create_dialog(parent, title, message, "ℹ️", "primary")

class LoginForm(StyledFrame):
    def __init__(self, parent, title, on_login, on_cancel, **kwargs):
        super().__init__(parent, style='card', **kwargs)
        self.pack(fill='both', expand=True, padx=30, pady=30)
        
        self.on_login = on_login
        
        StyledLabel(self, title, style='card_title').pack(pady=(0, 20))
        
        StyledLabel(self, "Usuario:", style='body').pack(anchor='w', pady=(10, 2))
        self.entry_user = StyledEntry(self, placeholder="Ingrese su usuario")
        self.entry_user.pack(fill='x', ipady=4)
        
        StyledLabel(self, "Contraseña:", style='body').pack(anchor='w', pady=(10, 2))
        self.entry_password = StyledEntry(self, show="*", placeholder="Ingrese su contraseña")
        self.entry_password.pack(fill='x', ipady=4)
        
        button_frame = tk.Frame(self, bg=self.cget('bg'))
        button_frame.pack(fill='x', pady=(25, 0))
        
        StyledButton(button_frame, "Iniciar Sesión", style='primary',
                    command=self._handle_login).pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        StyledButton(button_frame, "Cancelar", style='secondary',
                    command=on_cancel).pack(side='right', expand=True, fill='x', padx=(5, 0))
        
        self.entry_password.bind('<Return>', lambda e: self._handle_login())
        
    def _handle_login(self):
        username = self.entry_user.get_value()
        password = self.entry_password.get_value()
        
        if not username or not password:
            MessageDialog.show_error(self, "Campos Vacíos", "Por favor, complete todos los campos.")
            return
            
        self.on_login(username, password)
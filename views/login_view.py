# views/login_view.py

import tkinter as tk
from ui_components import StyledFrame, LoginForm

class LoginView(StyledFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='main')
        self.controller = controller

        # Contenedor para centrar el formulario de login
        center_frame = tk.Frame(self, bg=self.cget('bg'))
        center_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.4, relheight=0.5)

        # Usamos el componente LoginForm directamente
        login_form = LoginForm(
            parent=center_frame,
            title="Bienvenido al Sistema POS",
            on_login=self.controller.login,
            on_cancel=self.controller.root.destroy
        )
        login_form.pack(pady=20, padx=20)
# views/jefe_view.py

import tkinter as tk
from ui_components import StyledFrame, StyledLabel, StyledButton

class JefeView(StyledFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='main')
        self.controller = controller

        # Header
        header = StyledFrame(self, style='main', relief='solid', bd=1)
        header.pack(fill='x', padx=10, pady=10)
        StyledLabel(header, text=f"Panel de Administrador: {controller.usuario_actual}", style='title').pack(pady=10)

        # Contenedor de botones
        btn_container = StyledFrame(self, style='main')
        btn_container.pack(expand=True)

        buttons = {
            "Agregar Producto": ('primary', controller.agregar_producto),
            "Abrir Día": ('success', controller.abrir_dia),
            "Cerrar Día": ('warning', controller.cerrar_dia),
            "Informe de Ventas": ('primary', controller.mostrar_informes),
            "Cerrar Sesión": ('danger', controller.logout)
        }

        for text, (style, command) in buttons.items():
            btn = StyledButton(btn_container, text=text, style=style, command=command)
            btn.pack(pady=8, padx=50, fill='x')
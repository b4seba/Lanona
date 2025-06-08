import tkinter as tk
from tkinter import messagebox
from ui_components import StyledFrame, StyledLabel, StyledButton, MessageDialog
from styles import COLORS

class VentanaVendedor:
    def __init__(self, user_data):
        self.user_data = user_data
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Panel de Ventas")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        self.root.configure(bg=COLORS['light'])
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        pass

    def create_widgets(self):
        main_frame = StyledFrame(self.root, style='main')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # encabezado
        header_frame = StyledFrame(main_frame, style='main')
        header_frame.pack(fill='x', pady=(0, 15))
        StyledLabel(header_frame, "🛒 Panel de Ventas", style='title').pack(anchor='w')
        StyledLabel(header_frame, f"Vendedor: {self.user_data['nombre']}", style='subtitle').pack(anchor='w')

        # pie de pagina
        StyledButton(
            main_frame, 
            "🚪 Cerrar Sesión", 
            style='danger', 
            command=self.cerrar_sesion
        ).pack(side='bottom', fill='x', pady=(20, 0), ipady=5)

        # contenido
        content_frame = StyledFrame(main_frame, style='main')
        content_frame.pack(fill='both', expand=True)

        left_frame = StyledFrame(content_frame, style='main')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        right_frame = StyledFrame(content_frame, style='main')
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # operaciones de Venta
        ops_card = StyledFrame(left_frame, style='card')
        ops_card.pack(fill='both', expand=True)
        StyledLabel(ops_card, "🏪 Operaciones Principales", style='card_title').pack(pady=15, padx=20, anchor='w')
        StyledButton(ops_card, "💳 Nueva Venta", style='primary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        StyledButton(ops_card, "🔍 Buscar Producto", style='secondary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        StyledButton(ops_card, "📋 Consultar Precio", style='secondary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        StyledButton(ops_card, "🎫 Reimprimir Ticket", style='secondary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        
        # consultas
        query_card = StyledFrame(left_frame, style='card')
        query_card.pack(fill='x', pady=(20, 0))
        StyledLabel(query_card, "📊 Consultas Rápidas", style='card_title').pack(pady=15, padx=20, anchor='w')
        StyledButton(query_card, "📈 Ventas del Día", style='success', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        StyledButton(query_card, "💰 Total en Caja", style='success', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        
        # estado de Sistema
        status_card = StyledFrame(right_frame, style='card')
        status_card.pack(fill='x', pady=(0, 20))
        StyledLabel(status_card, "ℹ️ Estado del Sistema", style='card_title').pack(pady=15, padx=20, anchor='w')
        StyledLabel(status_card, "✅ Caja: Abierta", style='body').pack(anchor='w', padx=20, pady=2)
        StyledLabel(status_card, "🔗 Conexión: Estable", style='body').pack(anchor='w', padx=20, pady=2)
        StyledLabel(status_card, "🖨️Impresora: En línea", style='body').pack(anchor='w', padx=20, pady=(2, 20))

        # acciones Rápidas
        actions_card = StyledFrame(right_frame, style='card')
        actions_card.pack(fill='both', expand=True)
        StyledLabel(actions_card, "⚡ Acciones Rápidas", style='card_title').pack(pady=15, padx=20, anchor='w')
        StyledButton(actions_card, "🏷️ Gestionar Descuentos", style='primary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        StyledButton(actions_card, "👥 Consultar Cliente", style='secondary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)

    def show_not_implemented(self):
        MessageDialog.show_info(self.root, "Función no Disponible", "Esta funcionalidad aún no ha sido implementada.")

    def cerrar_sesion(self):
        if messagebox.askyesno("Confirmar Cierre", "¿Está seguro de que desea cerrar la sesión?"):
            self.root.destroy()
            self.user_data = None
            self.auth = None
            from main import MainApplication
            app = MainApplication()
            app.run()

    def run(self):
        self.root.mainloop()

def ventana_vendedor(user_data):
    vendedor_window = VentanaVendedor(user_data)
    vendedor_window.run()
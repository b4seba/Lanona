import tkinter as tk
from tkinter import messagebox
from auth_manager import AuthManager
from ui_components import StyledFrame, StyledLabel, StyledButton, MessageDialog, LoginForm
from styles import COLORS
from ventana_Vendedor import ventana_vendedor

class VentanaJefe:
    def __init__(self, user_data, parent_root):
        self.user_data = user_data
        self.auth = AuthManager()
        parent_root.destroy()
        
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Panel de Control - Jefe de Ventas")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['light'])
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        main_frame = StyledFrame(self.root, style='main')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        header_frame = StyledFrame(main_frame, style='main')
        header_frame.pack(fill='x', pady=(0, 20))
        StyledLabel(header_frame, "👨‍💼 Panel de Control del Jefe", style='title', bg=main_frame.cget('bg')).pack()
        StyledLabel(header_frame, f"Bienvenido, {self.user_data['nombre']}", style='subtitle', bg=main_frame.cget('bg')).pack()

        ops_container = StyledFrame(main_frame, style='main')
        ops_container.pack(fill='both', expand=True)

        left_col = StyledFrame(ops_container, style='main')
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 10))

        right_col = StyledFrame(ops_container, style='main')
        right_col.pack(side='right', fill='both', expand=True, padx=(10, 0))

        jefe_ops_card = StyledFrame(left_col, style='card')
        jefe_ops_card.pack(fill='both', expand=True, pady=(0, 10))
        StyledLabel(jefe_ops_card, "Operaciones", style='card_title', bg=jefe_ops_card.cget('bg')).pack(pady=15, anchor='w', padx=20)
        StyledButton(jefe_ops_card, "📊 Ver Reportes", style='primary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        StyledButton(jefe_ops_card, "💰 Gestión de Caja", style='primary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)

        config_card = StyledFrame(right_col, style='card')
        config_card.pack(fill='both', expand=True, pady=(0, 10))
        StyledLabel(config_card, "Configuración", style='card_title', bg=config_card.cget('bg')).pack(pady=15, anchor='w', padx=20)
        StyledButton(config_card, "⚙️ Ajustes del Sistema", style='secondary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)
        StyledButton(config_card, "👤 Gestionar Usuarios", style='secondary', command=self.show_not_implemented).pack(fill='x', padx=20, pady=5)

        # Tarjeta para acceceder al vendedor
        vendor_card = StyledFrame(main_frame, style='card')
        vendor_card.pack(fill='x', pady=(10, 0))
        StyledLabel(vendor_card, "Acceso al Punto de Venta", style='card_title', bg=vendor_card.cget('bg')).pack(pady=15)
        StyledButton(vendor_card, "🚀 Iniciar Sesión Vendedor", style='success', command=self.login_vendedor).pack(fill='x', padx=100, pady=10)

        StyledButton(main_frame, "🚪 Cerrar Sesión", style='danger', command=self.cerrar_sesion).pack(side='bottom', pady=(20, 0))

    def show_not_implemented(self):
        MessageDialog.show_info(self.root, "Función no Disponible", "Esta funcionalidad está en desarrollo.")

    def login_vendedor(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Acceso Vendedor")
        login_window.geometry("400x380")
        login_window.resizable(False, False)
        login_window.configure(bg=COLORS['light'])
        login_window.transient(self.root)
        login_window.grab_set()
        
        login_form = LoginForm(login_window, "🛒 Acceso Vendedor",
                               on_login=self.validar_vendedor,
                               on_cancel=login_window.destroy)

    def validar_vendedor(self, username, password):
        result = self.auth.validar_usuario(username, password)
        
        login_window = self.root.winfo_children()[-1] # Obtener la ventana Toplevel de login

        if not result['success']:
            MessageDialog.show_error(login_window, "Error de Login", result['message'])
            return
        
        if not self.auth.es_vendedor(username):
            MessageDialog.show_error(login_window, "Acceso Denegado", "Este usuario no tiene permisos de vendedor.")
            return
        
        login_window.destroy()
        MessageDialog.show_success(self.root, "Login Exitoso", f"Bienvenido, {result['user']['nombre']}!")
        self.root.after(1200, lambda: self.abrir_panel_vendedor(result['user']))

    def abrir_panel_vendedor(self, user_data):
        self.root.destroy()
        ventana_vendedor(user_data)

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

def ventana_Jefe(user_data, parent_root):
    jefe_window = VentanaJefe(user_data, parent_root)
    jefe_window.run()
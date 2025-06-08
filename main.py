import tkinter as tk
from tkinter import messagebox
from login import LoginManager
from ui_components import StyledFrame, StyledLabel, StyledButton, StyledEntry, MessageDialog
from styles import COLORS

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.login_manager = LoginManager()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Los Monitos de la Nona - Sistema de Ventas")
        self.root.geometry("450x480")
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
        header_frame.pack(pady=(10, 20))
        
        StyledLabel(header_frame, "🐒 Los Monitos de la Nona", style='title', bg=main_frame.cget('bg')).pack()
        StyledLabel(header_frame, "Punto de Venta v2.0", style='subtitle', bg=main_frame.cget('bg')).pack(pady=5)
        
        form_frame = StyledFrame(main_frame, style='card')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        StyledLabel(form_frame, "ACCESO JEFE DE VENTAS", style='card_title', bg=form_frame.cget('bg')).pack(pady=(20, 20))
        
        StyledLabel(form_frame, "Usuario", style='body', bg=form_frame.cget('bg')).pack(anchor='w', padx=20, pady=(10, 2))
        self.entry_id = StyledEntry(form_frame, placeholder="Ingrese ID de jefe")
        self.entry_id.pack(fill='x', padx=20, ipady=5)
        self.entry_id.focus()
        
        StyledLabel(form_frame, "Contraseña", style='body', bg=form_frame.cget('bg')).pack(anchor='w', padx=20, pady=(15, 2))
        self.entry_clave = StyledEntry(form_frame, show="*", placeholder="Ingrese contraseña")
        self.entry_clave.pack(fill='x', padx=20, ipady=5)
        
        button_frame = StyledFrame(form_frame, style='main', bg=form_frame.cget('bg'))
        button_frame.pack(fill='x', padx=20, pady=(30, 20))
        
        StyledButton(button_frame,
                     "🔓 Abrir Caja", style='primary', command=self.iniciar_sesion).pack(fill='x')
        StyledButton(button_frame, "❌ Salir", style='danger', command=self.salir_aplicacion).pack(fill='x', pady=(10, 0))
        
        self.entry_clave.bind('<Return>', lambda e: self.iniciar_sesion())
        
        StyledLabel(self.root, "© 2025 Los Monitos de la Nona Inc.", style='small', bg=main_frame.cget('bg')).pack(side='bottom', pady=10)

    def iniciar_sesion(self):
        usuario = self.entry_id.get_value()
        clave = self.entry_clave.get_value()



        if not usuario or not clave:
            MessageDialog.show_error(self.root, "Campos Vacíos", "Por favor, complete todos los campos.")
            return
        
        success = self.login_manager.login_jefe(usuario, clave, self.root)
        if not success:
            self.entry_clave.delete(0, tk.END)

    def salir_aplicacion(self):
        if messagebox.askyesno("Confirmar Salida", "¿Está seguro de que desea salir?"):
            self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()
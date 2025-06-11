from tkinter import Tk, Toplevel
import tkinter as tk
from ui_components import StyledFrame, StyledLabel, StyledEntry, StyledButton, MessageDialog

class AgregarProductoView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.title("Agregar Producto")
        self.controller = controller
        self.geometry("400x350")
        self.resizable(False, False)
        
        # Configurar el fondo principal
        self.configure(bg='#F8F9FA')  # Usando COLORS['light']
        
        # Frame principal con estilo de tarjeta
        main_frame = StyledFrame(self, style='card')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        StyledLabel(main_frame, "Agregar Producto", style='card_title').pack(pady=(0, 20))
        
        # Campo Nombre
        StyledLabel(main_frame, "Nombre:", style='body').pack(anchor='w', pady=(5, 0))
        self.entry_nombre = StyledEntry(main_frame, placeholder="Ingrese el nombre del producto")
        self.entry_nombre.pack(fill='x', ipady=4, pady=(0, 10))
        
        # Campo Precio
        StyledLabel(main_frame, "Precio:", style='body').pack(anchor='w', pady=(5, 0))
        self.entry_precio = StyledEntry(main_frame, placeholder="Ingrese el precio")
        self.entry_precio.pack(fill='x', ipady=4, pady=(0, 10))
        
        # Campo SKU
        StyledLabel(main_frame, "SKU:", style='body').pack(anchor='w', pady=(5, 0))
        self.entry_codigo = StyledEntry(main_frame, placeholder="Ingrese el código SKU")
        self.entry_codigo.pack(fill='x', ipady=4, pady=(0, 20))
        
        # Botón Guardar
        button_frame = StyledFrame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        StyledButton(button_frame, "Guardar", style='success', 
                    command=self.guardar_producto).pack(side='left', expand=True, fill='x')
        
        # Enfocar el primer campo
        self.entry_nombre.focus_set()
        
        # Configurar atajos de teclado
        self.entry_codigo.bind('<Return>', lambda e: self.guardar_producto())

    def guardar_producto(self):
        codigo = self.entry_codigo.get_value()
        nombre = self.entry_nombre.get_value()
        precio_str = self.entry_precio.get_value()
        
        # Validaciones
        if not codigo or not nombre or not precio_str:
            MessageDialog.show_error(self, "Campos Vacíos", "Todos los campos son obligatorios.")
            return
            
        try:
            precio = float(precio_str)
            if precio <= 0:
                raise ValueError
        except ValueError:
            MessageDialog.show_error(self, "Error", "El precio debe ser un número válido mayor a cero.")
            return

        # Lógica para guardar el producto
        if codigo in self.controller.db.productos:
            MessageDialog.show_error(self, "Error", "El código SKU ya existe.")
            return

        self.controller.db.productos[codigo] = {
            'nombre': nombre,
            'precio': precio
        }
        self.controller.db.save_data()
        
        MessageDialog.show_success(self, "Éxito", "Producto agregado correctamente.")
        self.destroy()
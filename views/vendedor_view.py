# views/vendedor_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from styles import COLORS, FONTS
from ui_components import StyledFrame, StyledLabel, StyledEntry, StyledButton
from views.cliente_dialog import ClienteDialog

class VendedorView(StyledFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='main')
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        # --- Header ---
        header = StyledFrame(self, style='main', bd=1, relief='solid')
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10,0))
        StyledLabel(header, text=f"Punto de Venta - Vendedor: {controller.usuario_actual}", style='subtitle').pack(side='left', padx=10)
        StyledButton(header, text="Cerrar Sesión", style='danger', command=controller.logout, pady=4, padx=10).pack(side='right', padx=10, pady=5)
        
        # --- Frame de Venta (Izquierda) ---
        venta_frame = StyledFrame(self, style='card', padx=10, pady=10)
        venta_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        venta_frame.grid_rowconfigure(0, weight=1)
        venta_frame.grid_columnconfigure(0, weight=1)

        columns = ('Cantidad', 'Código', 'Producto', 'Precio Unit.', 'Total')
        self.venta_tree = ttk.Treeview(venta_frame, columns=columns, show='headings', style="Treeview")
        for col in columns:
            self.venta_tree.heading(col, text=col)
        self.venta_tree.column('Cantidad', width=60, anchor='center')
        self.venta_tree.column('Código', width=80, anchor='center')
        self.venta_tree.column('Producto', width=200)
        self.venta_tree.column('Precio Unit.', width=80, anchor='center')
        self.venta_tree.column('Total', width=80, anchor='center')
        self.venta_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(venta_frame, orient="vertical", command=self.venta_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.venta_tree.configure(yscrollcommand=scrollbar.set)

        # --- Frame de Controles (Derecha) ---
        controls_frame = StyledFrame(self, style='main')
        controls_frame.grid(row=1, column=1, sticky="ns", padx=(5, 10), pady=10)
        
        # Búsqueda
        search_frame = StyledFrame(controls_frame, style='card', padx=15, pady=15)
        search_frame.pack(fill='x')
        StyledLabel(search_frame, "Buscar Producto", style='card_title').pack(anchor='w')
        self.search_entry = StyledEntry(search_frame, placeholder="SKU o Nombre")
        self.search_entry.pack(fill='x', ipady=4, pady=(10,5))
        self.search_entry.bind('<Return>', lambda e: self.controller.buscar_producto())
        
        self.productos_listbox = tk.Listbox(search_frame, height=6, font=FONTS['body'], bg=COLORS['white'], relief='solid', bd=1, highlightthickness=0)
        self.productos_listbox.pack(fill='x', pady=5)
        self.productos_listbox.bind('<Double-Button-1>', lambda e: self.controller.agregar_a_venta())
        StyledButton(search_frame, "Agregar a Venta", style='success', command=self.controller.agregar_a_venta).pack(fill='x', pady=5)

        # Totales y Acciones
        pago_frame = StyledFrame(controls_frame, style='card', padx=15, pady=15)
        pago_frame.pack(fill='x', pady=10)
        self.label_subtotal = StyledLabel(pago_frame, "Subtotal: $0", style='body')
        self.label_subtotal.pack(anchor='e')
        self.label_iva = StyledLabel(pago_frame, "IVA (19%): $0", style='body')
        self.label_iva.pack(anchor='e')
        self.label_total = StyledLabel(pago_frame, "Total: $0", style='card_title')
        self.label_total.pack(anchor='e', pady=(5,15))
        
        # Botones de documento
        btn_doc_frame = StyledFrame(pago_frame, style='main')
        btn_doc_frame.pack(fill='x', pady=(5,0))
        
        StyledButton(btn_doc_frame, "Boleta", style='primary', 
                   command=lambda: self.controller.generar_documento('boleta')).pack(side='left', expand=True, padx=2)
        StyledButton(btn_doc_frame, "Factura", style='primary', 
                   command=self._generar_factura).pack(side='left', expand=True, padx=2)
        
        StyledButton(pago_frame, "Limpiar Venta", style='warning', command=self.controller.limpiar_venta).pack(fill='x', pady=(8,2))

        # Frame de acciones adicionales
        actions_frame = StyledFrame(controls_frame, style='card', padx=15, pady=15)
        actions_frame.pack(fill='x', pady=5)
        
        StyledLabel(actions_frame, "Acciones", style='card_title').pack(anchor='w', pady=(0,10))
        
        # Botón para eliminar item seleccionado
        StyledButton(actions_frame, "Eliminar Item", style='danger', 
                    command=self._eliminar_item_seleccionado).pack(fill='x', pady=2)
        
        # Botón para modificar cantidad
        StyledButton(actions_frame, "Modificar Cantidad", style='warning', 
                    command=self._modificar_cantidad).pack(fill='x', pady=2)

    def _generar_factura(self):
        """Abre el diálogo para ingresar datos del cliente y genera la factura."""
        if not self.controller.venta_actual:
            messagebox.showwarning("Venta vacía", "Agregue productos antes de generar factura")
            return
        
        # Mostrar diálogo para datos del cliente
        dialog = ClienteDialog(self)
        cliente_data = dialog.show()
        
        if cliente_data:
            # Si el usuario confirmó los datos, generar la factura
            self.controller.generar_documento('factura', cliente_data)

    def _eliminar_item_seleccionado(self):
        """Elimina el item seleccionado de la venta."""
        selected = self.venta_tree.selection()
        if not selected:
            messagebox.showinfo("Sin selección", "Seleccione un item para eliminar")
            return
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Eliminar el item seleccionado?"):
            item_id = selected[0]
            # Obtener el código del producto del item seleccionado
            codigo = self.venta_tree.item(item_id, 'values')[1]
            self.controller.eliminar_item_venta(codigo)

    def _modificar_cantidad(self):
        """Permite modificar la cantidad de un item seleccionado."""
        selected = self.venta_tree.selection()
        if not selected:
            messagebox.showinfo("Sin selección", "Seleccione un item para modificar")
            return
        
        item_id = selected[0]
        valores = self.venta_tree.item(item_id, 'values')
        codigo = valores[1]
        cantidad_actual = valores[0]
        
        # Diálogo simple para nueva cantidad
        dialog = tk.Toplevel(self)
        dialog.title("Modificar Cantidad")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.configure(bg=COLORS['background'])
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (150)
        y = (dialog.winfo_screenheight() // 2) - (75)
        dialog.geometry(f"300x150+{x}+{y}")
        
        frame = StyledFrame(dialog, style='main', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        StyledLabel(frame, f"Cantidad actual: {cantidad_actual}", style='body').pack(pady=5)
        StyledLabel(frame, "Nueva cantidad:", style='body').pack(anchor='w')
        
        cantidad_entry = StyledEntry(frame)
        cantidad_entry.pack(fill='x', pady=5, ipady=4)
        cantidad_entry.insert(0, str(cantidad_actual))
        cantidad_entry.select_range(0, tk.END)
        cantidad_entry.focus_set()
        
        def confirmar():
            try:
                nueva_cantidad = int(cantidad_entry.get())
                if nueva_cantidad <= 0:
                    messagebox.showwarning("Cantidad inválida", "La cantidad debe ser mayor a 0", parent=dialog)
                    return
                self.controller.modificar_cantidad_item(codigo, nueva_cantidad)
                dialog.destroy()
            except ValueError:
                messagebox.showwarning("Cantidad inválida", "Ingrese un número válido", parent=dialog)
        
        btn_frame = StyledFrame(frame, style='main')
        btn_frame.pack(fill='x', pady=10)
        
        StyledButton(btn_frame, "Cancelar", style='secondary', 
                    command=dialog.destroy).pack(side='right', padx=(5,0))
        StyledButton(btn_frame, "Confirmar", style='success', 
                    command=confirmar).pack(side='right')
        
        cantidad_entry.bind('<Return>', lambda e: confirmar())
        dialog.bind('<Escape>', lambda e: dialog.destroy())

    def actualizar_totales(self, subtotal, iva, total):
        """Actualiza los labels de totales en la interfaz."""
        self.label_subtotal.config(text=f"Subtotal: ${subtotal:,.0f}")
        self.label_iva.config(text=f"IVA (19%): ${iva:,.0f}")
        self.label_total.config(text=f"Total: ${total:,.0f}")
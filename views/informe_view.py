import tkinter as tk
from tkinter import ttk
from datetime import date
from tkcalendar import DateEntry
from styles import COLORS, FONTS
from ui_components import StyledButton  # Importar el botón estilizado

class InformeView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['light'])
        self.controller = controller
        self.db = controller.db
        
        self.title("Informe de Ventas")
        self.geometry("1100x750")
        self.grab_set()

        # Frame principal
        main_frame = tk.Frame(self, bg=COLORS['light'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        # Frame para filtros
        filtros_frame = tk.Frame(main_frame, bg=COLORS['light'], padx=10, pady=10)
        filtros_frame.pack(fill='x')

        # Selector de fecha con calendario
        tk.Label(filtros_frame, text="Fecha:", font=FONTS['body'], bg=COLORS['light']).grid(row=0, column=0, sticky='w')
        
        self.calendario = DateEntry(
            filtros_frame,
            font=FONTS['body'],
            background=COLORS['white'],
            foreground=COLORS['dark'],
            selectbackground=COLORS['primary'],
            selectforeground='white',
            normalbackground=COLORS['white'],
            weekendbackground=COLORS['light'],
            headersbackground=COLORS['light'],
            bordercolor=COLORS['border'],
            borderwidth=1,
            date_pattern='yyyy-mm-dd',
            mindate=date(2020, 1, 1),
            maxdate=date.today()
        )
        self.calendario.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Selector de vendedor
        tk.Label(filtros_frame, text="Vendedor:", font=FONTS['body'], bg=COLORS['light']).grid(row=0, column=2, padx=(20,5), sticky='w')
        
        self.vendedor_var = tk.StringVar(value="Todos")
        vendedores = ["Todos"] + [u for u, data in self.db.usuarios.items() if data['tipo'] == 'vendedor']
        combo_vendedor = ttk.Combobox(
            filtros_frame, 
            textvariable=self.vendedor_var, 
            values=vendedores, 
            font=FONTS['body'],
            state='readonly'
        )
        combo_vendedor.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        # Botón Generar Informe
        StyledButton(
            filtros_frame,
            text="Generar Informe",
            style='primary',
            command=self.generar_informe
        ).grid(row=0, column=4, padx=20, sticky='e')

        # Configurar el grid
        filtros_frame.grid_columnconfigure(4, weight=1)  # Para alinear el botón a la derecha
        
        # Frame para mostrar informe
        self.informe_frame = tk.Frame(main_frame, bg=COLORS['light'])
        self.informe_frame.pack(fill='both', expand=True, pady=(10,0))

        # Generar informe inicial
        self.generar_informe()

    def generar_informe(self):
        # Limpiar frame anterior
        for widget in self.informe_frame.winfo_children():
            widget.destroy()

        # Obtener valores de los filtros
        fecha = self.calendario.get_date()  # Obtiene la fecha como objeto date
        fecha_str = fecha.strftime('%Y-%m-%d')  # Convertir a string
        vendedor = self.vendedor_var.get()
        
        # Filtrar ventas
        ventas_filtradas = self.controller.filtrar_ventas(fecha_str, vendedor)
        
        # Mostrar mensaje si no hay ventas
        if not ventas_filtradas:
            tk.Label(
                self.informe_frame,
                text="No hay ventas para los filtros seleccionados",
                font=FONTS['title'],
                fg=COLORS['danger'],
                bg=COLORS['light']
            ).pack(pady=50)
            return

        # Separar boletas y facturas
        boletas = [v for v in ventas_filtradas if v['tipo'] == 'boleta']
        facturas = [v for v in ventas_filtradas if v['tipo'] == 'factura']

        # Título del informe
        tk.Label(
            self.informe_frame,
            text=f"INFORME DE VENTAS - {fecha_str}",
            font=('Segoe UI', 16, 'bold'),
            bg=COLORS['light']
        ).pack(pady=10)
        
        # Mostrar vendedor si no es "Todos"
        if vendedor != "Todos":
            tk.Label(
                self.informe_frame,
                text=f"Vendedor: {vendedor}",
                font=FONTS['body'],
                bg=COLORS['light']
            ).pack(pady=5)

        # Frame de resumen
        resumen_frame = tk.LabelFrame(
            self.informe_frame,
            text="RESUMEN",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['light'],
            padx=10,
            pady=10
        )
        resumen_frame.pack(fill='x', pady=10)
        
        # Resumen de boletas
        if boletas:
            total_b = sum(v['total'] for v in boletas)
            tk.Label(
                resumen_frame,
                text=f"Boletas: {len(boletas)} | Total: ${total_b:,.0f}",
                font=FONTS['body'],
                bg=COLORS['light']
            ).pack(anchor='w')
        
        # Resumen de facturas
        if facturas:
            total_f = sum(v['total'] for v in facturas)
            tk.Label(
                resumen_frame,
                text=f"Facturas: {len(facturas)} | Total: ${total_f:,.0f}",
                font=FONTS['body'],
                bg=COLORS['light']
            ).pack(anchor='w')

        # Detalle de facturas (si existen)
        if facturas:
            detalle_frame = tk.LabelFrame(
                self.informe_frame,
                text="DETALLE DE FACTURAS",
                font=('Segoe UI', 12, 'bold'),
                bg=COLORS['light']
            )
            detalle_frame.pack(fill='both', expand=True, pady=10)
            
            # Crear Treeview
            cols = ('Número', 'Cliente', 'Subtotal', 'IVA', 'Total')
            tree = ttk.Treeview(detalle_frame, columns=cols, show='headings', style="Treeview")
            
            # Configurar columnas
            for col in cols: 
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor='center')
            
            tree.column('Cliente', width=200)
            
            # Insertar datos
            for f in facturas:
                cliente = f['cliente']['razon_social'] if f['cliente'] else 'N/A'
                tree.insert('', 'end', values=(
                    f['numero'],
                    cliente,
                    f"${f['subtotal']:,.0f}",
                    f"${f['iva']:,.0f}",
                    f"${f['total']:,.0f}"
                ))
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(detalle_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Empaquetar
            tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
            scrollbar.pack(side='right', fill='y')

        # Botón Exportar PDF
        def exportar_y_cerrar():
            if self.controller.exportar_informe_pdf(fecha_str, vendedor, ventas_filtradas):
                self.destroy()
            else:
                tk.messagebox.showerror("Error", "No se pudo exportar el informe PDF")

        StyledButton(
            self.informe_frame,
            text="Exportar Informe PDF", 
            style='warning',
            command=exportar_y_cerrar
        ).pack(pady=20)
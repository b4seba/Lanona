# pos_app.py

import tkinter as tk
from tkinter import ttk, simpledialog
from datetime import datetime, date

from database import Database
from styles import COLORS, FONTS
import pdf_generator
from ui_components import MessageDialog # <--- Usamos el nuevo MessageDialog

from views.login_view import LoginView
from views.jefe_view import JefeView
from views.vendedor_view import VendedorView
from views.informe_view import InformeView
from views.agregar_producto_view import AgregarProductoView

class PuntoVentaApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        
        self.usuario_actual = None
        self.tipo_usuario = None
        self.venta_actual = []
        self.productos_encontrados = []
        self.current_view = None

        self.setup_main_window()
        self.mostrar_vista(LoginView)

    def setup_main_window(self):
        self.root.title("Sistema POS - Los Monitos de la Nona")
        self.root.geometry("1280x720")
        self.root.configure(bg=COLORS['light'])
        
        # Configurar estilos de ttk para Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=COLORS['white'],
                        foreground=COLORS['dark'],
                        rowheight=25,
                        fieldbackground=COLORS['white'],
                        font=FONTS['body'])
        style.configure("Treeview.Heading",
                        font=FONTS['button'],
                        background=COLORS['primary'],
                        foreground=COLORS['white'],
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#0056b3')])
        style.map("Treeview",
                  background=[('selected', COLORS['primary'])],
                  foreground=[('selected', COLORS['white'])])

    def mostrar_vista(self, ViewClass):
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = ViewClass(self.root, self)
        self.current_view.pack(fill="both", expand=True)
    
    # --- Lógica de Autenticación y Navegación ---
    def login(self, usuario, password):
        if usuario in self.db.usuarios and self.db.usuarios[usuario]['password'] == password:
            self.usuario_actual = usuario
            self.tipo_usuario = self.db.usuarios[usuario]['tipo']
            if self.tipo_usuario == 'jefe':
                self.mostrar_vista(JefeView)
            else:
                hoy = str(date.today())
                if hoy not in self.db.dias_abiertos or self.db.dias_abiertos[hoy]['estado'] != 'abierto':
                    MessageDialog.show_error(self.root, "Día Cerrado", "No hay un día abierto para realizar ventas.")
                    self.logout()
                else:
                    self.mostrar_vista(VendedorView)
        else:
            MessageDialog.show_error(self.root, "Error de Acceso", "Usuario o contraseña incorrectos.")

    def logout(self):
        self.usuario_actual = None
        self.tipo_usuario = None
        self.mostrar_vista(LoginView)

    # --- Lógica del Jefe ---
    def agregar_producto(self):
        # La lógica de la ventana de diálogo puede permanecer aquí por simplicidad
        # TODO: Refactorizar a un diálogo con StyledComponents
       
        AgregarProductoView(self.root, self)
    
    def abrir_dia(self):
        hoy = str(date.today())
        if hoy in self.db.dias_abiertos and self.db.dias_abiertos[hoy]['estado'] == 'abierto':
            MessageDialog.show_info(self.root, "Advertencia", "El día ya está abierto.")
            return
        self.db.dias_abiertos[hoy] = {'estado': 'abierto', 'fecha_apertura': datetime.now().isoformat(), 'ventas': []}
        self.db.save_data()
        MessageDialog.show_success(self.root, "Éxito", f"Día {hoy} abierto correctamente.")

    def cerrar_dia(self):
        hoy = str(date.today())
        if hoy not in self.db.dias_abiertos or self.db.dias_abiertos[hoy]['estado'] == 'cerrado':
            MessageDialog.show_info(self.root, "Advertencia", "El día no está abierto o ya fue cerrado.")
            return
        self.db.dias_abiertos[hoy]['estado'] = 'cerrado'
        self.db.dias_abiertos[hoy]['fecha_cierre'] = datetime.now().isoformat()
        self.db.save_data()
        MessageDialog.show_success(self.root, "Éxito", f"Día {hoy} cerrado correctamente.")

    def mostrar_informes(self):
        InformeView(self.root, self)

    def filtrar_ventas(self, fecha, vendedor):
        if fecha not in self.db.ventas:
            return []
        ventas_dia = self.db.ventas[fecha]
        if vendedor != "Todos":
            return [v for v in ventas_dia if v['vendedor'] == vendedor]
        return ventas_dia

    def exportar_informe_pdf(self, fecha, vendedor, ventas):
        pdf_generator.exportar_informe_pdf(fecha, vendedor, ventas)
        MessageDialog.show_success(self.root, "Éxito", "Informe PDF exportado correctamente.")

    # --- Lógica del Vendedor ---
    def buscar_producto(self):
        termino = self.current_view.search_entry.get_value().lower()
        if not termino: return
        
        self.current_view.productos_listbox.delete(0, 'end')
        self.productos_encontrados.clear()
        
        for codigo, producto in self.db.productos.items():
            if termino in codigo.lower() or termino in producto['nombre'].lower():
                texto = f"{codigo} - {producto['nombre']} - ${producto['precio']}"
                self.current_view.productos_listbox.insert('end', texto)
                self.productos_encontrados.append(codigo)

    def agregar_a_venta(self):
        try:
            indice = self.current_view.productos_listbox.curselection()[0]
        except IndexError:
            MessageDialog.show_info(self.root, "Sin Selección", "Seleccione un producto de la lista.")
            return
        
        codigo_producto = self.productos_encontrados[indice]
        producto = self.db.productos[codigo_producto]
        
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad para:\n{producto['nombre']}", minvalue=1, parent=self.root)
        if not cantidad: return

        for item in self.venta_actual:
            if item['codigo'] == codigo_producto:
                item['cantidad'] += cantidad
                item['total'] = item['cantidad'] * item['precio']
                self.actualizar_vista_venta()
                return

        self.venta_actual.append({
            'codigo': codigo_producto, 'nombre': producto['nombre'],
            'precio': producto['precio'], 'cantidad': cantidad,
            'total': cantidad * producto['precio']
        })
        self.actualizar_vista_venta()

    def actualizar_vista_venta(self):
        tree = self.current_view.venta_tree
        tree.delete(*tree.get_children())
        
        subtotal = 0
        for item in self.venta_actual:
            tree.insert('', 'end', values=(
                item['cantidad'], item['codigo'], item['nombre'],
                f"${item['precio']:,.0f}", f"${item['total']:,.0f}"
            ))
            subtotal += item['total']
        
        iva = subtotal * 0.19
        total = subtotal + iva
        
        self.current_view.label_subtotal.config(text=f"Subtotal: ${subtotal:,.0f}")
        self.current_view.label_iva.config(text=f"IVA (19%): ${iva:,.0f}")
        self.current_view.label_total.config(text=f"Total: ${total:,.0f}")

    def limpiar_venta(self):
        self.venta_actual = []
        self.actualizar_vista_venta()

    def generar_documento(self, tipo, cliente_data=None):
        if not self.venta_actual:
            MessageDialog.show_info(self.root, "Venta Vacía", "No hay productos en la venta.")
            return
        
        # Validación adicional para facturas
        if tipo == 'factura':
            if not cliente_data:
                MessageDialog.show_error(self.root, "Datos Faltantes", "Se requieren datos del cliente para generar una factura.")
                return
            if not cliente_data.get('rut') or not cliente_data.get('razon_social'):
                MessageDialog.show_error(self.root, "Datos Incompletos", "RUT y Razón Social son obligatorios para factura.")
                return
        
        # Cálculo de totales
        subtotal = sum(item['total'] for item in self.venta_actual)
        iva = subtotal * 0.19
        total = subtotal + iva
        
        # Preparación de datos para el PDF
        venta = {
            'numero': self._generar_numero_documento(tipo),
            'tipo': tipo,
            'fecha': datetime.now().isoformat(),
            'vendedor': self.usuario_actual,
            'productos': self.venta_actual.copy(),
            'subtotal': subtotal,
            'iva': iva,
            'total': total,
            'cliente': cliente_data if tipo == 'factura' else None
        }
        
        # Guardar en la base de datos
        hoy = str(date.today())
        if hoy not in self.db.ventas:
            self.db.ventas[hoy] = []
        self.db.ventas[hoy].append(venta)
        self.db.save_data()
        
        # Generar PDF
        pdf_generator.generar_pdf_documento(venta)
        
        # Limpiar venta actual
        self.limpiar_venta()
        MessageDialog.show_success(self.root, "Éxito", f"{tipo.capitalize()} generada correctamente.")

    def _generar_numero_documento(self, tipo):
        hoy = str(date.today())
        if hoy not in self.db.ventas: return f"{tipo.upper()}-{hoy}-001"
        contador = len([v for v in self.db.ventas[hoy] if v['tipo'] == tipo]) + 1
        return f"{tipo.upper()}-{hoy}-{contador:03d}"

    def _solicitar_datos_cliente(self):
        # Esta función debería ser refactorizada para usar un diálogo personalizado
        # con StyledComponents para mantener la consistencia visual.
        # Por ahora, se mantiene la lógica original.
        return {} # Placeholder
import tkinter as tk
from tkinter import ttk, messagebox
from styles import COLORS, FONTS
from ui_components import StyledFrame, StyledLabel, StyledEntry, StyledButton

class ClienteDialog:
    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Datos del Cliente - Factura")
        self.dialog.geometry("420x540")  # Más alto y un poco más ancho
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLORS['light'])

        # Hacer la ventana modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Centrar la ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (420 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (540 // 2)
        self.dialog.geometry(f"420x540+{x}+{y}")

        # --- Scrollable Frame ---
        canvas = tk.Canvas(self.dialog, bg=COLORS['light'], highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.scrollable_frame = StyledFrame(canvas, style='main', padx=10, pady=10)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self._create_widgets()

        # Enfocar el primer campo
        self.rut_entry.focus_set()

        # Manejar el cierre de la ventana
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancelar)

    def _create_widgets(self):
        # Título
        title_frame = StyledFrame(self.scrollable_frame, style='main')
        title_frame.pack(fill='x', pady=(0, 20))

        StyledLabel(title_frame, "Ingrese los Datos del Cliente", style='title').pack()
        StyledLabel(title_frame, "Los campos marcados con * son obligatorios",
                    style='body', fg=COLORS['gray']).pack(pady=(5, 0))

        # Frame para los campos
        fields_frame = StyledFrame(self.scrollable_frame, style='card', padx=20, pady=20)
        fields_frame.pack(fill='x', pady=(0, 20))

        # Campo RUT
        StyledLabel(fields_frame, "RUT: *", style='body').pack(anchor='w')
        self.rut_entry = StyledEntry(fields_frame, placeholder="12.345.678-9")
        self.rut_entry.pack(fill='x', pady=(2, 5), ipady=6)
        self.rut_entry.bind('<KeyRelease>', self._format_rut)

        # Texto de ayuda para el RUT
        StyledLabel(fields_frame, "Se formateará automáticamente",
                    style='small').pack(anchor='w', pady=(0, 10))

        # Campo Razón Social
        StyledLabel(fields_frame, "Razón Social: *", style='body').pack(anchor='w')
        self.razon_social_entry = StyledEntry(fields_frame, placeholder="Nombre de la empresa")
        self.razon_social_entry.pack(fill='x', pady=(2, 10), ipady=6)

        # Campo Giro
        StyledLabel(fields_frame, "Giro:", style='body').pack(anchor='w')
        self.giro_entry = StyledEntry(fields_frame, placeholder="Actividad comercial")
        self.giro_entry.pack(fill='x', pady=(2, 10), ipady=6)

        # Campo Dirección
        StyledLabel(fields_frame, "Dirección:", style='body').pack(anchor='w')
        self.direccion_entry = StyledEntry(fields_frame, placeholder="Dirección completa")
        self.direccion_entry.pack(fill='x', pady=(2, 10), ipady=6)

        # Campo Email
        StyledLabel(fields_frame, "Email:", style='body').pack(anchor='w')
        self.email_entry = StyledEntry(fields_frame, placeholder="correo@empresa.cl")
        self.email_entry.pack(fill='x', pady=(2, 0), ipady=6)

        # Frame para botones
        buttons_frame = StyledFrame(self.scrollable_frame, style='main')
        buttons_frame.pack(fill='x', pady=(10, 0))

        # Botones
        StyledButton(buttons_frame, "Cancelar", style='secondary',
                     command=self._cancelar, padx=20, pady=8).pack(side='right', padx=(10, 0))
        StyledButton(buttons_frame, "Confirmar y Generar Factura", style='success',
                     command=self._confirmar, padx=20, pady=8).pack(side='right')

        # Bind Enter para confirmar
        self.dialog.bind('<Return>', lambda e: self._confirmar())
        self.dialog.bind('<Escape>', lambda e: self._cancelar())

    # ...el resto de tus métodos (sin cambios)...
    def _format_rut(self, event=None):
        current_text = self.rut_entry.get()
        current_pos = self.rut_entry.index(tk.INSERT)
        clean_rut = current_text.replace('.', '').replace('-', '')
        if len(clean_rut) > 1 and clean_rut != "123456789":
            if len(clean_rut) >= 2:
                numeros = clean_rut[:-1]
                dv = clean_rut[-1]
                if len(numeros) > 3:
                    formatted_nums = ""
                    for i, digit in enumerate(reversed(numeros)):
                        if i > 0 and i % 3 == 0:
                            formatted_nums = "." + formatted_nums
                        formatted_nums = digit + formatted_nums
                else:
                    formatted_nums = numeros
                formatted_rut = formatted_nums + "-" + dv
                if current_text != formatted_rut:
                    self.rut_entry.delete(0, tk.END)
                    self.rut_entry.insert(0, formatted_rut)
                    self.rut_entry.icursor(len(formatted_rut))

    def _validar_rut(self, rut):
        if not rut:
            return False
        rut_clean = rut.replace('.', '').replace('-', '')
        if len(rut_clean) < 8 or len(rut_clean) > 9:
            return False
        numeros = rut_clean[:-1]
        dv = rut_clean[-1].upper()
        if not numeros.isdigit():
            return False
        if dv not in '0123456789K':
            return False
        return True

    def _validar_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _confirmar(self):
        rut = self.rut_entry.get().strip()
        razon_social = self.razon_social_entry.get().strip()
        giro = self.giro_entry.get().strip()
        direccion = self.direccion_entry.get().strip()
        email = self.email_entry.get().strip()
        if not rut:
            messagebox.showwarning("Campo obligatorio", "El RUT es obligatorio", parent=self.dialog)
            self.rut_entry.focus_set()
            return
        if not self._validar_rut(rut):
            messagebox.showwarning("RUT inválido", "Por favor ingrese un RUT válido", parent=self.dialog)
            self.rut_entry.focus_set()
            return
        if not razon_social:
            messagebox.showwarning("Campo obligatorio", "La Razón Social es obligatoria", parent=self.dialog)
            self.razon_social_entry.focus_set()
            return
        if email and not self._validar_email(email):
            messagebox.showwarning("Email inválido", "Por favor ingrese un email válido", parent=self.dialog)
            self.email_entry.focus_set()
            return
        self.result = {
            'rut': rut,
            'razon_social': razon_social,
            'giro': giro if giro else "Sin especificar",
            'direccion': direccion if direccion else "Sin especificar",
            'email': email if email else ""
        }
        self.dialog.destroy()

    def _cancelar(self):
        self.result = None
        self.dialog.destroy()

    def show(self):
        self.dialog.wait_window()
        return self.result

    def get_cliente_data(self):
        return self.result
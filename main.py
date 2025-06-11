# main.py

import tkinter as tk
import subprocess
import sys

# --- Verificación de Dependencias ---
def check_dependencies():
    try:
        import reportlab
    except ImportError:
        print("Dependencia 'reportlab' no encontrada. Instalando...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
            print("'reportlab' instalado correctamente.")
        except Exception as e:
            print(f"Error al instalar 'reportlab': {e}")
            sys.exit(1)

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    check_dependencies()
    
    # Importar la app después de verificar dependencias
    from pos_app import PuntoVentaApp

    # Crear la ventana raíz y la aplicación
    root = tk.Tk()
    app = PuntoVentaApp(root)
    
    # Iniciar el bucle principal de la GUI
    root.mainloop()
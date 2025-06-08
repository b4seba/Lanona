import tkinter as tk
from auth_manager import AuthManager
from ui_components import MessageDialog
from ventana_Jefe import ventana_Jefe

class LoginManager:
    def __init__(self):
        self.auth = AuthManager()
    
    def login_jefe(self, usuario, clave, root):
        # validacion de credenciales
        result = self.auth.validar_usuario(usuario, clave)
        
        if not result['success']:
            MessageDialog.show_error(root, "Error de Login", result['message'])
            return False
        
        # Verificar que sea jefe
        if not self.auth.es_jefe(usuario):
            MessageDialog.show_error(root, "Acceso Denegado", 
                                   "Solo el jefe puede abrir la caja.")
            return False
        

        MessageDialog.show_success(root, "Login Exitoso", 
                                 f"Bienvenido, {result['user']['nombre']}")

        root.after(1000, lambda: self._abrir_ventana_jefe(result['user'], root))
        return True
    
    def _abrir_ventana_jefe(self, user_data, root):
        try:
            ventana_Jefe(user_data, root)
        except Exception as e:
            MessageDialog.show_error(root, "Error", f"Error al abrir panel del jefe: {str(e)}")

def LoginWindow(usuario, clave, root):
    login_manager = LoginManager()
    return login_manager.login_jefe(usuario, clave, root)

def error_login(root, mensaje):
    MessageDialog.show_error(root, "Error de Login", mensaje)
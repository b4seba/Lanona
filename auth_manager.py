import json
import os
from pathlib import Path

class AuthManager:
    def __init__(self):
        self.usuarios_file = Path("usuarios.json")
        self.usuarios = self.cargar_usuarios()
    
    def cargar_usuarios(self):
        try:
            if self.usuarios_file.exists():
                with open(self.usuarios_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('usuarios', {})
            else:
                # Crear json si es que no existe
                usuarios_default = {
                    "usuarios": {
                        "jefeVentas": {
                            "password": "12345",
                            "role": "jefe",
                            "nombre": "Jefe de Ventas"
                        },
                        "vendedor": {
                            "password": "1234", 
                            "role": "vendedor",
                            "nombre": "Vendedor"
                        }
                    }
                }
                self.guardar_usuarios(usuarios_default)
                return usuarios_default['usuarios']
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")
            return {}
    
    def guardar_usuarios(self, data):
   
        try:
            with open(self.usuarios_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")
    
    def validar_usuario(self, username, password):
        
        if username in self.usuarios:
            user_data = self.usuarios[username]
            if user_data['password'] == password:
                return {
                    'success': True,
                    'user': {
                        'username': username,
                        'role': user_data['role'],
                        'nombre': user_data['nombre']
                    }
                }
        
        return {
            'success': False,
            'message': 'Credenciales incorrectas'
        }
    
    def es_jefe(self, username):
        if username in self.usuarios:
            return self.usuarios[username]['role'] == 'jefe'
        return False
    
    def es_vendedor(self, username):
        if username in self.usuarios:
            return self.usuarios[username]['role'] == 'vendedor'
        return False
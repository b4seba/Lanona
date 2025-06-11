# database.py

import json
import os

class Database:
    def __init__(self):
        self.data_file = "pos_data.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.usuarios = data.get('usuarios', {})
                self.productos = data.get('productos', {})
                self.ventas = data.get('ventas', {})
                self.dias_abiertos = data.get('dias_abiertos', {})
        else:
            self.usuarios = {
                'admin': {'password': 'admin123', 'tipo': 'jefe'},
                'vendedor1': {'password': 'vend123', 'tipo': 'vendedor'}
            }
            self.productos = {
                'P001': {'nombre': 'Cuaderno Pro', 'precio': 1500, 'sku': 'P001'},
                'P002': {'nombre': 'Lápiz Grafito HB', 'precio': 300, 'sku': 'P002'},
                'P003': {'nombre': 'Goma de Borrar', 'precio': 200, 'sku': 'P003'}
            }
            self.ventas = {}
            self.dias_abiertos = {}
            self.save_data()
    
    def save_data(self):
        data = {
            'usuarios': self.usuarios,
            'productos': self.productos,
            'ventas': self.ventas,
            'dias_abiertos': self.dias_abiertos
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
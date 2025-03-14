import json
import os
from productos import Producto

class Inventario:
    def __init__(self, archivo):
        self.archivo = archivo
        self.productos = self.cargar_inventario()

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_inventario()

    def mostrar_inventario(self):
        for producto in self.productos:
            print(producto)

    def guardar_inventario(self):
        with open(self.archivo, 'w') as f:
            json.dump([producto.to_dict() for producto in self.productos], f, indent=4)

    def cargar_inventario(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                try:
                    return [Producto.from_dict(data) for data in json.load(f)]
                except json.JSONDecodeError:
                    return []
        return []

# Creación de directorio y archivo de inventario si no existen
os.makedirs('datos', exist_ok=True)
if not os.path.exists('datos/inventario.json'):
    with open('datos/inventario.json', 'w') as f:
        json.dump([], f)

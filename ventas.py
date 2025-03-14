import json
import os

class Venta:
    def __init__(self, archivo):
        self.archivo = archivo
        self.carrito = []
        self.ventas = self.cargar_ventas()

    def agregar_producto(self, producto, cantidad):
        if producto.cantidad >= cantidad:
            self.carrito.append((producto, cantidad))
            producto.cantidad -= cantidad
        else:
            print("Cantidad no disponible")

    def finalizar_venta(self):
        total = sum(producto.precio * cantidad for producto, cantidad in self.carrito)
        self.ventas.append(self.carrito)
        self.guardar_ventas()
        self.carrito = []
        print(f'Total a pagar: ${total:.2f}')

    def guardar_ventas(self):
        with open(self.archivo, 'w') as f:
            json.dump(self.ventas, f, indent=4)

    def cargar_ventas(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

# Creación de archivo de ventas si no existe
os.makedirs('datos', exist_ok=True)
if not os.path.exists('datos/ventas.json'):
    with open('datos/ventas.json', 'w') as f:
        json.dump([], f)

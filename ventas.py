import json

class Venta:
    def __init__(self, archivo_ventas):
        self.archivo_ventas = archivo_ventas
        self.ventas = []

    def agregar_producto(self, producto, cantidad):
        # Convierte el producto en un diccionario para almacenarlo
        self.ventas.append({
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": cantidad,
            "total": producto.precio * cantidad
        })

    def calcular_total(self):
        return sum(venta['total'] for venta in self.ventas)

    def finalizar_venta(self):
        # Guarda la venta actual en el archivo y limpia el registro de ventas
        self.guardar_ventas()
        self.ventas = []

    def guardar_ventas(self):
        try:
            with open(self.archivo_ventas, 'w', encoding='utf-8') as f:
                json.dump(self.ventas, f, indent=4)  # Se asegura que todo sea serializable
            print("Ventas guardadas exitosamente.")
        except Exception as e:
            print(f"Error al guardar las ventas: {e}")

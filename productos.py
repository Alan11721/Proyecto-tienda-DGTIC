class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return f'{self.nombre} - ${self.precio:.2f} ({self.cantidad} disponibles)'

    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['codigo'], data['nombre'], data['precio'], data['cantidad'])

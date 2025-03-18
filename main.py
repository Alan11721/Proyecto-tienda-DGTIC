import os
import sqlite3

# Clase para gestionar la conexión y operaciones con SQLite
class Database:
    def __init__(self, db_path):
        print(f"Intentando conectar a la base de datos en {db_path}")
        self.conexion = sqlite3.connect(db_path)
        print("Conexión exitosa.")
        self.cursor = self.conexion.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        # Tabla para productos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL
            )
        ''')
        # Tabla para ventas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        self.conexion.commit()

    def insertar_producto(self, codigo, nombre, precio, cantidad):
        try:
            self.cursor.execute('''
                INSERT INTO productos (codigo, nombre, precio, cantidad) 
                VALUES (?, ?, ?, ?)
            ''', (codigo, nombre, precio, cantidad))
            self.conexion.commit()
            print("Producto agregado exitosamente.")
        except sqlite3.IntegrityError:
            print("El código del producto ya existe. Intente con otro.")

    def mostrar_inventario(self):
        self.cursor.execute('SELECT * FROM productos')
        productos = self.cursor.fetchall()
        if productos:
            for p in productos:
                print(f"ID: {p[0]}, Código: {p[1]}, Nombre: {p[2]}, Precio: ${p[3]:.2f}, Cantidad: {p[4]}")
        else:
            print("El inventario está vacío.")

    def actualizar_stock(self, producto_id, cantidad_vendida):
        self.cursor.execute('''
            UPDATE productos 
            SET cantidad = cantidad - ? 
            WHERE id = ?
        ''', (cantidad_vendida, producto_id))
        self.conexion.commit()

    def registrar_venta(self, producto_id, cantidad, total):
        self.cursor.execute('''
            INSERT INTO ventas (producto_id, cantidad, total) 
            VALUES (?, ?, ?)
        ''', (producto_id, cantidad, total))
        self.conexion.commit()

# Funciones auxiliares
def imprimir_titulo(titulo):
    borde = "=" * (len(titulo) + 4)
    print("\n" + borde)
    print(f"| {titulo} |")
    print(borde + "\n")

def realizar_venta(db):
    imprimir_titulo("REGISTRO DE VENTA")
    db.mostrar_inventario()

    try:
        producto_id = int(input("Ingrese el ID del producto: "))
        cantidad = int(input("Cantidad: "))
        db.cursor.execute('SELECT precio, cantidad FROM productos WHERE id = ?', (producto_id,))
        producto = db.cursor.fetchone()

        if producto and producto[1] >= cantidad:  # Verifica stock disponible
            total = producto[0] * cantidad
            db.registrar_venta(producto_id, cantidad, total)
            db.actualizar_stock(producto_id, cantidad)
            print(f"Venta realizada con éxito. Total: ${total:.2f}")
        else:
            print("Stock insuficiente o producto no encontrado.")
    except ValueError:
        print("Entrada inválida. Intente de nuevo.")

def menu_principal():
    db = Database('datos/tienda.db')

    while True:
        imprimir_titulo("MENÚ PRINCIPAL")
        print("1. Mostrar Inventario")
        print("2. Agregar Producto al Inventario")
        print("3. Realizar Venta")
        print("4. Salir")
        print("=" * 20)

        opcion = input("Seleccione una opción: ").strip()
        if opcion == '1':
            imprimir_titulo("INVENTARIO")
            db.mostrar_inventario()
        elif opcion == '2':
            imprimir_titulo("AGREGAR PRODUCTO")
            codigo = input("Código: ")
            nombre = input("Nombre: ")
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))
            db.insertar_producto(codigo, nombre, precio, cantidad)
        elif opcion == '3':
            realizar_venta(db)
        elif opcion == '4':
            imprimir_titulo("SALIDA")
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    if not os.path.exists('datos'):
        os.makedirs('datos')
    menu_principal()

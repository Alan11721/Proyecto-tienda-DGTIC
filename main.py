import os
import sqlite3
from tabulate import tabulate

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
            headers = ["ID", "Código", "Nombre", "Precio", "Cantidad"]
            tabla = [[p[0], p[1], p[2], f"${p[3]:.2f}", p[4]] for p in productos]
            print(tabulate(tabla, headers, tablefmt="grid"))
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

    def editar_producto(self, producto_id, nuevo_nombre, nuevo_precio, nueva_cantidad):
        self.cursor.execute('''
            UPDATE productos 
            SET nombre = ?, precio = ?, cantidad = ?
            WHERE id = ?
        ''', (nuevo_nombre, nuevo_precio, nueva_cantidad, producto_id))
        self.conexion.commit()

# Función para imprimir un título con bordes decorativos
def imprimir_titulo(titulo):
    borde = "=" * (len(titulo) + 4)
    print("\n" + borde)
    print(f"| {titulo} |")
    print(borde + "\n")

# Módulo para realizar el corte de caja
def corte_de_caja(db):
    imprimir_titulo("CORTE DE CAJA")
    db.cursor.execute('SELECT total FROM ventas')  # Suma el total de todas las ventas
    ventas = db.cursor.fetchall()
    total_ventas = sum(v[0] for v in ventas)

    print(f"Total de ventas registradas: ${total_ventas:.2f}")
    input("\nPresiona Enter para regresar al menú principal...")

# Módulo de ventas modificado para aceptar múltiples productos por venta
def realizar_venta(db):
    imprimir_titulo("REGISTRO DE VENTA")
    productos_vendidos = []
    total_venta = 0

    while True:
        db.mostrar_inventario()
        opcion = input("Ingrese el ID del producto que desea agregar a la venta, 'finalizar' para terminar, o 'salir' para regresar al menú principal: ").strip()

        if opcion.lower() == "finalizar":
            break
        elif opcion.lower() == "salir":
            print("Saliendo al menú principal...")
            return

        try:
            producto_id = int(opcion)
            cantidad = int(input("Cantidad: "))
            db.cursor.execute('SELECT precio, cantidad FROM productos WHERE id = ?', (producto_id,))
            producto = db.cursor.fetchone()

            if producto and producto[1] >= cantidad:
                total_producto = producto[0] * cantidad
                productos_vendidos.append((producto_id, cantidad, total_producto))
                total_venta += total_producto
                print(f"Producto agregado. Total parcial: ${total_venta:.2f}")
            else:
                print("Stock insuficiente o producto no encontrado.")
        except ValueError:
            print("Entrada inválida. Intente de nuevo.")

    if productos_vendidos:
        print(f"\nTotal de la venta: ${total_venta:.2f}")
        while True:
            try:
                recibido = float(input("Monto recibido: "))
                if recibido >= total_venta:
                    cambio = recibido - total_venta
                    print(f"Cambio: ${cambio:.2f}")
                    print("Venta realizada con éxito. Gracias por su compra.")
                    for producto_id, cantidad, total_producto in productos_vendidos:
                        db.registrar_venta(producto_id, cantidad, total_producto)
                        db.actualizar_stock(producto_id, cantidad)
                    break
                else:
                    print("El monto recibido es insuficiente. Intente nuevamente.")
            except ValueError:
                print("Por favor, ingrese una cantidad válida.")
    else:
        print("No se realizó ninguna venta.")

# Módulo para editar productos en el inventario
def editar_inventario(db):
    imprimir_titulo("EDITAR INVENTARIO")
    db.mostrar_inventario()

    try:
        producto_id = int(input("Ingrese el ID del producto que desea modificar: "))
        db.cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        producto = db.cursor.fetchone()

        if producto:
            print(f"\nProducto seleccionado: {producto[2]} (Código: {producto[1]}, Precio: ${producto[3]:.2f}, Existencias: {producto[4]})")
            nuevo_nombre = input("Nuevo nombre (presiona Enter para no modificar): ").strip()
            nuevo_precio = input("Nuevo precio (presiona Enter para no modificar): ").strip()
            nueva_cantidad = input("Nueva cantidad (presiona Enter para no modificar): ").strip()

            nuevo_nombre = nuevo_nombre if nuevo_nombre else producto[2]
            nuevo_precio = float(nuevo_precio) if nuevo_precio else producto[3]
            nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else producto[4]

            db.editar_producto(producto_id, nuevo_nombre, nuevo_precio, nueva_cantidad)
            print("Producto actualizado exitosamente.")
        else:
            print("Producto no encontrado.")
    except ValueError:
        print("Entrada inválida. Intente de nuevo.")

# Menú principal modificado para incluir la opción de corte de caja
def menu_principal():
    db = Database('datos/tienda.db')

    while True:
        imprimir_titulo("MENÚ PRINCIPAL")
        print("1. Mostrar Inventario")
        print("2. Agregar Producto al Inventario")
        print("3. Realizar Venta")
        print("4. Editar Inventario")
        print("5. Corte de Caja")
        print("6. Salir")
        print("=" * 20)

        opcion = input("Seleccione una opción: ").strip()
        if opcion == '1':
            imprimir_titulo("INVENTARIO")
            db.mostrar_inventario()
            input("\nPresiona Enter para regresar al menú principal...")
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
            editar_inventario(db)
        elif opcion == '5':
            corte_de_caja(db)
        elif opcion == '6':
            imprimir_titulo("SALIDA")
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecución principal
if __name__ == "__main__":
    if not os.path.exists('datos'):
        os.makedirs('datos')  # Crea la carpeta "datos" si no existe
    menu_principal()  # Llama al menú principal para iniciar el programa


import os
import sqlite3
from tabulate import tabulate
from datetime import datetime

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
                producto_id TEXT NOT NULL,
                nombre_producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                total REAL NOT NULL,
                fecha_hora TEXT,
                ticket_id INTEGER
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

    def actualizar_stock(self, codigo, cantidad_vendida):
        self.cursor.execute('''
            UPDATE productos 
            SET cantidad = cantidad - ? 
            WHERE codigo = ?
        ''', (cantidad_vendida, codigo))
        self.conexion.commit()

    def registrar_venta(self, codigo, nombre, cantidad, total, ticket_id):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO ventas (producto_id, nombre_producto, cantidad, total, fecha_hora, ticket_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (codigo, nombre, cantidad, total, fecha_hora, ticket_id))
        self.conexion.commit()

    def obtener_ventas_por_ticket(self):
        # Obtener todas las ventas agrupadas por ticket_id
        self.cursor.execute('''
            SELECT ticket_id, fecha_hora, SUM(total) AS total_ticket, 
                   GROUP_CONCAT(nombre_producto || " (x" || cantidad || ")", ", ") AS productos
            FROM ventas
            GROUP BY ticket_id
        ''')
        return self.cursor.fetchall()

# Función para imprimir un título con bordes decorativos
def imprimir_titulo(titulo):
    borde = "=" * (len(titulo) + 4)
    print("\n" + borde)
    print(f"| {titulo} |")
    print(borde + "\n")

# Módulo para realizar el corte de caja
def corte_de_caja(db):
    imprimir_titulo("CORTE DE CAJA")
    ventas = db.obtener_ventas_por_ticket()
    total_ventas = sum(v[2] for v in ventas)

    if ventas:
        headers = ["Ticket ID", "Fecha y Hora", "Total", "Productos"]
        tabla = [[v[0], v[1], f"${v[2]:.2f}", v[3]] for v in ventas]
        print(tabulate(tabla, headers, tablefmt="grid"))
        print(f"\nTotal de ventas: ${total_ventas:.2f}")
    else:
        print("No hay ventas registradas.")

    while True:
        print("\nOpciones:")
        print("1. Guardar corte de caja e iniciar uno nuevo")
        print("2. Salir y continuar usando el corte actual")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            archivo = f"corte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(archivo, 'w') as f:
                f.write(f"Corte de caja:\n")
                for v in ventas:
                    f.write(f"Ticket ID: {v[0]}, Fecha: {v[1]}, Total: ${v[2]:.2f}, Productos: {v[3]}\n")
                f.write(f"\nTotal de ventas: ${total_ventas:.2f}\n")
            print(f"Corte de caja guardado como {archivo}.")
            db.cursor.execute('DELETE FROM ventas')  # Inicia un nuevo corte de caja borrando las ventas actuales
            db.conexion.commit()
            print("Se ha iniciado un nuevo corte de caja.")
            break
        elif opcion == "2":
            print("Continuando con el corte actual...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Módulo de ventas mejorado
def realizar_venta(db):
    ticket_id = int(datetime.now().timestamp())  # Generar un ID único para el ticket
    while True:
        imprimir_titulo("REGISTRO DE VENTA")
        productos_vendidos = []
        total_venta = 0

        while True:
            print("\nOpciones:")
            print("1. Ver Inventario")
            print("2. Escanear Producto")
            print("3. Borrar Producto Añadido")
            print("4. Finalizar Venta")
            print("5. Salir al Menú Principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                db.mostrar_inventario()
            elif opcion == "2":
                try:
                    codigo_barras = input("Ingrese el código de barras del producto (o 'fin' para terminar): ").strip()
                    if codigo_barras.lower() == 'fin':
                        break

                    cantidad = int(input("Cantidad: "))
                    db.cursor.execute('SELECT nombre, precio, cantidad FROM productos WHERE codigo = ?', (codigo_barras,))
                    producto = db.cursor.fetchone()

                    if producto and producto[2] >= cantidad:
                        nombre_producto = producto[0]
                        precio_producto = producto[1]
                        total_producto = precio_producto * cantidad
                        productos_vendidos.append((codigo_barras, nombre_producto, cantidad, total_producto))
                        total_venta += total_producto
                        print(f"Producto agregado: {nombre_producto} (x{cantidad}). Total parcial: ${total_venta:.2f}")
                    else:
                        print("Stock insuficiente o producto no encontrado.")
                except ValueError:
                    print("Entrada inválida. Intente de nuevo.")
            elif opcion == "3":
                if not productos_vendidos:
                    print("No hay productos para borrar.")
                    continue

                print("\nProductos añadidos:")
                for i, (codigo, nombre, cantidad, total) in enumerate(productos_vendidos):
                    print(f"{i + 1}. {nombre} (x{cantidad}) - ${total:.2f}")

                try:
                    indice = int(input("Seleccione el número del producto a borrar: ")) - 1
                    if 0 <= indice < len(productos_vendidos):
                        producto_borrado = productos_vendidos.pop(indice)
                        total_venta -= producto_borrado[3]
                        print(f"Producto borrado: {producto_borrado[1]} (x{producto_borrado[2]}).")
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Entrada inválida. Intente de nuevo.")
            elif opcion == "4":
                if not productos_vendidos:
                    print("No se ha agregado ningún producto. Por favor, registre al menos un producto antes de finalizar.")
                    continue

                print(f"\nTotal de la venta: ${total_venta:.2f}")
                while True:
                    try:
                        recibido = float(input("Monto recibido: "))
                        if recibido >= total_venta:
                            cambio = recibido - total_venta
                            print(f"Cambio: ${cambio:.2f}")
                            print("Venta realizada con éxito. Gracias por su compra.")
                            for codigo, nombre, cantidad, total_producto in productos_vendidos:
                                db.registrar_venta(codigo, nombre, cantidad, total_producto, ticket_id)
                                db.actualizar_stock(codigo, cantidad)
                            break
                        else:
                            print("El monto recibido es insuficiente. Intente nuevamente.")
                    except ValueError:
                        print("Por favor, ingrese una cantidad válida.")
                break
            elif opcion == "5":
                print("Saliendo al menú principal...")
                return
            else:
                print("Opción no válida. Intente nuevamente.")

# Módulo para editar productos en el inventario
def editar_inventario(db):
    imprimir_titulo("EDITAR INVENTARIO")
    db.mostrar_inventario()  # Mostrar el inventario actual para elegir un producto

    try:
        codigo_barras = input("\nIngrese el código de barras del producto que desea modificar: ").strip()
        db.cursor.execute('SELECT * FROM productos WHERE codigo = ?', (codigo_barras,))
        producto = db.cursor.fetchone()

        if producto:
            print(f"\nProducto seleccionado: {producto[2]} (Código: {producto[1]}, Precio: ${producto[3]:.2f}, Existencias: {producto[4]})")

            nuevo_nombre = input("Nuevo nombre (presiona Enter para no modificar): ").strip()
            nuevo_precio = input("Nuevo precio (presiona Enter para no modificar): ").strip()
            nueva_cantidad = input("Nueva cantidad (presiona Enter para no modificar): ").strip()

            # Mantener los valores actuales si el usuario no ingresa cambios
            nuevo_nombre = nuevo_nombre if nuevo_nombre else producto[2]
            nuevo_precio = float(nuevo_precio) if nuevo_precio else producto[3]
            nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else producto[4]

            # Actualizar el producto en la base de datos
            db.cursor.execute('''
                UPDATE productos 
                SET nombre = ?, precio = ?, cantidad = ?
                WHERE codigo = ?
            ''', (nuevo_nombre, nuevo_precio, nueva_cantidad, codigo_barras))
            db.conexion.commit()

            print("Producto actualizado exitosamente.")
        else:
            print("Producto no encontrado. Verifique el código de barras e intente de nuevo.")
    except ValueError:
        print("Entrada inválida. Por favor, intente de nuevo.")

# Módulo para ver reportes de ventas
def ver_reportes_ventas(db):
    imprimir_titulo("REPORTES DE VENTAS")
    ventas = db.obtener_ventas_por_ticket()

    if ventas:
        headers = ["Ticket ID", "Fecha y Hora", "Total", "Productos"]
        tabla = [[v[0], v[1], f"${v[2]:.2f}", v[3]] for v in ventas]
        print(tabulate(tabla, headers, tablefmt="grid"))
    else:
        print("No hay ventas registradas en este turno.")

# Menú principal
def menu_principal():
    db = Database('datos/tienda.db')

    while True:
        imprimir_titulo("MENÚ PRINCIPAL")
        print("1. Mostrar Inventario")
        print("2. Agregar Producto al Inventario")
        print("3. Realizar Venta")
        print("4. Editar Inventario")
        print("5. Corte de Caja")
        print("6. Ver Reportes de Ventas")
        print("7. Salir")
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
            ver_reportes_ventas(db)
        elif opcion == '7':
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
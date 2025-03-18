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
                cantidad INTEGER NOT NULL,
                total REAL NOT NULL,
                fecha_hora TEXT
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

    def registrar_venta(self, codigo, cantidad, total):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO ventas (producto_id, cantidad, total, fecha_hora) 
            VALUES (?, ?, ?, ?)
        ''', (codigo, cantidad, total, fecha_hora))
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
    db.cursor.execute('SELECT total, fecha_hora FROM ventas')
    ventas = db.cursor.fetchall()
    total_ventas = sum(v[0] for v in ventas)
    fecha_inicio = ventas[0][1] if ventas else "No hay ventas registradas"
    fecha_fin = ventas[-1][1] if ventas else "No hay ventas registradas"

    print(f"Corte de caja desde: {fecha_inicio}")
    print(f"Hasta: {fecha_fin}")
    print(f"Total de ventas: ${total_ventas:.2f}")

    while True:
        print("\nOpciones:")
        print("1. Guardar corte de caja e iniciar uno nuevo")
        print("2. Salir y continuar usando el corte actual")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            archivo = f"corte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(archivo, 'w') as f:
                f.write(f"Corte de caja desde: {fecha_inicio}\n")
                f.write(f"Hasta: {fecha_fin}\n")
                f.write(f"Total de ventas: ${total_ventas:.2f}\n")
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

# Módulo de ventas modificado para utilizar código de barras
def realizar_venta(db):
    imprimir_titulo("REGISTRO DE VENTA")
    productos_vendidos = []
    total_venta = 0

    while True:
        print("\nOpciones:")
        print("1. Ver Inventario")
        print("2. Agregar Producto a la Venta")
        print("3. Finalizar Venta")
        print("4. Salir al Menú Principal")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            db.mostrar_inventario()
        elif opcion == "2":
            try:
                codigo_barras = input("Ingrese el código de barras del producto: ").strip()
                cantidad = int(input("Cantidad: "))
                db.cursor.execute('SELECT precio, cantidad FROM productos WHERE codigo = ?', (codigo_barras,))
                producto = db.cursor.fetchone()

                if producto and producto[1] >= cantidad:
                    total_producto = producto[0] * cantidad
                    productos_vendidos.append((codigo_barras, cantidad, total_producto))
                    total_venta += total_producto
                    print(f"Producto agregado. Total parcial: ${total_venta:.2f}")
                else:
                    print("Stock insuficiente o producto no encontrado.")
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")
        elif opcion == "3":
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
                        for codigo, cantidad, total_producto in productos_vendidos:
                            db.registrar_venta(codigo, cantidad, total_producto)
                            db.actualizar_stock(codigo, cantidad)
                        break
                    else:
                        print("El monto recibido es insuficiente. Intente nuevamente.")
                except ValueError:
                    print("Por favor, ingrese una cantidad válida.")
            break
        elif opcion == "4":
            print("Saliendo al menú principal...")
            return
        else:
            print("Opción no válida. Intente nuevamente.")

# Función para agregar columna fecha_hora si no existe
def agregar_columna_fecha_hora(db):
    try:
        db.cursor.execute("ALTER TABLE ventas ADD COLUMN fecha_hora TEXT")
        db.conexion.commit()
        print("Columna 'fecha_hora' agregada correctamente a la tabla 'ventas'.")
    except sqlite3.OperationalError:
        print("La columna 'fecha_hora' ya existe en la tabla 'ventas'.")

# Menú principal
def menu_principal():
    db = Database('datos/tienda.db')
    agregar_columna_fecha_hora(db)  # Agregar columna 'fecha_hora' si no existe

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
            print("Editar inventario: En construcción")
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

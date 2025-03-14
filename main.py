import os
from productos import Producto
from inventario import Inventario
from ventas import Venta

# Crea un directorio llamado 'datos' si no existe
def crear_directorios():
    os.makedirs('datos', exist_ok=True)

# Imprime un título con bordes decorativos
def imprimir_titulo(titulo):
    borde = "=" * (len(titulo) + 4)
    print("\n" + borde)
    print(f"| {titulo} |")
    print(borde + "\n")

# Proceso de venta continuo
def proceso_venta(venta, inventario):
    while True:  # Ciclo para iniciar nuevas ventas automáticamente
        productos_agregados = []  # Lista para almacenar los productos agregados en esta venta
        while True:
            imprimir_titulo("REGISTRO DE VENTA")
            print("Ingrese el código del producto (o escriba 'finalizar' para terminar la venta):")
            codigo = input("Código: ").strip()  # Asegura que no haya espacios adicionales

            if codigo.lower() == 'finalizar':  # Finaliza el proceso de venta
                if not productos_agregados:  # Validar si no se agregó ningún producto
                    print("No se han registrado productos. Venta cancelada.")
                    break  # Regresar al inicio de otra venta
                imprimir_titulo("RESUMEN DE VENTA")
                for p in productos_agregados:
                    print(f"{p['nombre']} x{p['cantidad']} - ${p['total']:.2f}")
                total = sum(p['total'] for p in productos_agregados)  # Calcula el total correctamente
                print(f"\nTOTAL: ${total:.2f}")
                
                # Calculadora para cambio
                while True:
                    try:
                        recibido = float(input("Ingrese cantidad recibida: "))
                        if recibido >= total:
                            cambio = recibido - total
                            print(f"Cambio: ${cambio:.2f}")
                            print("Venta finalizada. ¡Gracias!")
                            venta.finalizar_venta()
                            break  # Salir de la calculadora y regresar al inicio de otra venta
                        else:
                            print("La cantidad recibida es insuficiente. Intente de nuevo.")
                    except ValueError:  # Manejo de errores para entradas no numéricas
                        print("Por favor, ingrese una cantidad válida.")
                break  # Salir del flujo actual y comenzar otra venta
            else:  # Agrega un producto a la venta
                try:
                    cantidad = int(input("Cantidad: "))
                    producto = next((p for p in inventario.productos if p.codigo == codigo), None)
                    if producto:
                        venta.agregar_producto(producto, cantidad)
                        productos_agregados.append({
                            'nombre': producto.nombre,
                            'cantidad': cantidad,
                            'total': producto.precio * cantidad
                        })
                        print(f"Producto agregado: {producto.nombre} x{cantidad}")
                    else:
                        print("Producto no encontrado. Intente nuevamente.")
                except ValueError:  # Manejo de errores para entradas no numéricas
                    print("Por favor, ingrese una cantidad válida.")

# Muestra el menú principal con las opciones disponibles
def menu():
    imprimir_titulo("MENÚ PRINCIPAL")
    print("1. Mostrar Inventario")
    print("2. Agregar Producto al Inventario")
    print("3. Realizar Venta")
    print("4. Salir")
    print("=" * 20)

# Función principal que ejecuta el sistema de punto de venta
def main():
    crear_directorios()  # Asegura que el directorio de datos exista
    inventario = Inventario('datos/inventario.json')  # Carga el inventario desde un archivo JSON
    venta = Venta('datos/ventas.json')  # Carga las ventas desde un archivo JSON

    # Bucle principal del programa
    while True:
        menu()  # Muestra el menú principal
        opcion = input("Seleccione una opción: ")

        if opcion == '1':  # Mostrar inventario
            imprimir_titulo("INVENTARIO")
            inventario.mostrar_inventario()
        elif opcion == '2':  # Agregar producto al inventario
            imprimir_titulo("AGREGAR PRODUCTO")
            codigo = input("Código: ")
            nombre = input("Nombre: ")
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))
            producto = Producto(codigo, nombre, precio, cantidad)
            inventario.agregar_producto(producto)
            print("Producto agregado exitosamente.")
        elif opcion == '3':  # Realizar venta
            proceso_venta(venta, inventario)  # Proceso continuo de venta
        elif opcion == '4':  # Salir del programa
            imprimir_titulo("SALIDA")
            print("Gracias por usar el punto de venta. ¡Hasta luego!")
            break  # Rompe el bucle para salir
        else:
            print("Opción no válida")

# Verifica que el archivo esté siendo ejecutado directamente
if __name__ == "__main__":
    main()

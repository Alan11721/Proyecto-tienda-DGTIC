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
            codigo = input("Código: ").strip()

            if codigo.lower() == 'finalizar':  # Finaliza el proceso de venta
                if not productos_agregados:
                    print("No se han registrado productos. Venta cancelada.")
                    break
                imprimir_titulo("RESUMEN DE VENTA")
                total = sum(p['total'] for p in productos_agregados)
                for p in productos_agregados:
                    print(f"{p['nombre']} x{p['cantidad']} - ${p['total']:.2f}")
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
                            break  # Termina la calculadora
                        else:
                            print("La cantidad recibida es insuficiente. Intente de nuevo.")
                    except ValueError:
                        print("Por favor, ingrese una cantidad válida.")
                break  # Comienza otra venta
            else:
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
                except ValueError:
                    print("Por favor, ingrese una cantidad válida.")

# Menú principal
def menu():
    imprimir_titulo("MENÚ PRINCIPAL")
    print("1. Mostrar Inventario")
    print("2. Agregar Producto al Inventario")
    print("3. Realizar Venta")
    print("4. Salir")
    print("=" * 20)

def main():
    crear_directorios()
    inventario = Inventario('datos/inventario.json')
    venta = Venta('datos/ventas.json')

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            imprimir_titulo("INVENTARIO")
            inventario.mostrar_inventario()
        elif opcion == '2':
            imprimir_titulo("AGREGAR PRODUCTO")
            codigo = input("Código: ")
            nombre = input("Nombre: ")
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))
            producto = Producto(codigo, nombre, precio, cantidad)
            inventario.agregar_producto(producto)
            print("Producto agregado exitosamente.")
        elif opcion == '3':
            proceso_venta(venta, inventario)
        elif opcion == '4':
            imprimir_titulo("SALIDA")
            print("Gracias por usar el punto de venta. ¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()

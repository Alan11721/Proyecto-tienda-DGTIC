import os
from productos import Producto
from inventario import Inventario
from ventas import Venta

def crear_directorios():
    os.makedirs('datos', exist_ok=True)

def imprimir_titulo(titulo):
    print("\n" + "="*len(titulo))
    print(titulo)
    print("="*len(titulo) + "\n")

def menu():
    imprimir_titulo("MENÚ PRINCIPAL")
    print("1. Mostrar Inventario")
    print("2. Agregar Producto al Inventario")
    print("3. Realizar Venta")
    print("4. Salir")
    print("="*20)

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
        elif opcion == '3':
            imprimir_titulo("REALIZAR VENTA")
            codigo = input("Código del producto: ")
            cantidad = int(input("Cantidad: "))
            producto = next((p for p in inventario.productos if p.codigo == codigo), None)
            if producto:
                venta.agregar_producto(producto, cantidad)
                venta.finalizar_venta()
            else:
                print("Producto no encontrado")
        elif opcion == '4':
            imprimir_titulo("SALIDA")
            print("Gracias por usar el punto de venta. ¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()

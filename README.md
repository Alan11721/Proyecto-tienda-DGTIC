# Proyectp-tienda-DGTIC
Este proyecto se desarrollará como una alternativa a los puntos de venta tradicionales disponibles en el mercado. Aunque existen muchas opciones muy completas, muchas de ellas son bastante caras y requieren una cantidad considerable de recursos. Es por eso que este proyecto pretende ofrecer una alternativa más accesible, ya que los recursos necesarios son mínimos, facilitando su implementación en equipos más antiguos.

El objetivo es crear un sistema minimalista y fácil de usar para el usuario final. Aunque se ejecutará en la terminal y requerirá cierto conocimiento básico para manejarlo adecuadamente, la curva de aprendizaje será breve. Una vez dominado, los usuarios podrán utilizarlo sin mayores complicaciones.

Este sistema se limitará a las funciones mínimas necesarias para resolver las necesidades de una tienda de abarrotes pequeña. Estas funcionalidades incluyen:

Memorizar los precios de los productos: Simplificando la gestión de productos y precios.

Realizar cortes de caja: Facilitando el control de ventas diarias.

Aunque muchas herramientas en el mercado permiten llevar un control de inventario, generar reportes de ventas, gestionar compras, diseñar tickets y muchas otras funciones, la realidad es que muy pocos negocios utilizan todas estas características. Por lo tanto, si no se van a utilizar, no vale la pena pagar por ellas. Este proyecto ofrece una solución más simple y económica, enfocándose únicamente en lo esencial.

**Características principales**
Gestión de productos: Permite agregar, editar y eliminar productos con sus precios y cantidades.

Registro de ventas: Facilita la venta de productos y el cálculo automático del cambio.

Cortes de caja: Genera reportes de ventas diarias y permite reiniciar el conteo de ventas.

Reportes de ventas: Muestra un resumen de todas las ventas realizadas durante el turno.

**Requisitos mínimos**
El programa está diseñado para funcionar en equipos con recursos limitados. Los requisitos mínimos son:

Sistema operativo: Windows, macOS o Linux.

Python: Versión 3.6 o superior.

Memoria RAM: 512 MB (recomendado 1 GB).

Almacenamiento: Menos de 10 MB de espacio en disco.

**Instalación**
Sigue estos pasos para instalar y ejecutar el programa:

1. Descargar el proyecto
Ve al repositorio del proyecto en GitHub: Proyecto Tienda DGTIC.

Haz clic en el botón Code y selecciona Download ZIP.

Extrae el archivo ZIP en una carpeta de tu computadora.

2. Instalar Python
Si no tienes Python instalado, sigue estos pasos:

Ve al sitio oficial de Python: python.org.

Descarga la versión más reciente de Python (3.6 o superior).

Ejecuta el instalador y asegúrate de marcar la opción Add Python to PATH antes de hacer clic en Install Now.

3. Ejecutar el programa
Abre una terminal o consola en tu computadora.

Navega a la carpeta donde extrajiste el proyecto. Por ejemplo:

bash
Copy
cd C:\Users\TuUsuario\Downloads\Proyecto-tienda-DGTIC
Ejecuta el programa con el siguiente comando:

bash
Copy
python main.py
Instrucciones de uso
Una vez que el programa esté en ejecución, sigue estas instrucciones para usarlo:

**Menú principal**
El programa mostrará un menú con las siguientes opciones:

Mostrar Inventario: Muestra todos los productos disponibles.

Agregar Producto: Permite agregar un nuevo producto al inventario.

Realizar Venta: Inicia el proceso de venta de productos.

Editar Inventario: Permite modificar los datos de un producto existente.

Corte de Caja: Genera un reporte de ventas y permite reiniciar el conteo.

Ver Reportes de Ventas: Muestra un resumen de todas las ventas realizadas.

Salir: Cierra el programa.

**Realizar una venta**
Selecciona la opción Realizar Venta en el menú principal.
Escanea o ingresa manualmente el código de barras del producto.
Ingresa la cantidad vendida.
Repite los pasos 2 y 3 para agregar más productos.
Cuando termines, selecciona la opción Finalizar Venta.
Ingresa el monto recibido y el programa calculará el cambio automáticamente.

**Corte de caja**
Selecciona la opción Corte de Caja en el menú principal.
El programa mostrará un resumen de las ventas realizadas.
Puedes guardar el corte de caja en un archivo de texto o continuar con el conteo actual.

**Preguntas frecuentes**
-¿Cómo puedo agregar un nuevo producto?
Selecciona la opción Agregar Producto en el menú principal.
Ingresa el código de barras, nombre, precio y cantidad del producto.
Confirma los datos y el producto se agregará al inventario.

-¿Qué hago si me equivoco al agregar un producto a la venta?
Durante el proceso de venta, selecciona la opción Borrar Producto Añadido.
Elige el producto que deseas eliminar de la venta.
Continúa con la venta normalmente.

-¿Cómo puedo ver las ventas realizadas?
Selecciona la opción Ver Reportes de Ventas en el menú principal.
El programa mostrará un resumen de todas las ventas realizadas durante el turno.

**Contribuir**
Si deseas contribuir a este proyecto, sigue estos pasos:
Haz un fork del repositorio.
Crea una rama con tu nueva funcionalidad (git checkout -b nueva-funcionalidad).
Realiza tus cambios y haz commit (git commit -m 'Agrega nueva funcionalidad').
Haz push a la rama (git push origin nueva-funcionalidad).
Abre un Pull Request en GitHub.

**Licencia**
Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo LICENSE.

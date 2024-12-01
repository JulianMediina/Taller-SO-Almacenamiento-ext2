# Sistema de Archivos Simulado Ext2

Este proyecto implementa un sistema de archivos simulado basado en el sistema Ext2. Permite crear, eliminar, recuperar, mover archivos y realizar pruebas de estrés sobre el sistema. Además, muestra el estado actual de los bloques y los inodos de manera tabular.

## Funcionalidades

- **Crear archivo**: Permite crear archivos con un nombre y tamaño especificado, asignando bloques disponibles e inodos.
- **Eliminar archivo**: Elimina archivos, liberando los bloques y el inodo asociado.
- **Recuperar archivo**: Recupera información sobre un archivo existente, como su tamaño y bloques asociados.
- **Mover archivo**: Mueve un archivo a otros bloques disponibles si hay suficiente espacio.
- **Mostrar estado**: Muestra el estado actual de los bloques y los inodos, indicando si están ocupados o libres.
- **Prueba de estrés**: Realiza operaciones aleatorias de creación, eliminación, recuperación y movimiento de archivos para probar la capacidad y eficiencia del sistema.

## Estructura del Código

### Parámetros del sistema de archivos

- `TAMANO_BLOQUE`: Tamaño de cada bloque en bytes (4 KB).
- `NUMERO_BLOQUES`: Número total de bloques disponibles.
- `NUMERO_INODOS`: Número total de inodos disponibles.

### Clases

#### `SistemaArchivosExt2`

Esta clase implementa las funciones principales del sistema de archivos, incluyendo:

- `crear_archivo(nombre, tamano)`: Crea un archivo.
- `eliminar_archivo(nombre)`: Elimina un archivo.
- `recuperar_archivo(nombre)`: Recupera información de un archivo.
- `mover_archivo(nombre)`: Mueve un archivo a otros bloques.
- `mostrar_estado()`: Muestra el estado de bloques e inodos.
- `prueba_estres(num_operaciones)`: Realiza una prueba de estrés con operaciones aleatorias.

#### `interfaz_consola()`

Función que presenta una interfaz de línea de comandos donde el usuario puede interactuar con el sistema de archivos, eligiendo opciones como crear, eliminar, mover archivos y ejecutar pruebas de estrés.

## Instalación

Para ejecutar este sistema de archivos simulado, solo necesitas tener Python instalado. Además, se utiliza la biblioteca `prettytable` para mostrar el estado de bloques e inodos en formato tabular.

Instala `prettytable` con el siguiente comando:

```bash
pip install prettytable

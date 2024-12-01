import math
from prettytable import PrettyTable

# Parámetros del sistema de archivos
TAMANO_BLOQUE = 4096  # 4 KB
NUMERO_BLOQUES = 100  # Total de bloques disponibles
NUMERO_INODOS = 20    # Total de inodos disponibles

class SistemaArchivosExt2:
    """
    Implementación de un sistema de archivos simulado basado en Ext2.
    Permite crear, eliminar, recuperar y mover archivos, además de mostrar el estado actual de bloques e inodos.
    """

    def __init__(self):
        # Inicialización del sistema de archivos
        self.bitmap_bloques = [0] * NUMERO_BLOQUES  # Estado de los bloques (0 = libre, 1 = ocupado)
        self.tabla_inodos = [None] * NUMERO_INODOS  # Cada inodo representa un archivo
        self.archivos = {}  # Diccionario para almacenar los metadatos de los archivos

    def crear_archivo(self, nombre, tamano):
        """
        Crea un archivo con el nombre y tamaño especificados.
        Asigna los bloques necesarios y un inodo disponible.
        """
        if nombre in self.archivos:
            return f"Error: El archivo '{nombre}' ya existe."

        # Calcular el número de bloques necesarios
        bloques_necesarios = math.ceil(tamano / TAMANO_BLOQUE)
        bloques_disponibles = [i for i, ocupado in enumerate(self.bitmap_bloques) if not ocupado]

        if len(bloques_disponibles) < bloques_necesarios:
            return "Error: No hay suficiente espacio en disco."

        # Asignar bloques disponibles
        bloques_asignados = bloques_disponibles[:bloques_necesarios]
        for bloque in bloques_asignados:
            self.bitmap_bloques[bloque] = 1

        # Buscar un inodo libre
        inodo_libre = next((i for i, inodo in enumerate(self.tabla_inodos) if inodo is None), None)
        if inodo_libre is None:
            # Revertir cambios si no hay inodo libre
            for bloque in bloques_asignados:
                self.bitmap_bloques[bloque] = 0
            return "Error: No hay inodos disponibles."

        # Actualizar metadatos
        self.tabla_inodos[inodo_libre] = {
            'nombre': nombre,
            'tamano': tamano,
            'bloques': bloques_asignados,
        }
        self.archivos[nombre] = self.tabla_inodos[inodo_libre]
        return f"Archivo '{nombre}' creado exitosamente en bloques: {bloques_asignados}"

    def eliminar_archivo(self, nombre):
        """
        Elimina un archivo, liberando sus bloques y el inodo asociado.
        """
        if nombre not in self.archivos:
            return f"Error: El archivo '{nombre}' no existe."

        archivo = self.archivos.pop(nombre)
        for bloque in archivo['bloques']:
            self.bitmap_bloques[bloque] = 0

        # Liberar el inodo asociado
        inodo_index = next(i for i, inodo in enumerate(self.tabla_inodos) if inodo and inodo['nombre'] == nombre)
        self.tabla_inodos[inodo_index] = None
        return f"Archivo '{nombre}' eliminado exitosamente."

    def recuperar_archivo(self, nombre):
        """
        Recupera información sobre un archivo existente.
        """
        if nombre not in self.archivos:
            return f"Error: El archivo '{nombre}' no existe."

        archivo = self.archivos[nombre]
        return f"Archivo '{nombre}': Tamaño {archivo['tamano']} bytes, Bloques {archivo['bloques']}."

    def mover_archivo(self, nombre):
        """
        Mueve un archivo a otros bloques disponibles, si es posible.
        """
        if nombre not in self.archivos:
            return f"Error: El archivo '{nombre}' no existe."

        archivo = self.archivos[nombre]
        bloques_necesarios = len(archivo['bloques'])
        bloques_disponibles = [i for i, ocupado in enumerate(self.bitmap_bloques) if not ocupado]

        if len(bloques_disponibles) < bloques_necesarios:
            return "Error: No hay suficientes bloques disponibles para mover el archivo."

        # Liberar los bloques actuales
        for bloque in archivo['bloques']:
            self.bitmap_bloques[bloque] = 0

        # Asignar nuevos bloques
        nuevos_bloques_asignados = bloques_disponibles[:bloques_necesarios]
        for bloque in nuevos_bloques_asignados:
            self.bitmap_bloques[bloque] = 1

        # Actualizar el inodo y los metadatos
        inodo_index = next(i for i, inodo in enumerate(self.tabla_inodos) if inodo and inodo['nombre'] == nombre)
        self.tabla_inodos[inodo_index]['bloques'] = nuevos_bloques_asignados
        self.archivos[nombre]['bloques'] = nuevos_bloques_asignados

        return f"Archivo '{nombre}' movido exitosamente a bloques: {nuevos_bloques_asignados}"

    def mostrar_estado(self):
        """
        Muestra el estado actual de los bloques y los inodos en formato tabular.
        """
        # Crear tabla para bloques
        tabla_bloques = PrettyTable()
        tabla_bloques.field_names = ["Bloque", "Estado", "Archivo Asociado"]
        for i, ocupado in enumerate(self.bitmap_bloques):
            archivo_asociado = next((a for a, datos in self.archivos.items() if i in datos['bloques']), "Ninguno")
            estado = "Ocupado" if ocupado else "Libre"
            tabla_bloques.add_row([i, estado, archivo_asociado])

        # Crear tabla para inodos
        tabla_inodos = PrettyTable()
        tabla_inodos.field_names = ["Inodo", "Estado", "Nombre Archivo", "Tamaño", "Bloques"]
        for i, inodo in enumerate(self.tabla_inodos):
            if inodo:
                tabla_inodos.add_row([i, "Ocupado", inodo['nombre'], inodo['tamano'], inodo['bloques']])
            else:
                tabla_inodos.add_row([i, "Libre", "-", "-", "-"])

        return f"--- Estado de Bloques ---\n{tabla_bloques}\n\n--- Estado de Inodos ---\n{tabla_inodos}"

    def prueba_estres(self, num_operaciones):
        """
        Realiza una prueba de estrés ejecutando operaciones aleatorias sobre el sistema de archivos.
        """
        import random

        print(f"Iniciando prueba de estrés con {num_operaciones} operaciones...")

        # Crear archivos iniciales
        nombres_archivos = [f"file_{i}" for i in range(num_operaciones)]
        tamano_archivos = [random.randint(1024, 8192) for _ in range(num_operaciones // 2)]

        print("Creando archivos iniciales...")
        for i, nombre in enumerate(nombres_archivos[:num_operaciones // 2]):
            tamano = tamano_archivos[i]
            print(self.crear_archivo(nombre, tamano))

        # Realizar operaciones aleatorias
        print("Ejecutando operaciones aleatorias...")
        for _ in range(num_operaciones):
            operacion = random.choice(["crear", "eliminar", "recuperar", "mover"])
            nombre = random.choice(nombres_archivos)

            if operacion == "crear":
                tamano = random.randint(1024, 8192)
                print(f"Intentando crear archivo: {nombre} con tamaño {tamano} bytes")
                print(self.crear_archivo(nombre, tamano))

            elif operacion == "eliminar":
                print(f"Intentando eliminar archivo: {nombre}")
                print(self.eliminar_archivo(nombre))

            elif operacion == "recuperar":
                print(f"Intentando recuperar archivo: {nombre}")
                print(self.recuperar_archivo(nombre))

            elif operacion == "mover":
                print(f"Intentando mover archivo: {nombre}")
                print(self.mover_archivo(nombre))


# Interfaz por consola
def interfaz_consola():
    sistema = SistemaArchivosExt2()

    while True:
        print("\n--- Sistema de Archivos Ext2 ---")
        print("1. Crear archivo")
        print("2. Eliminar archivo")
        print("3. Recuperar archivo")
        print("4. Mostrar estado de bloques e inodos")
        print("5. Mover archivo")
        print("6. Ejecutar prueba de estrés")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del archivo: ")
            tamano = int(input("Ingrese el tamaño del archivo (en bytes): "))
            print(sistema.crear_archivo(nombre, tamano))
        elif opcion == "2":
            nombre = input("Ingrese el nombre del archivo a eliminar: ")
            print(sistema.eliminar_archivo(nombre))
        elif opcion == "3":
            nombre = input("Ingrese el nombre del archivo a recuperar: ")
            print(sistema.recuperar_archivo(nombre))
        elif opcion == "4":
            print(sistema.mostrar_estado())
        elif opcion == "5":
            nombre = input("Ingrese el nombre del archivo a mover: ")
            print(sistema.mover_archivo(nombre))
        elif opcion == "6":
            num_operaciones = int(input("Ingrese el número de operaciones para la prueba de estrés: "))
            sistema.prueba_estres(num_operaciones)
        elif opcion == "7":
            print("Saliendo del sistema de archivos.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    interfaz_consola()

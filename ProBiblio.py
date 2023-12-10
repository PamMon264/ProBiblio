from pymongo import MongoClient

class Biblioteca:
    def __init__(self, connection_string, db_name):
        # Conexión a la base de datos
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.libros_collection = self.db['Libros_en_la_Biblioteca']
        self.alumnos_collection = self.db['Alumnos_en_la_Biblioteca']
    
    def ingresar_libro(self):
        nombre_libro = input("Ingrese el nombre del libro: ")

        categorias_disponibles = ["Ciencia-ficción", "Terror", "Drama", "Informática", "Acción"]
        print("Categorías de libros disponibles:")
        for i, categoria in enumerate(categorias_disponibles, 1):
            print(f"{i}. {categoria}")

        try:
            eleccion_categoria = int(input("Seleccione la categoría (número): "))
            # Validar que la elección esté dentro del rango
            if 1 <= eleccion_categoria <= len(categorias_disponibles):
                # Asignar la categoría seleccionada
                categoria = categorias_disponibles[eleccion_categoria - 1]
            else:
                print("Selección inválida. Se establecerá la categoría como 'Otra'")
                categoria = "Otra"
        except ValueError:
            print("Selección inválida. Se establecerá la categoría como 'Otra'")
            categoria = "Otra"

        nombre_autor = input("Ingrese el nombre del autor: ")
        apellido_autor = input("Ingrese el apellido del autor: ")
        nacionalidad_autor = input("Ingrese la nacionalidad del autor: ")

        libro = {
            "nombre": nombre_libro,
            "categoria": categoria,
            "autor": {
                "nombre": nombre_autor,
                "apellido": apellido_autor,
                "nacionalidad": nacionalidad_autor
            }
        }

        self.libros_collection.insert_one(libro)
        print("Libro ingresado con éxito.")

        
    def agregar_alumno_y_prestar_libro(self):
        nombre_alumno = input("Ingrese el nombre del alumno: ")
        apellido_alumno = input("Ingrese el apellido del alumno: ")
        carrera_alumno = input("Ingrese la carrera del alumno: ")
        numero_control_alumno = input("Ingrese el número de control del alumno: ")

        lista_libros = list(self.libros_collection.find({}, {"nombre": 1}))

        if not lista_libros:
            print("No hay libros disponibles en la biblioteca para prestar.")
            return

        print("Lista de libros disponibles:")
        for i, libro in enumerate(lista_libros, 1):
            print(f"{i}. {libro['nombre']}")

        try:
            eleccion_libro = int(input("Seleccione el libro (número): "))
            if 1 <= eleccion_libro <= len(lista_libros):
                # Obtener la información completa del libro desde la base de datos
                libro_seleccionado = self.libros_collection.find_one({"nombre": lista_libros[eleccion_libro - 1]["nombre"]})
            else:
                print("Selección inválida. No se pudo obtener información del libro seleccionado.")
                return
        except ValueError:
            print("Selección inválida. No se pudo obtener información del libro seleccionado.")
            return

        categoria_libro = libro_seleccionado.get("categoria", "Otra")

        alumno = {
            "nombre": nombre_alumno,
            "apellido": apellido_alumno,
            "carrera": carrera_alumno,
            "numero_control": numero_control_alumno,
            "libro_prestado": {
                "nombre": libro_seleccionado["nombre"],
                "categoria": categoria_libro
            }
        }

        self.alumnos_collection.insert_one(alumno)
        print("Alumno agregado y libro prestado con éxito.")

   




    def consultar_libros(self):
        lista_libros = list(self.libros_collection.find())

        if not lista_libros:
            print("No hay libros disponibles en la biblioteca.")
            return

        for libro in lista_libros:
            print("\nNombre del libro:", libro["nombre"])
            print("Autor:", f"{libro['autor']['nombre']} {libro['autor']['apellido']}")
            print("Categoría:", libro["categoria"])

            alumnos_que_solicitaron = list(self.alumnos_collection.find({"libro_prestado.nombre": libro["nombre"]}))

            if alumnos_que_solicitaron:
                print("Alumnos que solicitaron este libro:")
                for alumno in alumnos_que_solicitaron:
                    print(f"- {alumno['nombre']} {alumno['apellido']}, {alumno['carrera']}, Número de control: {alumno['numero_control']}")
            else:
                print("Ningún alumno ha solicitado este libro.")

    def mostrar_libros_para_modificar(self):
        lista_libros = list(self.libros_collection.find())

        if not lista_libros:
            print("No hay libros disponibles en la biblioteca.")
            return

        print("Libros disponibles para modificar:")
        for i, libro in enumerate(lista_libros, 1):
            print(f"{i}. {libro['nombre']} - Autor: {libro['autor']['nombre']} {libro['autor']['apellido']} - Categoría: {libro['categoria']}")

        try:
            eleccion_libro = int(input("Seleccione el libro a modificar (número): "))
            libro_a_modificar = lista_libros[eleccion_libro - 1]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        print("\nCampos disponibles para modificar:")
        print("1. Nombre del libro")
        print("2. Categoría del libro")
        print("3. Autor del libro")

        try:
            eleccion_campo = int(input("Seleccione el campo a modificar (número): "))
        except ValueError:
            print("Selección inválida.")
            return

        if eleccion_campo == 1:
            nuevo_nombre = input("Ingrese el nuevo nombre del libro: ")
            self.libros_collection.update_one({"_id": libro_a_modificar["_id"]}, {"$set": {"nombre": nuevo_nombre}})
        elif eleccion_campo == 2:
            nueva_categoria = input("Ingrese la nueva categoría del libro: ")
            self.libros_collection.update_one({"_id": libro_a_modificar["_id"]}, {"$set": {"categoria": nueva_categoria}})
        elif eleccion_campo == 3:
            nuevo_nombre_autor = input("Ingrese el nuevo nombre del autor: ")
            nuevo_apellido_autor = input("Ingrese el nuevo apellido del autor: ")
            self.libros_collection.update_one({"_id": libro_a_modificar["_id"]}, {"$set": {"autor.nombre": nuevo_nombre_autor, "autor.apellido": nuevo_apellido_autor}})
        else:
            print("Selección inválida.")

        print("Libro modificado con éxito.")

    def eliminar_libro(self):
        lista_libros = list(self.libros_collection.find())

        if not lista_libros:
            print("No hay libros disponibles en la biblioteca.")
            return

        print("Libros disponibles para eliminar:")
        for i, libro in enumerate(lista_libros, 1):
            print(f"{i}. {libro['nombre']} - Autor: {libro['autor']['nombre']} {libro['autor']['apellido']} - Categoría: {libro['categoria']}")

        try:
            eleccion_libro = int(input("Seleccione el libro a eliminar (número): "))
            libro_a_eliminar = lista_libros[eleccion_libro - 1]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        confirmacion = input(f"¿Está seguro de que desea eliminar el libro '{libro_a_eliminar['nombre']}'? (S/N): ").lower()

        if confirmacion == 's':
            self.libros_collection.delete_one({"_id": libro_a_eliminar["_id"]})
            print("Libro eliminado.")
        else:
            print("Operación cancelada.")

    def consultar_alumnos(self):
        lista_alumnos = list(self.alumnos_collection.find())

        if not lista_alumnos:
            print("No hay alumnos registrados en el sistema.")
            return

        print("Alumnos en el sistema:")
        for alumno in lista_alumnos:
            print("\nNombre del alumno:", alumno["nombre"], alumno["apellido"])
            print("Carrera:", alumno["carrera"])
            print("Número de control:", alumno["numero_control"])

            libro_prestado = alumno.get("libro_prestado")
            if libro_prestado:
                print("Libro solicitado:")
                print(f"- {libro_prestado['nombre']} - Categoría: {libro_prestado['categoria']}")
            else:
                print("El alumno no ha solicitado ningún libro.")

    def modificar_alumno(self):
        numero_control = input("Ingrese el número de control del alumno a modificar: ")

        alumno_a_modificar = self.alumnos_collection.find_one({"numero_control": numero_control})

        if not alumno_a_modificar:
            print("No se encontró ningún alumno con ese número de control.")
            return

        print("\nCampos disponibles para modificar:")
        print("1. Nombre del alumno")
        print("2. Apellido del alumno")
        print("3. Carrera del alumno")

        try:
            eleccion_campo = int(input("Seleccione el campo a modificar (número): "))
        except ValueError:
            print("Selección inválida.")
            return

        if eleccion_campo == 1:
            nuevo_nombre = input("Ingrese el nuevo nombre del alumno: ")
            self.alumnos_collection.update_one({"numero_control": numero_control}, {"$set": {"nombre": nuevo_nombre}})
        elif eleccion_campo == 2:
            nuevo_apellido = input("Ingrese el nuevo apellido del alumno: ")
            self.alumnos_collection.update_one({"numero_control": numero_control}, {"$set": {"apellido": nuevo_apellido}})
        elif eleccion_campo == 3:
            nueva_carrera = input("Ingrese la nueva carrera del alumno: ")
            self.alumnos_collection.update_one({"numero_control": numero_control}, {"$set": {"carrera": nueva_carrera}})
        else:
            print("Selección inválida.")

        print("Alumno modificado con éxito.")

    def eliminar_alumno(self):
        lista_alumnos = list(self.alumnos_collection.find())

        if not lista_alumnos:
            print("No hay alumnos registrados en el sistema.")
            return

        print("Alumnos en el sistema:")
        for i, alumno in enumerate(lista_alumnos, 1):
            print(f"{i}. {alumno['nombre']} {alumno['apellido']} - Número de control: {alumno['numero_control']}")

            libro_prestado = alumno.get("libro_prestado")
            if libro_prestado:
                print(f"   Libro solicitado: {libro_prestado['nombre']} - Categoría: {libro_prestado['categoria']}")
            else:
                print("   El alumno no ha solicitado ningún libro.")

        try:
            eleccion_alumno = int(input("Seleccione el alumno a eliminar (número): "))
            alumno_a_eliminar = lista_alumnos[eleccion_alumno - 1]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        if alumno_a_eliminar.get("libro_prestado"):
            devolucion_libro = input(f"¿El alumno ha devuelto el libro '{alumno_a_eliminar['libro_prestado']['nombre']}'? (si/no): ").lower()
            if devolucion_libro != 'si':
                print("No se puede eliminar al alumno hasta que devuelva el libro.")
                return

        self.alumnos_collection.delete_one({"numero_control": alumno_a_eliminar["numero_control"]})
        print("Alumno eliminado con éxito.")

    def mostrar_categorias(self):
        categorias_unicas = self.libros_collection.distinct("categoria")

        if not categorias_unicas:
            print("No hay categorías de libros disponibles en la biblioteca.")
            return

        print("Categorías de libros existentes:")
        for i, categoria in enumerate(categorias_unicas, 1):
            print(f"{i}. {categoria}")

    def salir_del_sistema(self):
        print("Saliendo del sistema. ¡Hasta luego!")
        self.client.close()
        exit()

def main():
    connection_string = "mongodb+srv://bdata:1234@biblioteca.j9zcdza.mongodb.net/"
    db_name = "BibliotecaBigData"

    biblioteca = Biblioteca(connection_string, db_name)

    while True:
        print("\nMenú Principal:")
        print("A) Ingresar libro")
        print("B) Agregar alumno y prestar libro")
        print("C) Consultar libros")
        print("D) Mostrar libros para modificar")
        print("E) Eliminar libro")
        print("F) Consultar alumnos")
        print("G) Modificar alumno")
        print("H) Eliminar alumno")
        print("I) Mostrar categorías")
        print("X) Salir")

        opcion = input("Seleccione una opción del menú: ").upper()

        if opcion == 'A':
            biblioteca.ingresar_libro()
        elif opcion == 'B':
            biblioteca.agregar_alumno_y_prestar_libro()
        elif opcion == 'C':
            biblioteca.consultar_libros()
        elif opcion == 'D':
            biblioteca.mostrar_libros_para_modificar()
        elif opcion == 'E':
            biblioteca.eliminar_libro()
        elif opcion == 'F':
            biblioteca.consultar_alumnos()
        elif opcion == 'G':
            biblioteca.modificar_alumno()
        elif opcion == 'H':
            biblioteca.eliminar_alumno()
        elif opcion == 'I':
            biblioteca.mostrar_categorias()
        elif opcion == 'X':
            biblioteca.salir_del_sistema()
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()

    


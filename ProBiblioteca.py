from pymongo import MongoClient
from datetime import datetime

class Biblioteca:
    def __init__(self, cadena_conexion):
        # Conectar a la base de datos
        self.cliente = MongoClient(cadena_conexion)

        self.base_datos = self.cliente["BibliotecaBigData"]

        self.coleccion_libros = self.base_datos["Libros"]
        self.coleccion_alumnos = self.base_datos["Alumnos"]
        self.categorias_disponibles = [
            "Ciencia-ficción",
            "Terror",
            "Drama",
            "Romance",
            "Informática",
            "Acción"
        ]

    def ingresar_libro(self):
        nombre_libro = input("Ingrese el nombre del libro: ")

        print("Categorías de libros disponibles:")
        for i, categoria in enumerate(self.categorias_disponibles, 1):
            print(f"{i}. {categoria}")

        categoria_index = int(
            input("Seleccione la categoría del libro (número): ")) - 1
        categoria = self.categorias_disponibles[categoria_index]

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

        self.coleccion_libros.insert_one(libro)
        print("Libro ingresado con éxito.")

    def ingresar_alumno(self):
        nombre_alumno = input("Ingrese el nombre del alumno: ")
        apellido_alumno = input("Ingrese el apellido del alumno: ")
        carrera_alumno = input("Ingrese la carrera del alumno: ")
        numero_control_alumno = input(
            "Ingrese el número de control del alumno: ")

        alumno = {
            "nombre": nombre_alumno,
            "apellido": apellido_alumno,
            "carrera": carrera_alumno,
            "numero_control": numero_control_alumno,
            "libros": [],
        }

        self.coleccion_alumnos.insert_one(alumno)
        print("Alumno ingresado con éxito.")

    def consultar_libros(self):
        libros_cursor = self.coleccion_libros.find()

        lista_libros = list(libros_cursor)

        if not lista_libros:
            print("No hay libros disponibles en la biblioteca.")
        else:
            print("Libros disponibles:")
            for libro in lista_libros:
                print("\nNombre del libro:", libro["nombre"])
                print("Autor:", f"{libro['autor']['nombre']} {
                      libro['autor']['apellido']}")
                print("Categoría:", libro["categoria"])
                print("-----------------------")

    def agregar_libro_a_alumno(self):
        alumnos = list(self.coleccion_alumnos.find())
        if not alumnos:
            print("No hay alumnos registrados.")
            return
        print("Alumnos en el sistema:")
        for i, alumno in enumerate(alumnos, 1):
            print(f"{i}. {alumno['nombre']} {alumno['apellido']} ({alumno['numero_control']})")

    
        try:
            seleccion_alumno_index = int(
                input("Seleccione el número del alumno: ")) - 1
            alumno_seleccionado = alumnos[seleccion_alumno_index]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

    
        libros_disponibles = list(self.coleccion_libros.find())
        if not libros_disponibles:
            print("No hay libros disponibles.")
            return

        print("Libros disponibles:")
        for i, libro in enumerate(libros_disponibles, 1):
            print(f"{i}. {libro['nombre']} - Autor: {libro['autor']['nombre']} {libro['autor']['apellido']} - Categoría: {libro['categoria']}")


        try:
            seleccion_libro_index = int(
                input("Seleccione el número del libro: ")) - 1
            libro_seleccionado = libros_disponibles[seleccion_libro_index]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        libros_alumno = [libro['nombre']
                         for libro in alumno_seleccionado.get('libros', [])]
        if libro_seleccionado['nombre'] in libros_alumno:
            print(
                "Este libro ya está asignado al alumno. Se reemplazará automáticamente.")

            self.coleccion_alumnos.update_one({"_id": alumno_seleccionado["_id"]}, {
                                              "$pull": {"libros": {"nombre": libro_seleccionado['nombre']}}})

        fecha_prestamo = datetime.now().strftime("%Y-%m-%d")
        libro_prestamo = {
            "nombre": libro_seleccionado['nombre'],
            "autor": libro_seleccionado['autor'],
            "categoria": libro_seleccionado['categoria'],
            "fecha_prestamo": fecha_prestamo
        }

        self.coleccion_alumnos.update_one({"_id": alumno_seleccionado["_id"]}, {
                                          "$push": {"libros": libro_prestamo}})
        print("Libro asignado al alumno con éxito.")

    def consultar_alumnos(self):
        lista_alumnos = list(self.coleccion_alumnos.find())
        if not lista_alumnos:
            print("No hay alumnos registrados en el sistema.")
            return

        print("Alumnos registrados:")
        for alumno in lista_alumnos:
            print(f"Nombre: {alumno['nombre']} {alumno['apellido']} - Número de control: {alumno['numero_control']}")
            print("Libros prestados:")

        
            libros_prestados = alumno.get("libros", [])

            if libros_prestados:
                for libro in libros_prestados:
                    nombre_libro = libro.get("nombre", "Libro Desconocido")
                    print(f"- {nombre_libro}")
            
            else:
                print("Ningún libro prestado.")

            print("--------")

    def devolver_libro(self):
        numero_control = input("Ingrese el número de control del alumno: ")
        alumno = self.coleccion_alumnos.find_one(
            {"numero_control": numero_control})

        if not alumno:
            print("No existe un alumno con ese número de control.")
            return

        if not alumno.get('libros'):
            print("El alumno no tiene libros prestados.")
            return

        print("Libros prestados al alumno:")

        for i, libro in enumerate(alumno['libros'], 1):
            nombre_libro = libro['nombre']
            autor_nombre = libro['autor']['nombre']
            autor_apellido = libro['autor']['apellido']
            fecha_prestamo = libro.get('fecha_prestamo', 'Fecha desconocida')
            print(f"{i}. {nombre_libro} ({autor_nombre} {autor_apellido}) - Fecha de préstamo: {fecha_prestamo}")
            
        try:
            seleccion_libro_index = int(
                input("Seleccione el número del libro a devolver: ")) - 1
            libro_devuelto = alumno['libros'][seleccion_libro_index]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        self.coleccion_alumnos.update_one(
            {"_id": alumno["_id"]}, {"$pull": {"libros": libro_devuelto}})
        print("Libro devuelto con éxito.")

    def modificar_alumno(self):
        numero_control = input(
            "Ingrese el número de control del alumno a modificar: ")
        alumno = self.coleccion_alumnos.find_one(
            {"numero_control": numero_control})

        if not alumno:
            print("No existe un alumno con ese número de control.")
            return

        print("Información actual del alumno:")
        print(f"Nombre: {alumno['nombre']} {alumno['apellido']}")
        print(f"Carrera: {alumno['carrera']}")
        print(f"Número de control: {alumno['numero_control']}")

        try:
            campo_modificar = int(
                input("Seleccione el campo a modificar:\n1. Nombre\n2. Apellido\n3. Carrera\n"))
        except ValueError:
            print("Selección inválida.")
            return

        if campo_modificar == 1:
            nuevo_nombre = input("Ingrese el nuevo nombre del alumno: ")
            self.coleccion_alumnos.update_one(
                {"_id": alumno["_id"]}, {"$set": {"nombre": nuevo_nombre}})
            print("Nombre actualizado con éxito.")
        elif campo_modificar == 2:
            nuevo_apellido = input("Ingrese el nuevo apellido del alumno: ")
            self.coleccion_alumnos.update_one(
                {"_id": alumno["_id"]}, {"$set": {"apellido": nuevo_apellido}})
            print("Apellido actualizado con éxito.")
        elif campo_modificar == 3:
            nueva_carrera = input("Ingrese la nueva carrera del alumno: ")
            self.coleccion_alumnos.update_one(
                {"_id": alumno["_id"]}, {"$set": {"carrera": nueva_carrera}})
            print("Carrera actualizada con éxito.")
        else:
            print("Selección inválida.")

    def eliminar_libro(self):
        
        libros = list(self.coleccion_libros.find())

        if not libros:
            print("No hay libros disponibles para eliminar.")
            return

        print("Libros disponibles para eliminar:")
        for i, libro in enumerate(libros, 1):
            print(f"{i}. {libro['nombre']} - Autor: {libro['autor']['nombre']} {libro['autor']['apellido']} - Categoría: {libro['categoria']}")

       
        try:
            seleccion_libro_index = int(input("Seleccione el número del libro a eliminar: ")) - 1
            libro_seleccionado = libros[seleccion_libro_index]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        self.coleccion_libros.delete_one({"_id": libro_seleccionado["_id"]})
        print("Libro eliminado con éxito.")

        libros_disponibles = list(self.coleccion_libros.find())

        alumnos_con_libro = list(self.coleccion_alumnos.find(
            {"libros.nombre": libro_seleccionado["nombre"]}))
        for alumno in alumnos_con_libro:
            libros_alumno_actualizados = [
                libro for libro in alumno["libros"] if libro["nombre"] != libro_seleccionado["nombre"]]
            self.coleccion_alumnos.update_one(
                {"_id": alumno["_id"]}, {"$set": {"libros": libros_alumno_actualizados}})

        print("Cambios reflejados en la base de datos.")
    
    def modificar_libro(self):
    
        lista_libros = list(self.coleccion_libros.find())

        if not lista_libros:
            print("No hay libros disponibles en la biblioteca.")
            return

        print("Lista de libros disponibles:")
        for i, libro in enumerate(lista_libros, 1):
            print(f"{i}. {libro['nombre']} - Autor: {libro['autor']['nombre']} {libro['autor']['apellido']} - Categoría: {libro['categoria']}")

        try:
            seleccion_libro_index = int(input("Seleccione el número del libro que desea modificar: ")) - 1
            libro_seleccionado = lista_libros[seleccion_libro_index]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        print(f"\nLibro seleccionado: {libro_seleccionado['nombre']}")
        print("Campos disponibles para modificar:")
        print("1. Nombre del libro")
        print("2. Autor")
        print("3. Categoría")

        try:
            seleccion_campo = int(input("Seleccione el número del campo que desea modificar: "))
        except ValueError:
            print("Selección inválida. Debe ingresar un número.")
            return

        if seleccion_campo == 1:
            nuevo_nombre = input("Ingrese el nuevo nombre del libro: ")
            self.coleccion_libros.update_one({"_id": libro_seleccionado["_id"]}, {"$set": {"nombre": nuevo_nombre}})
        elif seleccion_campo == 2:
            nuevo_autor_nombre = input("Ingrese el nuevo nombre del autor: ")
            nuevo_autor_apellido = input("Ingrese el nuevo apellido del autor: ")
            self.coleccion_libros.update_one(
                {"_id": libro_seleccionado["_id"]},
                {"$set": {"autor.nombre": nuevo_autor_nombre, "autor.apellido": nuevo_autor_apellido}}
           )
        elif seleccion_campo == 3:
            nueva_categoria = input("Ingrese la nueva categoría del libro: ")
            self.coleccion_libros.update_one({"_id": libro_seleccionado["_id"]}, {"$set": {"categoria": nueva_categoria}})
        else:
            print("Selección inválida.")

        print("Libro modificado con éxito.")
        
        
        
        libro_modificado = {
            "nombre": nuevo_nombre if seleccion_campo == 1 else libro_seleccionado['nombre'],
            "autor": {
                "nombre": nuevo_autor_nombre if seleccion_campo == 2 else libro_seleccionado['autor']['nombre'],
                "apellido": nuevo_autor_apellido if seleccion_campo == 2 else libro_seleccionado['autor']['apellido'],
            },
        "categoria": nueva_categoria if seleccion_campo == 3 else libro_seleccionado['categoria'],
        }
       
        self.coleccion_alumnos.update_many(
            {"libros.nombre": libro_seleccionado['nombre']},
            {"$set": {"libros.$": libro_modificado}}
        )

    


    def eliminar_alumno(self):
        
        alumnos = list(self.coleccion_alumnos.find())

        if not alumnos:
            print("No hay alumnos registrados.")
            return

        print("Alumnos en el sistema:")
        for i, alumno in enumerate(alumnos, 1):
            print(f"Nombre: {alumno['nombre']} {
                  alumno['apellido']} ({alumno['numero_control']})")

            if alumno.get('libros'):
                print("Libros solicitados:")
                for i, libro in enumerate(alumno['libros'], 1):
                    print(f"{i}. {libro['nombre']} ({libro['autor']['nombre']} {
                          libro['autor']['apellido']})")
                print("-----------------------")
            else:
                print("Este alumno no ha solicitado libros.")
                print("-----------------------")

        
        numero_control_eliminar = input(
            "Ingrese el número de control del alumno a eliminar: ")

       
        alumno_eliminar = self.coleccion_alumnos.find_one(
            {"numero_control": numero_control_eliminar})

        if not alumno_eliminar:
            print("No existe un alumno con ese número de control.")
            return

        if alumno_eliminar.get('libros'):
            print("Primero devuelve los libros antes de eliminar al alumno.")
        else:
            
            self.coleccion_alumnos.delete_one({"_id": alumno_eliminar["_id"]})
            print("Alumno eliminado de la biblioteca.")

            
            self.coleccion_alumnos = list(self.coleccion_alumnos.find())

           
            libros_prestados = list(self.coleccion_libros.find(
                {"nombre": {"$in": [libro["nombre"] for libro in alumno_eliminar.get("libros", [])]}}))
            for libro in libros_prestados:
                alumnos_con_libro = [alumno for alumno in libro.get(
                    "alumnos", []) if alumno["numero_control"] != numero_control_eliminar]
                self.coleccion_libros.update_one(
                    {"_id": libro["_id"]}, {"$set": {"alumnos": alumnos_con_libro}})

            print("Cambios reflejados en la base de datos.")

    def mostrar_categorias(self):
        print("Categorías de libros registradas:")
        for categoria in self.categorias_disponibles:
            print(f"- {categoria}")

    def salir(self):
        print("Saliendo del sistema. ¡Hasta luego!")
        self.cliente.close()



if __name__ == "__main__":
    biblioteca = Biblioteca(
        "mongodb+srv://bdata:1234@biblioteca.j9zcdza.mongodb.net/")

    while True:
        print("Menú Principal:")
        print("1. Ingresar libro")
        print("2. Agregar alumno")
        print("3. Consultar libros")
        print("4. Agregar libro a alumno")
        print("5. Consultar alumnos")
        print("6. Devoluciones")
        print("7. Modificar libro")
        print("8. Modificar alumno")
        print("9. Eliminar libro")
        print("10. Eliminar alumno")
        print("11. Mostrar categorías")
        print("12. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            biblioteca.ingresar_libro()
        elif opcion == "2":
            biblioteca.ingresar_alumno()
        elif opcion == "3":
            biblioteca.consultar_libros()
        elif opcion == "4":
            biblioteca.agregar_libro_a_alumno()
        elif opcion == "5":
            biblioteca.consultar_alumnos()
        elif opcion == "6":
            biblioteca.devolver_libro()
        elif opcion == "7":
            biblioteca.modificar_libro()
        elif opcion == "8":
            biblioteca.modificar_alumno()
        elif opcion == "9":
            biblioteca.eliminar_libro()
        elif opcion == "10":
            biblioteca.eliminar_alumno()
        elif opcion == "11":
            biblioteca.mostrar_categorias()
        elif opcion == "12":
            biblioteca.salir()
        else:
            print("Opción no válida. Inténtalo de nuevo.")

class Autor:
    def __init__(self, nombre, apellido, nacionalidad):
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad

    def mostrar_autor(self):
        return f"{self.nombre} {self.apellido} ({self.nacionalidad})"

class Libro:
    def __init__(self, nombre, categoria, autor):
        self.nombre = nombre
        self.categoria = categoria
        self.autor = autor
        self.alumno_prestado = None

    def mostrar_libro(self):
        return f"Nombre del libro: {self.nombre}\n" \
               f"Autor: {self.autor.mostrar_autor()}\n" \
               f"Categoría: {self.categoria}\n"

class Estante:
    def __init__(self, categoria):
        self.categoria = categoria
        self.libros = []

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def eliminar_libro(self, libro):
        if libro in self.libros:
            self.libros.remove(libro)

class Biblioteca:
    def __init__(self):
        self.estantes = {
            'Ciencia-ficción': Estante('Ciencia-ficción'),
            'Terror': Estante('Terror'),
            'Drama': Estante('Drama'),
            'Historia': Estante('Historia'),
            'Informática': Estante('Informática'),
            'Acción': Estante('Acción')
        }
        self.libros = []
        self.alumnos = []

    def agregar_libro(self, nombre, categoria, autor):
        nuevo_libro = Libro(nombre, categoria, autor)
        self.libros.append(nuevo_libro)
        if categoria in self.estantes:
            self.estantes[categoria].agregar_libro(nuevo_libro)
            print("Libro ingresado con éxito.")
        else:
            print(f"La categoría '{categoria}' no existe en la biblioteca. No se pudo agregar el libro.")

    def mostrar_categorias(self):
        print("Categorías de libros disponibles:")
        for categoria in self.estantes.keys():
            print(categoria)

    def eliminar_libro(self, libro):
        if libro in self.libros:
            self.libros.remove(libro)
            self.estantes[libro.categoria].eliminar_libro(libro)

    def mostrar_libros(self):
        for estante in self.estantes.values():
            estante.libros.sort(key=lambda libro: (libro.autor.apellido, libro.categoria))
            for libro in estante.libros:
                print(libro.mostrar_libro())
                if libro.alumno_prestado is not None:
                    alumno_prestado = next(alumno for alumno in self.alumnos if alumno.libro_prestado == libro)
                    print(f"Alumno que lo tiene prestado: {alumno_prestado.nombre} ({alumno_prestado.no_control})")
                print("=" * 50)

    def agregar_alumno(self, nombre, apellido, carrera, no_control):
        nuevo_alumno = Alumno(nombre, apellido, carrera, no_control)
        self.alumnos.append(nuevo_alumno)

    def consultar_alumnos(self):
        print("Lista de alumnos y libros prestados:")
        for alumno in self.alumnos:
            print(f"Alumno: {alumno.nombre} ({alumno.no_control})")
            if alumno.libro_prestado is not None:
                print(f"Libro prestado: {alumno.libro_prestado.nombre}")
            else:
                print("No tiene libros prestados.")
            print("=" * 50)

    def eliminar_alumno(self, no_control):
        for alumno in self.alumnos:
            if alumno.no_control == no_control:
                if alumno.libro_prestado is not None:
                    devolver_libro = input(f"¿El alumno ha devuelto el libro? (S/N): ").strip().upper()
                    if devolver_libro == "S":
                        libro_devuelto = alumno.devolver_libro()
                        print(f"El libro '{libro_devuelto.nombre}' ha sido devuelto.")
                        self.alumnos.remove(alumno)
                        print(f"Alumno eliminado con éxito.")
                    else:
                        print("El alumno no puede ser eliminado si tiene libros pendientes.")
                else:
                    self.alumnos.remove(alumno)
                    print(f"Alumno eliminado con éxito.")
                return

    def modificar_alumno(self, no_control, campo, nuevo_valor):
        for alumno in self.alumnos:
            if alumno.no_control == no_control:
                if campo == "nombre":
                    alumno.nombre = nuevo_valor
                elif campo == "apellido":
                    alumno.apellido = nuevo_valor
                elif campo == "carrera":
                    alumno.carrera = nuevo_valor

class Alumno:
    def __init__(self, nombre, apellido, carrera, no_control):
        self.nombre = nombre
        self.apellido = apellido
        self.carrera = carrera
        self.no_control = no_control
        self.libro_prestado = None

    def prestar_libro(self, libro):
        if self.libro_prestado is None:
            self.libro_prestado = libro
        else:
            print(f"El alumno ya tiene un libro prestado: {self.libro_prestado.nombre}")

    def devolver_libro(self):
        if self.libro_prestado is not None:
            libro_devuelto = self.libro_prestado
            self.libro_prestado = None
            return libro_devuelto
        else:
            print("El alumno no tiene libros prestados")

def mostrar_menu():
    print("Bienvenido a la Biblioteca")
    print("Menú:")
    print("A) Ingresar libro")
    print("B) Eliminar libro")
    print("C) Modificar libro")
    print("D) Agregar alumno")
    print("E) Consultar libros")
    print("F) Modificar alumno")
    print("G) Eliminar alumno")
    print("H) Consultar alumnos")
    print("I) Mostrar categorías")
    print("X) Salir")

biblioteca = Biblioteca()

while True:
    mostrar_menu()
    opcion = input("Elija una opción: ").strip().upper()

    if opcion == 'A':
        nombre_libro = input("Nombre del libro: ")
        biblioteca.mostrar_categorias()
        categoria_libro = input("Categoría del libro: ")
        autor_nombre = input("Nombre del autor: ")
        autor_apellido = input("Apellido del autor: ")
        autor_nacionalidad = input("Nacionalidad del autor: ")
        autor_nuevo = Autor(autor_nombre, autor_apellido, autor_nacionalidad)
        biblioteca.agregar_libro(nombre_libro, categoria_libro, autor_nuevo)

    elif opcion == 'B':
        biblioteca.mostrar_libros()
        nombre_libro = input("Nombre del libro que desea eliminar: ")
        libro_eliminar = next((libro for libro in biblioteca.libros if libro.nombre == nombre_libro), None)
        if libro_eliminar:
            biblioteca.eliminar_libro(libro_eliminar)
            print(f"El libro '{nombre_libro}' ha sido eliminado.")
        else:
            print(f"No se encontró el libro '{nombre_libro}'.")

    elif opcion == 'C':
        biblioteca.mostrar_libros()
        nombre_libro = input("Nombre del libro que desea modificar: ")
        libro_modificar = next((libro for libro in biblioteca.libros if libro.nombre == nombre_libro), None)
        if libro_modificar:
            print("Seleccione el campo a modificar:")
            print("1) Nombre del libro")
            print("2) Categoría del libro")
            print("3) Nombre del autor")
            campo = input("Opción: ").strip()
            if campo == '1':
                nuevo_nombre = input("Nuevo nombre del libro: ")
                libro_modificar.nombre = nuevo_nombre
            elif campo == '2':
                biblioteca.mostrar_categorias()
                nueva_categoria = input("Nueva categoría del libro: ")
                libro_modificar.categoria = nueva_categoria
            elif campo == '3':
                nuevo_autor_nombre = input("Nuevo nombre del autor: ")
                nuevo_autor_apellido = input("Nuevo apellido del autor: ")
                nuevo_autor_nacionalidad = input("Nueva nacionalidad del autor: ")
                nuevo_autor = Autor(nuevo_autor_nombre, nuevo_autor_apellido, nuevo_autor_nacionalidad)
                libro_modificar.autor = nuevo_autor
                print("Libro modificado con éxito.")
            else:
                print("Opción no válida. No se realizó ninguna modificación.")
        else:
            print(f"No se encontró el libro '{nombre_libro}'.")

    elif opcion == 'D':
        nombre_alumno = input("Nombre del alumno: ")
        apellido_alumno = input("Apellido del alumno: ")
        carrera_alumno = input("Carrera del alumno: ")
        no_control_alumno = input("Número de control del alumno: ")
        libro_solicitado = input("Libro que solicitó el alumno: ")
        biblioteca.agregar_alumno(nombre_alumno, apellido_alumno, carrera_alumno, no_control_alumno)
        alumno = next((alumno for alumno in biblioteca.alumnos if alumno.no_control == no_control_alumno), None)
        if alumno:
            libro = next((libro for libro in biblioteca.libros if libro.nombre == libro_solicitado), None)
            if libro:
                alumno.prestar_libro(libro)
                print("Alumno agregado y libro prestado con éxito.")
            else:
                print(f"No se encontró el libro '{libro_solicitado}'.")
        else:
            print(f"No se encontró el alumno con número de control '{no_control_alumno}'.")

    elif opcion == 'E':
        biblioteca.mostrar_libros()

    elif opcion == 'F':
        no_control = input("Número de control del alumno a modificar: ")
        alumno = next((alumno for alumno in biblioteca.alumnos if alumno.no_control == no_control), None)
        if alumno:
            print("Seleccione el campo a modificar:")
            print("1) Nombre del alumno")
            print("2) Apellido del alumno")
            print("3) Carrera del alumno")
            campo = input("Opción: ").strip()
            if campo == '1':
                nuevo_nombre = input("Nuevo nombre: ")
                alumno.nombre = nuevo_nombre
            elif campo == '2':
                nuevo_apellido = input("Nuevo apellido: ")
                alumno.apellido = nuevo_apellido
            elif campo == '3':
                nueva_carrera = input("Nueva carrera: ")
                alumno.carrera = nueva_carrera
            else:
                print("Opción no válida. No se realizó ninguna modificación.")
        else:
            print(f"No se encontró el alumno con número de control '{no_control}'.")

    elif opcion == 'G':
        biblioteca.consultar_alumnos()
        no_control = input("Número de control del alumno a eliminar: ")
        alumno = next((alumno for alumno in biblioteca.alumnos if alumno.no_control == no_control), None)
        if alumno:
            devolver_libro = input(f"¿El alumno ha devuelto el libro? (S/N): ").strip().upper()
            if devolver_libro == "S":
                libro_devuelto = alumno.devolver_libro()
                print(f"El libro '{libro_devuelto.nombre}' ha sido devuelto.")
                biblioteca.alumnos.remove(alumno)
                print(f"Alumno eliminado con éxito.")
            else:
                print("El alumno no puede ser eliminado si tiene libros pendientes.")
        else:
            print(f"No se encontró el alumno con número de control '{no_control}'.")

    elif opcion == 'H':
        biblioteca.consultar_alumnos()

    elif opcion == 'I':
        biblioteca.mostrar_categorias()

    elif opcion == 'X':
        print("¡Hasta luego!")
        break

    else:
        print("Opción no válida. Por favor, elija una opción válida.")

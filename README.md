# Mario-Bross
# Clase base
class Entidad:
    def _init_(self, nombre, posicion):
        self.nombre = nombre
        self.posicion = posicion

    def mover(self, nueva_posicion):
        self.posicion = nueva_posicion

# Clase Poder
class Poder:
    def _init_(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def _str_(self):
        return f"{self.nombre}: {self.descripcion}"

# Clase Jugador
class Jugador(Entidad):
    def _init_(self, nombre, posicion, vida):
        super()._init_(nombre, posicion)
        self.vida = vida
        self.poderes = []

    def agregar_poder(self, poder):
        self.poderes.append(poder)

    def mostrar_info(self):
        print(f"Jugador: {self.nombre}")
        print(f"Posición: {self.posicion}")
        print(f"Vida: {self.vida}")
        print("Poderes:")
        for poder in self.poderes:
            print(f"  - {poder}")

# Clase Enemigo
class Enemigo(Entidad):
    def _init_(self, nombre, posicion, tipo_enemigo):
        super()._init_(nombre, posicion)
        self.tipo_enemigo = tipo_enemigo

    def mostrar_info(self):
        print(f"Enemigo: {self.nombre}")
        print(f"Tipo: {self.tipo_enemigo}")
        print(f"Posición: {self.posicion}")

# Programa principal
if _name_ == "_main_":
    # Crear jugador
    jugador = Jugador("Mario", (0, 0), 3)

    # Crear enemigos
    enemigo1 = Enemigo("Goomba1", (5, 2), "Goomba")
    enemigo2 = Enemigo("Koopa1", (7, 3), "Koopa")
    enemigos = [enemigo1, enemigo2]

    # Crear poderes
    poder1 = Poder("Fuego", "Lanza bolas de fuego")
    poder2 = Poder("Estrella", "Invencibilidad temporal")
    jugador.agregar_poder(poder1)
    jugador.agregar_poder(poder2)

    # Mover jugador
    jugador.mover((2, 1))

    # Mostrar información
    jugador.mostrar_info()
    print("\nEnemigos:")
    for enemigo in enemigos:
        enemigo.mostrar_info()

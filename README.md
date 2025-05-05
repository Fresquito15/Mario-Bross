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
        enemigo.mostrar_info()import random
from Poder import Hongo, Planta
from Personaje import Jugador

# Generación aleatoria de poderes
def generar_poderes():
    poderes = []
    tipos_hongo = ["Rojo", "Verde"]
    for i in range(10):
        tipo = random.choice(["Hongo", "Planta"])
        nombre = f"{tipo}_{i}"
        descripcion = "Da habilidades especiales"
        posX = random.randint(0, 10)
        posY = random.randint(0, 10)
        estado = "activo"
        if tipo == "Hongo":
            poder = Hongo(i, nombre, descripcion, posX, posY, estado, random.choice(tipos_hongo))
        else:
            poder = Planta(i, nombre, descripcion, posX, posY, estado)
        poderes.append(poder)
    return poderes

# Verifica colisiones entre Mario y los poderes
def verificar_colision(jugador, poderes):
    for poder in poderes:
        if (jugador.posicionX == poder.posicionX and
            jugador.posicionY == poder.posicionY and
            poder.estado == "activo"):
            jugador.recogerPoder(poder)

# Menú de opciones
def menu():
    print("\n--- Menú ---")
    print("1. Adelante")
    print("2. Atrás")
    print("3. Subir")
    print("4. Bajar")
    print("5. Salir")
    return input("Selecciona una opción: ")

# Programa principal
def main():
    mario = Jugador(1, "Mario")
    poderes = generar_poderes()

    print("\n¡Bienvenido al juego de Mario!")
    print("Encuentra y recoge poderes mientras te mueves por el mapa.")

    while True:
        opcion = menu()
        if opcion == "1":
            mario.mover(x=1)
        elif opcion == "2":
            mario.mover(x=-1)
        elif opcion == "3":
            mario.mover(y=1)
        elif opcion == "4":
            mario.mover(y=-1)
        elif opcion == "5":
            print("¡Gracias por jugar!")
            break
        else:
            print("Opción inválida.")

        verificar_colision(mario, poderes)
        print(f"Estado de Mario: posición=({mario.posicionX}, {mario.posicionY}), tamaño={mario.tamano}, vidas={mario.vidas}, dispara={mario.dispara}")

if __name__ == "__main__":
    main()


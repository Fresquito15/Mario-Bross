import pygame
import random

# Inicialización de pygame
pygame.init()
pygame.font.init()

# Constantes de la pantalla
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
LIMITE_INFERIOR = 450  # Piso debajo del cual no aparecerán objetos

# Colores
COLOR_FONDO = (135, 206, 250)  # Azul cielo
COLOR_TEXTO = (255, 255, 255)

# Fuente para textos
FUENTE = pygame.font.SysFont('Arial', 24)

# Frames por segundo
FPS = 60


class Jugador:
    def __init__(self):
        self.x = 100
        self.y = LIMITE_INFERIOR - 10
        self.ancho = 40
        self.alto = 50
        self.color = (255, 0, 0)  # Rojo
        self.vidas = 3
        self.estado = 'pequeño'  # 'pequeño' o 'grande'
        self.inmunidad = False
        self.tiempo_inmunidad = 0
        self.velocidad = 5
        self.recogidas_monedas = 0

    def dibujar(self, pantalla, imagen_pequeno, imagen_grande):
        if self.estado == 'pequeño':
            pantalla.blit(imagen_pequeno, (self.x, self.y))
        else:
            pantalla.blit(imagen_grande, (self.x, self.y))

    def mover(self, direccion):
        if direccion == "izquierda":
            self.x = max(self.x - self.velocidad, 0)
        elif direccion == "derecha":
            self.x = min(self.x + self.velocidad, ANCHO_VENTANA - self.ancho)

    def actualizar_estado(self):
        if self.inmunidad:
            self.tiempo_inmunidad -= 1 / FPS
            if self.tiempo_inmunidad <= 0:
                self.inmunidad = False

    def colisionar_con_goomba(self):
        if self.inmunidad:
            return
        if self.estado == 'grande':
            self.estado = 'pequeño'
            self.color = (255, 0, 0)  # Rojo
            self.alto = 50
            self.y = LIMITE_INFERIOR - self.alto
        elif self.estado == 'pequeño':
            if self.vidas > 1:
                self.vidas -= 1
            else:
                self.vidas = 0

    def crecer(self):
        self.estado = 'grande'
        self.color = (255, 100, 100)
        self.alto = 80
        self.y = LIMITE_INFERIOR - self.alto

    def vida_extra(self):
        self.vidas += 1

    def activar_inmunidad(self):
        self.inmunidad = True
        self.tiempo_inmunidad = 8


class Goomba:
    def __init__(self):
        self.tipo = random.choice(['café', 'negro'])
        self.color = (139, 69, 19) if self.tipo == 'café' else (0, 0, 0)
        self.ancho = 40
        self.alto = 50
        self.x = ANCHO_VENTANA
        self.y = LIMITE_INFERIOR - self.alto
        self.velocidad = 3
        self.activo = True

    def mover(self):
        self.x -= self.velocidad
        if self.x + self.ancho < 0:
            self.activo = False

    def dibujar(self, pantalla, imagen_cafe, imagen_negro):
        if self.tipo == 'café':
            pantalla.blit(imagen_cafe, (self.x, self.y))
        else:
            pantalla.blit(imagen_negro, (self.x, self.y))

    def colisiona_con(self, jugador):
        rect_goomba = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        rect_jugador = pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.alto)
        return rect_goomba.colliderect(rect_jugador)


class ObjetoBeneficioso:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activo = True

    def dibujar(self, pantalla):
        raise NotImplementedError

    def colisiona_con(self, jugador):
        if not self.activo:
            return False
        rect_jugador = pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.alto)
        distancia = ((self.x - (jugador.x + jugador.ancho // 2)) ** 2 + (self.y - (jugador.y + jugador.alto // 2)) ** 2) ** 0.5
        return distancia < self.radio + max(jugador.ancho, jugador.alto) / 4


class Moneda(ObjetoBeneficioso):
    def __init__(self, x=None, y=None):
        if x is None:
            x = random.randint(10, ANCHO_VENTANA - 10)
        if y is None:
            y = random.randint(10, LIMITE_INFERIOR - 20)
        super().__init__(x, y)
        self.radio = 10
        self.color = (255, 223, 0)

    def dibujar(self, pantalla, imagen_moneda):
        if self.activo:
            pantalla.blit(imagen_moneda, (self.x - self.radio, self.y - self.radio))


class Hongo(ObjetoBeneficioso):
    def __init__(self, tipo, posicion_fija):
        super().__init__(*posicion_fija)
        self.tipo = tipo  # 'crecimiento' o 'vida'
        self.color = (255, 0, 255) if tipo == 'crecimiento' else (0, 255, 0)
        self.radio = 15
        self.activo = False
        self.tiempo_visible = 0

    def dibujar(self, pantalla, imagen_hongo_crecimiento, imagen_hongo_vida):
        if self.activo:
            if self.tipo == 'crecimiento':
                pantalla.blit(imagen_hongo_crecimiento, (self.x - self.radio, self.y - self.radio))
            else:
                pantalla.blit(imagen_hongo_vida, (self.x - self.radio, self.y - self.radio))

    def activar(self, tiempo):
        self.activo = True
        self.tiempo_visible = tiempo

    def actualizar(self):
        if self.activo:
            self.tiempo_visible -= 1 / FPS
            if self.tiempo_visible <= 0:
                self.activo = False


class Estrella(ObjetoBeneficioso):
    def __init__(self, posicion_fija):
        super().__init__(*posicion_fija)
        self.radio = 15
        self.color = (255, 255, 255)

    def dibujar(self, pantalla, imagen_estrella):
        if self.activo:
            pantalla.blit(imagen_estrella, (self.x - self.radio, self.y - self.radio))


class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Mario Mosquera Game")
        self.clock = pygame.time.Clock()
        self.jugador = Jugador()

        # Cargar imágenes
        self.imagen_fondo = pygame.image.load("assets/images/Fondo.png")
        self.imagen_jugador_pequeno = pygame.image.load("mario pequeno.png").convert_alpha()
        self.imagen_jugador_grande = pygame.image.load("mario grande.png").convert_alpha()
        self.imagen_goomba_cafe = pygame.image.load("goomba cafe.png").convert_alpha()
        self.imagen_goomba_negro = pygame.image.load("goomba negro.png").convert_alpha()
        self.imagen_moneda = pygame.image.load("moneda.png").convert_alpha()
        self.imagen_hongo_crecimiento = pygame.image.load("Hongo rojo.png").convert_alpha()
        self.imagen_hongo_vida = pygame.image.load("Hongo verde.png").convert_alpha()
        self.imagen_estrella = pygame.image.load("estrella.png").convert_alpha()

        self.monedas = []
        self.generar_monedas()

        self.hongo_crecimiento = Hongo('crecimiento', (600, LIMITE_INFERIOR - 30))
        self.hongo_vida = Hongo('vida', (700, LIMITE_INFERIOR - 30))
        self.estrella = Estrella((650, LIMITE_INFERIOR - 30))

        self.goombas = []
        self.goombas_creados_total = 0
        self.max_goombas_simultaneos = 2
        self.max_goombas_total = 10
        self.tiempo_desde_ultimo_goomba = 0
        self.tiempo_minimo_entre_goombas = 2

        self.juego_terminado = False

    def generar_monedas(self):
        self.monedas = []
        posiciones_usadas = set()
        while len(self.monedas) < 10:
            x = random.randint(20, ANCHO_VENTANA - 20)
            y = random.randint(10, LIMITE_INFERIOR - 50)
            if all(abs(x - px) > 30 and abs(y - py) > 30 for px, py in posiciones_usadas):
                self.monedas.append(Moneda(x, y))
                posiciones_usadas.add((x, y))

    def generar_goomba(self):
        if len(self.goombas) < self.max_goombas_simultaneos and self.goombas_creados_total < self.max_goombas_total:
            nuevo_goomba = Goomba()
            self.goombas.append(nuevo_goomba)
            self.goombas_creados_total += 1

    def manejar_eventos(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.jugador.mover("izquierda")
        if keys[pygame.K_RIGHT]:
            self.jugador.mover("derecha")

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
        return True

    def actualizar(self):
        if self.juego_terminado:
            return

        self.tiempo_desde_ultimo_goomba += 1 / FPS
        if self.tiempo_desde_ultimo_goomba >= self.tiempo_minimo_entre_goombas:
            self.generar_goomba()
            self.tiempo_desde_ultimo_goomba = 0

        for goomba in self.goombas:
            goomba.mover()

        self.goombas = [g for g in self.goombas if g.activo]

        for goomba in self.goombas:
            if goomba.colisiona_con(self.jugador):
                self.jugador.colisionar_con_goomba()
                goomba.activo = False
                if self.jugador.vidas <= 0:
                    self.juego_terminado = True

        for moneda in self.monedas:
            if moneda.colisiona_con(self.jugador):
                moneda.activo = False
                self.jugador.recogidas_monedas += 1
                if self.jugador.recogidas_monedas == 10:
                    self.jugador.vida_extra()
                    self.jugador.recogidas_monedas = 0
                    self.generar_monedas()

        for hongo in [self.hongo_crecimiento, self.hongo_vida]:
            if hongo.colisiona_con(self.jugador) and hongo.activo:
                if hongo.tipo == 'crecimiento':
                    self.jugador.crecer()
                else:
                    self.jugador.vida_extra()
                hongo.activo = False

        if self.estrella.activo and self.estrella.colisiona_con(self.jugador):
            self.jugador.activar_inmunidad()
            self.estrella.activo = False

        self.hongo_crecimiento.actualizar()
        self.hongo_vida.actualizar()

        if not self.hongo_crecimiento.activo and random.random() < 1 / FPS / 20:
            self.hongo_crecimiento.activar(10)

        if not self.hongo_vida.activo and random.random() < 1 / FPS / 20:
            self.hongo_vida.activar(10)

        self.jugador.actualizar_estado()

    def dibujar(self):
        self.pantalla.fill((135, 206, 250))
        pygame.draw.rect(self.pantalla, (50, 205, 50), (0, LIMITE_INFERIOR, ANCHO_VENTANA, ALTO_VENTANA - LIMITE_INFERIOR))

        for moneda in self.monedas:
            moneda.dibujar(self.pantalla, self.imagen_moneda)

        self.hongo_crecimiento.dibujar(self.pantalla, self.imagen_hongo_crecimiento, self.imagen_hongo_vida)
        self.hongo_vida.dibujar(self.pantalla, self.imagen_hongo_crecimiento, self.imagen_hongo_vida)
        self.estrella.dibujar(self.pantalla, self.imagen_estrella)

        for goomba in self.goombas:
            goomba.dibujar(self.pantalla, self.imagen_goomba_cafe, self.imagen_goomba_negro)

        self.jugador.dibujar(self.pantalla, self.imagen_jugador_pequeno, self.imagen_jugador_grande)

        texto_vidas = FUENTE.render(f"Vidas: {self.jugador.vidas}", True, COLOR_TEXTO)
        texto_estado = FUENTE.render(f"Estado: {self.jugador.estado}", True, COLOR_TEXTO)
        texto_monedas = FUENTE.render(f"Monedas recogidas: {self.jugador.recogidas_monedas}/10", True, COLOR_TEXTO)

        self.pantalla.blit(texto_vidas, (10, 10))
        self.pantalla.blit(texto_estado, (10, 40))
        self.pantalla.blit(texto_monedas, (10, 70))

        if self.juego_terminado:
            texto_fin = FUENTE.render("¡Game over!.", True, (255, 0, 0))
            self.pantalla.blit(texto_fin, (ANCHO_VENTANA // 2 - texto_fin.get_width() // 2, ALTO_VENTANA // 2))

        pygame.display.flip()

    def correr(self):
        ejecutando = True
        while ejecutando:
            self.clock.tick(FPS)
            ejecutando = self.manejar_eventos()

            if self.juego_terminado:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    ejecutando = False
                self.dibujar()
                continue

            self.actualizar()
            self.dibujar()


if __name__ == "__main__":
    juego = Juego()
    juego.correr()
    pygame.quit()

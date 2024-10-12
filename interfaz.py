import pygame
import random
import os
import time
import sys

pygame.init()

# Confi pantalla
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Blackjack")

VERDE_MESA = (34, 139, 34)
BLANCO = (255, 255, 255)
DORADO = (255, 215, 0)
TRANSPARENTE = (0, 0, 0, 128)

fuente = pygame.font.Font(None, 48)
fuente_pequena = pygame.font.Font(None, 36)

# Botón "Nueva Partida"
boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50)

def crear_baraja():
    """Crea y mezcla la baraja."""
    baraja = [(valor, palo) for valor in range(1, 12) for palo in ['♠', '♥', '♦', '♣']]
    random.shuffle(baraja)
    return baraja

def cargar_imagen_carta(valor, palo):
    """Carga y ajusta la imagen correspondiente a una carta."""
    nombre_archivo = f"{valor}{palo}.png"
    if hasattr(sys, '_MEIPASS'):
        ruta = os.path.join(sys._MEIPASS, "cartas", nombre_archivo)
    else:
        ruta = os.path.join("cartas", nombre_archivo)
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (80, 120))

def calcular_puntaje(cartas):
    """Calcula el puntaje de una mano considerando la flexibilidad del As."""
    total = sum(min(10, valor) for valor, _ in cartas)
    ases = sum(1 for valor, _ in cartas if valor == 1)

    while ases > 0 and total + 10 <= 21:
        total += 10
        ases -= 1

    return total

def repartir_carta():
    """Saca una carta de la baraja."""
    return baraja.pop()

def mostrar_cartas(cartas, x, y):
    """Dibuja las cartas en pantalla."""
    for i, (valor, palo) in enumerate(cartas):
        if valor == "?":
            imagen = pygame.image.load(os.path.join("cartas", "carta_oculta.png"))
            imagen = pygame.transform.scale(imagen, (80, 120))
        else:
            imagen = cargar_imagen_carta(valor, palo)
        pantalla.blit(imagen, (x + i * 90, y))

def mostrar_texto(texto, x, y):
    """Muestra un texto en la pantalla."""
    label = fuente_pequena.render(texto, True, BLANCO)
    pantalla.blit(label, (x, y))

def mensaje_superpuesto(texto, boton=False):
    """Muestra un mensaje sobre la interfaz con un botón opcional."""
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill(TRANSPARENTE)
    mensaje = fuente.render(texto, True, DORADO)
    overlay.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
    pantalla.blit(overlay, (0, 0))

    if boton:
        pygame.draw.rect(pantalla, DORADO, boton_rect)
        texto_boton = fuente_pequena.render("Nueva Partida", True, BLANCO)
        pantalla.blit(texto_boton, (boton_rect.x + 25, boton_rect.y + 10))

    pygame.display.flip()

def turno_dealer(cartas_dealer):
    """Simula el turno del dealer."""
    while calcular_puntaje(cartas_dealer) < 17:
        cartas_dealer.append(repartir_carta())
        actualizar_pantalla(cartas_dealer, ocultar_dealer=False)
        time.sleep(1)

def actualizar_pantalla(cartas_dealer, ocultar_dealer=True):
    """Actualiza la pantalla con las cartas y puntajes."""
    pantalla.fill(VERDE_MESA)
    mostrar_texto("Tú", 50, 350)
    mostrar_cartas(cartas_jugador, 50, 400)
    mostrar_texto("Dealer", 50, 50)
    
    if ocultar_dealer:
        mostrar_cartas(cartas_dealer[:1], 50, 100)
    else:
        mostrar_cartas(cartas_dealer, 50, 100)

    pygame.display.flip()

def iniciar_ronda():
    """Inicia una nueva ronda."""
    global cartas_jugador, cartas_dealer, baraja, nueva_partida
    baraja = crear_baraja()
    cartas_jugador = [repartir_carta(), repartir_carta()]
    cartas_dealer = [repartir_carta(), repartir_carta()]
    nueva_partida = False  # No se inicia una nueva ronda hasta que el jugador lo indique

def manejar_fin_de_partida(mensaje):
    """Muestra el mensaje de fin de partida y espera a que el jugador haga clic en 'Nueva Partida'."""
    mensaje_superpuesto(mensaje, boton=True)
    esperando_nueva_partida = True

    while esperando_nueva_partida:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    iniciar_ronda()
                    esperando_nueva_partida = False

# Inicialización del juego
cartas_jugador = []
cartas_dealer = []
jugando = True
nueva_partida = False
iniciar_ronda()

# Bucle principal
while True:
    actualizar_pantalla(cartas_dealer)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
            pygame.quit()
            exit()

        if evento.type == pygame.KEYDOWN:
            if not nueva_partida:  # Solo permite pedir o plantarse si no está esperando nueva partida
                if evento.key == pygame.K_p:
                    cartas_jugador.append(repartir_carta())
                    if calcular_puntaje(cartas_jugador) > 21:
                        manejar_fin_de_partida("¡Te pasaste! Pierdes.")

                if evento.key == pygame.K_s:
                    turno_dealer(cartas_dealer)
                    puntaje_jugador = calcular_puntaje(cartas_jugador)
                    puntaje_dealer = calcular_puntaje(cartas_dealer)

                    if puntaje_dealer > 21 or puntaje_jugador > puntaje_dealer:
                        manejar_fin_de_partida("¡Ganaste!")
                    elif puntaje_jugador < puntaje_dealer:
                        manejar_fin_de_partida("¡Perdiste!")
                    else:
                        manejar_fin_de_partida("¡Empate!")
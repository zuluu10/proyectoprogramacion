import pygame
from sys import exit
import math

pygame.init()

W, H = 1000, 600
PANTALLA = pygame.display.set_mode((W, H))
pygame.display.set_caption('Bolirana')
clock = pygame.time.Clock()

# Cargar icono
icono = pygame.image.load('imagenes/icon.png')
pygame.display.set_icon(icono)

# Fondo juego
fondo_surface = pygame.image.load('imagenes/Fondo1.png').convert()
fondo_surface = pygame.transform.scale(fondo_surface, (1000, 600))

# Canica
canica = pygame.image.load('imagenes/canica.png')
canica = pygame.transform.scale(canica, (26.5, 23.3))
canica_rect = canica.get_rect()

# Personaje
quieto = pygame.image.load('imagenes/Quieto/Idle.png')
quieto = pygame.transform.scale(quieto, (400, 324))

# Animaciones
animaciones = {
    'quieto': [quieto],
    'caminaDerecha': [pygame.transform.scale(pygame.image.load(f'imagenes/Caminando/Walk{i}.png'), (400, 324)) for i in range(1, 9)],
    'caminaIzquierda': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'imagenes/Caminando/Walk{i}.png'), (400, 324)), True, False) for i in range(1, 9)],
    'salto': [pygame.transform.scale(pygame.image.load(f'imagenes/Salto/Jump-{i}.png'), (400, 324)) for i in range(1, 9)],
    'lanzamiento': [pygame.transform.scale(pygame.image.load(f'imagenes/Attack/Attack_{i}.png'), (400, 324)) for i in range(1, 10)],
}

# Variables de personaje
x, px, py, ancho, velocidad = 0, 50, 200, 40, 15
salto, cuentaSalto, cuentaSalto_lista = False, 10, 0
izquierda, derecha, lanzado, cuentaLanzamiento = False, False, False, 0
cuentaPasos = 0

# Variables de canica
canica_lanzada, canica_velocidad, canica_angulo, canica_tiempo = False, 0, 0, 0

# Variables de lanzamiento
lanzamiento_completado = False

def calcular_trayectoria(fuerza, angulo, tiempo):
    g = 9.81  # Aceleración debida a la gravedad
    angulo_rad = math.radians(angulo)
    x = fuerza * math.cos(angulo_rad) * tiempo
    y = fuerza * math.sin(angulo_rad) * tiempo - 0.5 * g * tiempo ** 2
    return x, y

def dibujar_trayectoria(pantalla, fuerza, angulo):
    puntos = []
    for t in range(0, 70, 5):
        tiempo = t / 10
        x, y = calcular_trayectoria(fuerza, angulo, tiempo)
        if 0 <= 50 + x <= 800 and 0 <= 300 - y <= 400:
            puntos.append((50 + x, 300 - y))
        else:
            break
    for punto in puntos:
        pygame.draw.circle(pantalla, (255, 255, 255), (int(punto[0]), int(punto[1])), 3)

def recargaPantalla():
    global cuentaPasos, lanzado, cuentaLanzamiento, salto, cuentaSalto, cuentaSalto_lista, canica_lanzada, canica_tiempo, lanzamiento_completado
    
    # Animación de pasos
    if cuentaPasos + 1 >= len(animaciones['caminaDerecha']):
        cuentaPasos = 0
    if izquierda:
        PANTALLA.blit(animaciones['caminaIzquierda'][cuentaPasos // 1], (px, py))
        cuentaPasos += 1
    elif derecha:
        PANTALLA.blit(animaciones['caminaDerecha'][cuentaPasos // 1], (px, py))
        cuentaPasos += 1
    elif salto:
        if cuentaSalto_lista < len(animaciones['salto']):
            PANTALLA.blit(animaciones['salto'][cuentaSalto_lista], (px, py))
            cuentaSalto_lista += 1
        else:
            PANTALLA.blit(animaciones['salto'][-1], (px, py))
    elif lanzado and not lanzamiento_completado:
        if cuentaLanzamiento < len(animaciones['lanzamiento']):
            PANTALLA.blit(animaciones['lanzamiento'][cuentaLanzamiento], (px, py))
            cuentaLanzamiento += 1
        else:
            lanzado = False
            cuentaLanzamiento = 0
            canica_lanzada = True
            canica_tiempo = 0
            lanzamiento_completado = True
            PANTALLA.blit(animaciones['quieto'][0], (px, py))
    else:
        PANTALLA.blit(animaciones['quieto'][0], (px, py))
    
    # Actualizar la posición de la canica
    if canica_lanzada:
        canica_tiempo += 0.1
        x, y = calcular_trayectoria(canica_velocidad, canica_angulo, canica_tiempo)
        canica_rect.x = px + x + 260
        canica_rect.y = py - y + 150
        PANTALLA.blit(canica, canica_rect)
    else:
        PANTALLA.blit(canica, (px + 180, py + 180))
    
    pygame.display.update()

ejecuta = True

while ejecuta:
    clock.tick(15)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecuta = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                lanzado = True
                cuentaLanzamiento = 0
                canica_velocidad = 80
                canica_angulo = 30
            if event.button == 4:
                pass  # Rueda del ratón arriba
            if event.button == 5:
                pass  # Rueda del ratón abajo
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] and px > -100:
        px -= velocidad
        izquierda = True
        derecha = False
    elif keys[pygame.K_d] and px < 900 - velocidad - ancho:
        px += velocidad
        izquierda = False
        derecha = True
    else:
        izquierda = False
        derecha = False
        cuentaPasos = 0
    
    if keys[pygame.K_w] and py > 200:
        py -= velocidad
    if keys[pygame.K_s] and py < 300:
        py += velocidad
    
    if not salto:
        if keys[pygame.K_SPACE]:
            salto = True
            izquierda = False
            derecha = False
            cuentaPasos = 0
    else:
        if cuentaSalto >= -10:
            py -= cuentaSalto * 3
            cuentaSalto -= 1
        else:
            cuentaSalto = 10
            salto = False
            cuentaSalto_lista = 0
    
    PANTALLA.blit(fondo_surface, (0, 0))
    recargaPantalla()
    
pygame.quit()


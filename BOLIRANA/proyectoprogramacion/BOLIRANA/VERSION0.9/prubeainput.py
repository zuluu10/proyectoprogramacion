import pygame
import math

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lanzamiento de Proyectiles")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Parámetros del proyectil
pos_inicial = (100, 500)
velocidad_inicial = 0
angulo_inicial = 45
gravedad = 9.81

# Función para calcular la trayectoria del proyectil
def calcular_trayectoria(fuerza, angulo, tiempo):
    angulo_rad = math.radians(angulo)
    x = fuerza * math.cos(angulo_rad) * tiempo
    y = (fuerza * math.sin(angulo_rad) * tiempo) - (0.5 * gravedad * tiempo ** 2)
    return x, y

# Función para dibujar la trayectoria
def dibujar_trayectoria(pantalla, fuerza, angulo):
    puntos = []
    for t in range(0, 70, 2):
        tiempo = t / 5
        x, y = calcular_trayectoria(fuerza, angulo, tiempo)
        if 0 <= pos_inicial[0] + x <= ANCHO and 0 <= pos_inicial[1] - y <= ALTO:
            puntos.append((pos_inicial[0] + x, pos_inicial[1] - y))
        else:
            break
    for punto in puntos:
        pygame.draw.circle(pantalla, BLANCO, (int(punto[0]), int(punto[1])), 3)

# Bucle principal
corriendo = True
arrastrando = False
fuerza = 0
angulo = angulo_inicial

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            arrastrando = True
            inicio_arrastre = pygame.mouse.get_pos()
        elif evento.type == pygame.MOUSEBUTTONUP:
            arrastrando = False
            final_arrastre = pygame.mouse.get_pos()
            dx = final_arrastre[0] - inicio_arrastre[0]
            dy = final_arrastre[1] - inicio_arrastre[1]
            fuerza = math.sqrt(dx ** 2 + dy ** 2) / 10
            angulo = math.degrees(math.atan2(-dy, dx))

    PANTALLA.fill(NEGRO)
    
    if arrastrando:
        actual_pos = pygame.mouse.get_pos()
        pygame.draw.line(PANTALLA, BLANCO, inicio_arrastre, actual_pos, 2)
        dx = actual_pos[0] - inicio_arrastre[0]
        dy = actual_pos[1] - inicio_arrastre[1]
        fuerza = math.sqrt(dx ** 2 + dy ** 2) / 10
        angulo = math.degrees(math.atan2(-dy, dx))
        dibujar_trayectoria(PANTALLA, fuerza, angulo)

    pygame.draw.circle(PANTALLA, BLANCO, pos_inicial, 5)
    dibujar_trayectoria(PANTALLA, fuerza, angulo)

    pygame.display.flip()

pygame.quit()

import pygame
from sys import exit
import math

pygame.init()

# Constantes
W, H = 1000, 600
VELOCIDAD = 15
GRAVEDAD = 1
FUERZA_INICIAL = 50
FUERZA_MAXIMA = 100
FUERZA_MINIMA = 0
INCREMENTO_FUERZA = 1
INTERVALO_TIEMPO = 0.2
ALTURA_SALTO = 10
PERSONAJE_OFFSET_X = 280
PERSONAJE_OFFSET_Y = 180
CANICA_DIMENSIONES = (17.6, 15.53)
PERSONAJE_DIMENSIONES = (400, 324)

# Configuración de la pantalla
PANTALLA = pygame.display.set_mode((W, H))
pygame.display.set_caption('Bolirana')
icono = pygame.image.load('imagenes/icon.png')
pygame.display.set_icon(icono)

# Fondo del juego
fondo_surface = pygame.image.load('imagenes/Fondo1.png').convert()
fondo_surface = pygame.transform.scale(fondo_surface, (W, H))

# Canica
canica = pygame.image.load('imagenes/canica.png').convert_alpha()
canica = pygame.transform.scale(canica, CANICA_DIMENSIONES)

# Bolirana
bolirana = pygame.image.load('imagenes/bolirana.png').convert_alpha()
bolirana = pygame.transform.flip(bolirana, True, False)
bolirana = pygame.transform.scale(bolirana, (400,400))

# Personaje
quieto = pygame.image.load('imagenes/Quieto/Idle.png')
quieto = pygame.transform.scale(quieto, PERSONAJE_DIMENSIONES)

quieto_canica = pygame.image.load('imagenes/Quieto/Idle_canica.png')
quieto_canica = pygame.transform.scale(quieto_canica, PERSONAJE_DIMENSIONES)

camina = [pygame.transform.scale(pygame.image.load(f'imagenes/Caminando/Walk{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 9)]
camina_izq = [pygame.transform.flip(img, True, False) for img in camina]

lanzamiento = [pygame.transform.scale(pygame.image.load(f'imagenes/imagenes-lanzamiento/Attack_{i}.png'), PERSONAJE_DIMENSIONES) for i in range(2, 10)]

salto_lista = [pygame.transform.scale(pygame.image.load(f'imagenes/Salto/Jump-{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 9)]

# Variables del personaje y juego
px, py = 50, 200
salto = False
cuentaSalto = ALTURA_SALTO
cuentaSalto_lista = 0

izquierda = False
derecha = False

lanzado = False
cuentaLanzamiento = 0
cuentaPasos = 0

canica_lanzada = False
canica_x = 0
canica_y = 0
canica_vx = 0
canica_vy = 0

fuerza_lanzamiento = FUERZA_INICIAL

# Fuente para texto
font = pygame.font.Font(None, 36)

def lanzar_canica(px, py, angulo_lanzamiento, fuerza_lanzamiento):
    global canica_lanzada, canica_x, canica_y, canica_vx, canica_vy
    canica_lanzada = True
    canica_x = px + PERSONAJE_OFFSET_X
    canica_y = py + PERSONAJE_OFFSET_Y

    radianes = math.radians(angulo_lanzamiento)
    canica_vx = fuerza_lanzamiento * math.cos(radianes)
    canica_vy = -fuerza_lanzamiento * math.sin(radianes)

def calcular_trayectoria(px, py, angulo_lanzamiento, fuerza_lanzamiento):
    trayectoria = []
    tiempo = 0
    x_inicial = px + PERSONAJE_OFFSET_X
    y_inicial = py + PERSONAJE_OFFSET_Y
    radianes = math.radians(angulo_lanzamiento)
    vx = fuerza_lanzamiento * math.cos(radianes)
    vy = -fuerza_lanzamiento * math.sin(radianes)
    while tiempo < 2:  # Calcular la trayectoria para los primeros 2 segundos
        x = x_inicial + vx * tiempo
        y = y_inicial + vy * tiempo + 0.5 * GRAVEDAD * tiempo**2
        if y > H:
            break
        trayectoria.append((x, y))
        tiempo += INTERVALO_TIEMPO  # Aumentar el intervalo de tiempo para espaciar más los puntos
    return trayectoria

def recargaPantalla():
    global cuentaPasos, lanzado, cuentaLanzamiento, salto, cuentaSalto, cuentaSalto_lista, px, py, izquierda, derecha, canica_lanzada, canica_x, canica_y, canica_vx, canica_vy, canica_pos, angulo_lanzamiento, fuerza_lanzamiento

    # Actualizar la animación del personaje
    if cuentaPasos + 1 >= len(camina):
        cuentaPasos = 0

    if izquierda:
        PANTALLA.blit(camina_izq[cuentaPasos // 1], (px, py))
        cuentaPasos += 1
        canica_pos = (px + 190, py + 180) 
    elif derecha:
        PANTALLA.blit(camina[cuentaPasos // 1], (px, py))
        cuentaPasos += 1
        canica_pos = (px + 190, py + 180)
    elif salto:
        if cuentaSalto_lista < len(salto_lista):
            PANTALLA.blit(salto_lista[cuentaSalto_lista], (px, py))
            cuentaSalto_lista += 1
            canica_pos = (px + 200, py + 220)
        else:
            PANTALLA.blit(salto_lista[-1], (px, py))
            canica_pos = (px + 200, py + 220)
    elif lanzado:
        if cuentaLanzamiento >= len(lanzamiento):
            lanzado = False
            cuentaLanzamiento = 0
        else:
            PANTALLA.blit(lanzamiento[cuentaLanzamiento // 1], (px, py))
            cuentaLanzamiento += 1
    else:
        PANTALLA.blit(quieto, (px, py))

    # Actualizar la posición de la canica si está lanzada
    if canica_lanzada:
        canica_x += canica_vx
        canica_y += canica_vy
        canica_vy += GRAVEDAD

        if canica_y > H:
            canica_lanzada = False

        PANTALLA.blit(canica, (canica_x, canica_y))

    # Dibujar línea de ángulo de lanzamiento
    if ajustando_angulo:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(PANTALLA, (255, 0, 0), (px + PERSONAJE_OFFSET_X, py + PERSONAJE_OFFSET_Y), (mouse_x, mouse_y), 2)

    # Calcular y dibujar la trayectoria inicial del balín
    trayectoria = calcular_trayectoria(px, py, angulo_lanzamiento, fuerza_lanzamiento)
    for punto in trayectoria:
        pygame.draw.circle(PANTALLA, (255, 255, 255), (int(punto[0]), int(punto[1])), 3)  # Color blanco

    # Mostrar ángulo y fuerza en la pantalla
    angulo_texto = font.render(f"Ángulo: {int(angulo_lanzamiento)}°", True, (255, 255, 255))
    PANTALLA.blit(angulo_texto, (10, 10))

    fuerza_texto = font.render(f"Fuerza: {fuerza_lanzamiento}", True, (255, 255, 255))
    PANTALLA.blit(fuerza_texto, (10, 50))

    # Dibujar la barra de fuerza
    barra_rect = pygame.Rect(10, 90, fuerza_lanzamiento * 2, 20)
    pygame.draw.rect(PANTALLA, (0, 255, 0), barra_rect)

    pygame.display.update()

# Configuración del reloj del juego
RELOJ = pygame.time.Clock()

# Variables del juego
ejecuta = True
angulo_lanzamiento = 45
ajustando_angulo = False

# Bucle principal del juego
while ejecuta:
    RELOJ.tick(24)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecuta = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                ajustando_angulo = True
            elif event.button == 4:  # Rueda del ratón hacia arriba
                angulo_lanzamiento += 1
            elif event.button == 5:  # Rueda del ratón hacia abajo
                angulo_lanzamiento -= 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                ajustando_angulo = False
        elif event.type == pygame.MOUSEMOTION:
            if ajustando_angulo:
                mouse_x, mouse_y = event.pos
                dx = mouse_x - (px + PERSONAJE_OFFSET_X)
                dy = (py + PERSONAJE_OFFSET_Y) - mouse_y
                angulo_lanzamiento = math.degrees(math.atan2(dy, dx))

    keys = pygame.key.get_pressed()  # Realiza acciones de las teclas manteniéndolas pulsadas. Repite el movimiento.

    # Incrementar y decrementar la fuerza con las teclas de flecha arriba y abajo
    if keys[pygame.K_UP]:
        fuerza_lanzamiento = min(fuerza_lanzamiento + INCREMENTO_FUERZA, FUERZA_MAXIMA)  # Aumentar la fuerza hasta un máximo de 100
    if keys[pygame.K_DOWN]:
        fuerza_lanzamiento = max(fuerza_lanzamiento - INCREMENTO_FUERZA, FUERZA_MINIMA)  # Disminuir la fuerza hasta un mínimo de 0

    # Tecla X: lanzamiento de la canica
    if keys[pygame.K_x]:
        lanzado = True  # comienza la animación del lanzamiento
        izquierda = False
        derecha = False
        cuentaPasos = 0
        lanzar_canica(px, py, angulo_lanzamiento, fuerza_lanzamiento)  # llamamos la función lanzar_canica con el ángulo actual

    # Tecla A: movimiento a la izquierda
    if keys[pygame.K_a] and px > -200:
        px -= VELOCIDAD
        izquierda = True
        derecha = False

    # Tecla D: movimiento a la derecha
    elif keys[pygame.K_d] and px < 900 - VELOCIDAD - 40:  # márgenes de tope para que el personaje no se salga de la pantalla
        px += VELOCIDAD
        izquierda = False
        derecha = True
        
    # Tecla W: movimiento hacia arriba
    elif keys[pygame.K_w] and py > 200:  # margen de límite
        py -= VELOCIDAD
        derecha = True
        
    # Tecla S: movimiento hacia abajo
    elif keys[pygame.K_s] and py < 300:
        py += VELOCIDAD
        derecha = True    
        
    # personaje quieto    
    else:
        izquierda = False
        derecha = False
        cuentaPasos = 0

    # Tecla Space: Salto
    if not salto:  # verificamos si el personaje no está saltando
        if keys[pygame.K_SPACE]:
            salto = True  # personaje comenzó el salto
            izquierda = False
            derecha = False
            cuentaPasos = 0
    else:
        # si el salto es true, el personaje está en el aire
        # el salto se controla con la variable cuentaSalto que empieza en 10 y decrece hasta -10.
        if cuentaSalto >= -10:
            py -= cuentaSalto * 3  # le restamos cuentaSalto * 3 a la posición del personaje en y. RECORDAR QUE AL RESTAR ESTAMOS SUBIENDO EL PERSONAJE
            cuentaSalto -= 1  # restamos cuentaSalto en cada ciclo para ir iterando en la animación
        else:
            cuentaSalto = ALTURA_SALTO  # resetamos para el próximo salto
            salto = False
            cuentaSalto_lista = 0  # Resetear el índice de imágenes del salto para la próxima animación

    # Dibujar el fondo y actualizar la pantalla
    PANTALLA.blit(fondo_surface, (0, 0))
    PANTALLA.blit(bolirana, (570, 190))
    recargaPantalla()  # Actualizar y redibujar todos los elementos de la pantalla

pygame.quit()



    

    
    


    



       




   

import pygame
from sys import exit
import math
import random
import time
import threading

pygame.init()
pygame.time.Clock


# Constantes
W, H = 1000, 600
VELOCIDAD = 15
GRAVEDAD = 1
FUERZA_INICIAL = 20
FUERZA_MAXIMA = 100
FUERZA_MINIMA = 15
INCREMENTO_FUERZA = 1
INTERVALO_TIEMPO = 0.2
ALTURA_SALTO = 10
PERSONAJE_OFFSET_X = 280
PERSONAJE_OFFSET_Y = 180
CANICA_DIMENSIONES = (14.6, 12.53)
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
canica_rect = canica.get_rect()

# Bolirana
bolirana = pygame.image.load('imagenes/bolirana1.png').convert_alpha()
bolirana = pygame.transform.flip(bolirana, True, False)
bolirana = pygame.transform.scale(bolirana, (400,400))

# Ranas 
rana1 = pygame.image.load('imagenes/green.png').convert_alpha()
rana1 = pygame.transform.scale(rana1, (39.1,40.8))
rana1_rect = rana1.get_rect(topleft=(700,380))

rana2 = pygame.image.load('imagenes/silver.png').convert_alpha()
rana2 = pygame.transform.scale(rana2, (32.7, 33.86))
rana2_rect = rana2.get_rect(topleft=(770,370))

rana3 = pygame.image.load('imagenes/golden.png').convert_alpha()
rana3 = pygame.transform.scale(rana3, (24.55, 25.44))
rana3_rect = rana3.get_rect(topleft=(820,360))

# Personaje
quieto = pygame.image.load('imagenes/Quieto/Idle.png')
quieto = pygame.transform.scale(quieto, PERSONAJE_DIMENSIONES)

quieto_canica = pygame.image.load('imagenes/Quieto/Idle_canica.png')
quieto_canica = pygame.transform.scale(quieto_canica, PERSONAJE_DIMENSIONES)

camina = [pygame.transform.scale(pygame.image.load(f'imagenes/Caminando/Walk{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 9)]
camina_izq = [pygame.transform.flip(img, True, False) for img in camina]

lanzamiento = [pygame.transform.scale(pygame.image.load(f'imagenes/imagenes-lanzamiento/Attack_{i}.png'), PERSONAJE_DIMENSIONES) for i in range(2, 10)]

salto_lista = [pygame.transform.scale(pygame.image.load(f'imagenes/Salto/Jump-{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 9)]

#menú
play = pygame.image.load('menu/play.png').convert_alpha()
play.set_colorkey((0,0,0))

help = pygame.image.load('menu/help.png').convert_alpha()

quit = pygame.image.load('menu/quit.png').convert_alpha()

controles = pygame.image.load('menu/controles.png').convert_alpha()
controles = pygame.transform.scale(controles , (W,H))

volver_button = pygame.image.load('menu/back-button.png').convert_alpha()
volver_button = pygame.transform.scale(volver_button, (200,200))

# Clase de los botones
class Boton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        # Dibujar el botón en la pantalla
        PANTALLA.blit(self.image, (self.rect.x, self.rect.y))
    
    def is_clicked(self):
        # Obtener posición del mouse y verificar si se hace clic en el botón
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]  # Obtener estado del botón izquierdo del mouse
        
        if self.rect.collidepoint(pos) and click:
            return True
        return False
    
# Crear las instancias de los botones
botonplay = Boton(100, 0, play)
botonhelp = Boton(100, 150, help)
botonquit = Boton(100, 300, quit)
botonback = Boton(50,50, volver_button)

background = pygame.image.load("menu/background.png").convert()   

#musica
pygame.mixer.init()
lista_musica_fondo = [(pygame.mixer.Sound(f"sonidos/musica/cancion{i}.mp3")) for i in range(1,9)]

#canciones
cambiar_cancion = threading.Event()
muted = False

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

puntaje = 0  # Variable to keep track of the score
intentos_restantes = 5  # Variable to keep track of remaining attempts

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS",25)



def reproducir_musica_aleatoria_indefinidamente(lista_musica_fondo, cambiar_musica_event):
    global muted
    while True:
        random.shuffle(lista_musica_fondo)
        for sonido in lista_musica_fondo:
            sonido.play()
            # Esperar hasta que el sonido termine de reproducirse o se presione "N", o se mutee con "M"
            while pygame.mixer.get_busy():
                if cambiar_musica_event.is_set():
                    sonido.stop() 
                    cambiar_musica_event.clear()
                    break
                time.sleep(0.1)
                if muted:
                    pygame.mixer.Sound.set_volume(sonido, 0)
                else:
                    pygame.mixer.Sound.set_volume(sonido, 1)


# Empezar musica en un hilo separado
threading.Thread(target=reproducir_musica_aleatoria_indefinidamente, args=(lista_musica_fondo, cambiar_cancion), daemon=True).start()

def lanzar_canica(px, py, angulo_lanzamiento, fuerza_lanzamiento):
    global canica_lanzada, canica_x, canica_y, canica_vx, canica_vy, intentos_restantes
    if intentos_restantes > 0 and not canica_lanzada:
        canica_lanzada = True
        canica_x = px + PERSONAJE_OFFSET_X
        canica_y = py + PERSONAJE_OFFSET_Y

        radianes = math.radians(angulo_lanzamiento)
        canica_vx = fuerza_lanzamiento * math.cos(radianes)
        canica_vy = -fuerza_lanzamiento * math.sin(radianes)

        intentos_restantes -= 1

        

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

# Create masks for the marble and frogs
canica_mask = pygame.mask.from_surface(canica)
rana1_mask = pygame.mask.from_surface(rana1)
rana2_mask = pygame.mask.from_surface(rana2)
rana3_mask = pygame.mask.from_surface(rana3)

def recargaPantalla():
    global cuentaPasos, lanzado, cuentaLanzamiento, salto, cuentaSalto, cuentaSalto_lista, px, py, izquierda, derecha, canica_lanzada, canica_x, canica_y, canica_vx, canica_vy, canica_pos, angulo_lanzamiento, fuerza_lanzamiento, puntaje, intentos_restantes

    # Update the character animation
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

    # Update marble position if launched
    if canica_lanzada:
        canica_x += canica_vx
        canica_y += canica_vy
        canica_vy += GRAVEDAD

        # Update the position of the marble's rect
        canica_rect.topleft = (canica_x, canica_y)

        # Check for precise pixel-perfect collisions with frogs
        offset_rana1 = (rana1_rect.x - canica_rect.x, rana1_rect.y - canica_rect.y)
        offset_rana2 = (rana2_rect.x - canica_rect.x, rana2_rect.y - canica_rect.y)
        offset_rana3 = (rana3_rect.x - canica_rect.x, rana3_rect.y - canica_rect.y)

        collision_rana1 = canica_mask.overlap(rana1_mask, offset_rana1)
        collision_rana2 = canica_mask.overlap(rana2_mask, offset_rana2)
        collision_rana3 = canica_mask.overlap(rana3_mask, offset_rana3)

        if collision_rana1:
            puntaje += 100
            canica_lanzada = False  # Reset marble if it hits a frog
            
        elif collision_rana2:
            puntaje += 200
            canica_lanzada = False
            
        elif collision_rana3:
            puntaje+= 500
            canica_lanzada = False        

        if canica_y > H:
            canica_lanzada = False

        PANTALLA.blit(canica, (canica_x, canica_y))

    # Draw launch angle line
    if ajustando_angulo:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(PANTALLA, (255, 0, 0), (px + PERSONAJE_OFFSET_X, py + PERSONAJE_OFFSET_Y), (mouse_x, mouse_y), 2)

    # Calculate and draw marble trajectory
    trayectoria = calcular_trayectoria(px, py, angulo_lanzamiento, fuerza_lanzamiento)
    for punto in trayectoria:
        pygame.draw.circle(PANTALLA, (255, 255, 255), (int(punto[0]), int(punto[1])), 3)  # White color

    # Display angle and force on screen
    angulo_texto = font.render(f"Ángulo: {int(angulo_lanzamiento)}°", True, (255, 255, 255))
    PANTALLA.blit(angulo_texto, (10, 10))

    fuerza_texto = font.render(f"Fuerza: {fuerza_lanzamiento}", True, (255, 255, 255))
    PANTALLA.blit(fuerza_texto, (10, 50))

    # Draw force bar
    barra_rect = pygame.Rect(10, 90, fuerza_lanzamiento * 2, 20)
    pygame.draw.rect(PANTALLA, (0, 255, 0), barra_rect)

    # Display score on screen
    puntaje_texto = font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    PANTALLA.blit(puntaje_texto, (W - 200, 10))

    # Display remaining attempts on screen
    intentos_texto = font.render(f"Intentos restantes: {intentos_restantes}", True, (255, 255, 255))
    PANTALLA.blit(intentos_texto, (W - 260, 50))

    pygame.display.update()
    
# Configuración del reloj del juego
RELOJ = pygame.time.Clock()

# Variables del juego
ejecuta = True
angulo_lanzamiento = 45
ajustando_angulo = False

# Variable para controlar la ejecución del juego y el menú
# Main game loop
# Main game loop
# Main game loop
game_running = False
key_pressed = False  # Track the X key state
# Variable to track the current screen (menu, help, game)
current_screen = 'menu'

while ejecuta:
    RELOJ.tick(24)

    if current_screen == 'menu':
        PANTALLA.blit(background, (0, 0))
        botonplay.draw()
        botonhelp.draw()
        botonquit.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecuta = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botonplay.is_clicked():
                    current_screen = 'game'
                elif botonhelp.is_clicked():
                    current_screen = 'help'
                elif botonquit.is_clicked():
                    ejecuta = False

    elif current_screen == 'help':
        PANTALLA.blit(controles, (0, 0))
        botonback.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecuta = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botonback.is_clicked():
                    current_screen = 'menu'

    elif current_screen == 'game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecuta = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    ajustando_angulo = True
                elif event.button == 4:  # Mouse wheel up
                    angulo_lanzamiento += 1
                elif event.button == 5:  # Mouse wheel down
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    cambiar_cancion.set()
                elif event.key == pygame.K_m:
                    muted = not muted

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            fuerza_lanzamiento = min(fuerza_lanzamiento + INCREMENTO_FUERZA, FUERZA_MAXIMA)
        if keys[pygame.K_DOWN]:
            fuerza_lanzamiento = max(fuerza_lanzamiento - INCREMENTO_FUERZA, FUERZA_MINIMA)

        if keys[pygame.K_x]:
            if not key_pressed:  # Check if the key was already pressed
                key_pressed = True
                if intentos_restantes > 0:
                    lanzado = True
                    izquierda = False
                    derecha = False
                    cuentaPasos = 0
                    lanzar_canica(px, py, angulo_lanzamiento, fuerza_lanzamiento)
        else:
            key_pressed = False  # Reset key press state when the key is released

        if keys[pygame.K_a] and px > -200:
            px -= VELOCIDAD
            izquierda = True
            derecha = False
        elif keys[pygame.K_d] and px < 900 - VELOCIDAD - 40:
            px += VELOCIDAD
            izquierda = False
            derecha = True
        elif keys[pygame.K_w] and py > 200:
            py -= VELOCIDAD
            derecha = True
        elif keys[pygame.K_s] and py < 300:
            py += VELOCIDAD
            derecha = True
        else:
            izquierda = False
            derecha = False
            cuentaPasos = 0

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
                cuentaSalto = ALTURA_SALTO
                salto = False
                cuentaSalto_lista = 0

        PANTALLA.blit(fondo_surface, (0, 0))
        PANTALLA.blit(bolirana, (570, 190))
        PANTALLA.blit(rana1, rana1_rect)
        PANTALLA.blit(rana2, rana2_rect)
        PANTALLA.blit(rana3, rana3_rect)
        recargaPantalla()

        if intentos_restantes == 0:
            pygame.time.delay(2000) #Cuando se llega a 0 intentos, se para el tiempo 2 segundos y se resetea el puntaje.
            intentos_restantes = 5
            puntaje = 0

pygame.quit()




   

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
GRAVEDAD = 5
FUERZA_INICIAL = 0
FUERZA_MAXIMA = 100
FUERZA_MINIMA = 0
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
canica_ui = pygame.transform.scale(canica, (CANICA_DIMENSIONES[0] * 2, CANICA_DIMENSIONES[1] * 2))
canica = pygame.transform.scale(canica, CANICA_DIMENSIONES)

canica_rect = canica.get_rect()

# Bolirana
bolirana = pygame.image.load('imagenes/bolirana1.png').convert_alpha()
#bolirana = pygame.transform.flip(bolirana, True, False)
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

coin = pygame.image.load('imagenes/coin.png').convert_alpha()
coin_size = (30, 30)
coin = pygame.transform.scale(coin, coin_size)
coin_rect = coin.get_rect()
coin_rect.update(random.randint(300, 700), random.randint(100,300), coin_size[0], coin_size[1])
coin_taken = False
multiplicador = 1

# Personaje
quieto_rolo = pygame.image.load('imagenes/Quieto/Idle.png')
quieto_rolo = pygame.transform.scale(quieto_rolo, PERSONAJE_DIMENSIONES)

quieto_canica = pygame.image.load('imagenes/Quieto/Idle_canica.png')
quieto_canica = pygame.transform.scale(quieto_canica, PERSONAJE_DIMENSIONES)

camina_rolo = [pygame.transform.scale(pygame.image.load(f'imagenes/Caminando/Walk{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 9)]
camina_izq_rolo = [pygame.transform.flip(img, True, False) for img in camina_rolo]

lanzamiento_rolo = [pygame.transform.scale(pygame.image.load(f'imagenes/imagenes-lanzamiento/Attack_{i}.png'), PERSONAJE_DIMENSIONES) for i in range(2, 10)]

salto_lista = [pygame.transform.scale(pygame.image.load(f'imagenes/Salto/Jump-{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 9)]

#PJ1

quieto_llanero = pygame.image.load('imagenes/pjs/quietollanero/walkllanero1.png')
quieto_llanero = pygame.transform.scale(quieto_llanero, PERSONAJE_DIMENSIONES)

camina_llanero = [pygame.transform.scale(pygame.image.load(f'imagenes/pjs/caminallanero/walkllanero{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 9)]
camina_izq_llanero = [pygame.transform.flip(img, True, False) for img in camina_llanero]
 
lanzamiento_llanero = [pygame.transform.scale(pygame.image.load(f'imagenes/pjs/lanzamientollanero/lan{i}llanero.png'), PERSONAJE_DIMENSIONES) for i in range(1, 5)]

#PJ2

quieto_paisa = pygame.image.load('imagenes/pjs/quietopaisa/caminapaisa1.png')
quieto_paisa = pygame.transform.scale(quieto_paisa, PERSONAJE_DIMENSIONES)

camina_paisa = [pygame.transform.scale(pygame.image.load(f'imagenes/pjs/caminapaisa/caminapaisa{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 9)]
camina_izq_paisa = [pygame.transform.flip(img, True, False) for img in camina_paisa]

lanzamiento_paisa = [pygame.transform.scale(pygame.image.load(f'imagenes/pjs/lanzamientopaisa/lan{i}.png'), PERSONAJE_DIMENSIONES) for i in range(1, 5)]

skins_images = {
    "Paisa": {
        "camina": camina_paisa,
        "camina_izq": camina_izq_paisa,
        "lanzamiento": lanzamiento_paisa,
        "quieto": quieto_paisa
    },
    "Llanero": {
        "camina": camina_llanero,
        "camina_izq": camina_izq_llanero,
        "lanzamiento": lanzamiento_llanero,
        "quieto": quieto_llanero
    },
    "Rolo": {
        "camina": camina_rolo,
        "camina_izq" : camina_izq_rolo,
        "lanzamiento" : lanzamiento_rolo,
        "quieto" : quieto_rolo
        
        }
}    


COLOR_NEGRO = (0,0,0)
COLOR_BLANCO = (255, 255, 255)
COLOR_AZUL = (0, 0, 255)


icons_size = (60,40)

p1 = pygame.image.load('imagenes/p1.png').convert_alpha()
p1 = pygame.transform.scale(p1, icons_size)

p2 = pygame.image.load('imagenes/p2.png').convert_alpha()
p2 = pygame.transform.scale(p2, icons_size)

p3 = pygame.image.load('imagenes/p3.png').convert_alpha()
p3 = pygame.transform.scale(p3, icons_size)

p4 = pygame.image.load('imagenes/p4.png').convert_alpha()
p4 = pygame.transform.scale(p4, icons_size)
#menú
play = pygame.image.load('menu/play.png').convert_alpha()
play.set_colorkey((0,0,0))

help = pygame.image.load('menu/help.png').convert_alpha()

quit = pygame.image.load('menu/quit.png').convert_alpha()

settings = pygame.image.load("menu/settings.png")

controles = pygame.image.load('menu/controles.png').convert_alpha()
controles = pygame.transform.scale(controles , (W,H))

volver_button = pygame.image.load('menu/back-button.png').convert_alpha()
volver_button = pygame.transform.scale(volver_button, (200,200))

class Boton:
    def __init__(self, x, y, w, h, image_or_color=None, texto="", color_texto=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        
        if isinstance(image_or_color, pygame.Surface):
            # Si el argumento es una imagen, redimensionarla al tamaño del botón
            self.image = pygame.transform.scale(image_or_color, (w, h))
            self.color_fondo = None
        else:
            # Si el argumento es un color, usarlo como fondo
            self.image = None
            self.color_fondo = image_or_color

        self.texto = texto
        self.color_texto = color_texto
        self.clicked = False

    def draw(self, surface):
        if self.image:
            # Dibujar la imagen si existe
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            # Dibujar un rectángulo con el color de fondo si no hay imagen
            pygame.draw.rect(surface, self.color_fondo, self.rect)

        if self.texto:
            # Renderizar el texto en el botón
            font = pygame.font.Font(None, 36)  # Definir la fuente
            texto_surface = font.render(self.texto, True, self.color_texto)
            # Centrar el texto en el botón
            texto_rect = texto_surface.get_rect(center=self.rect.center)
            surface.blit(texto_surface, texto_rect)

    def is_clicked(self):
        # Obtener posición del mouse y verificar si se hace clic en el botón
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]  # Obtener estado del botón izquierdo del mouse
        
        if self.rect.collidepoint(pos) and click:
            return True
        return False
    
background = pygame.image.load('menu/background.png')    
    
# Crear botones
botonplay = Boton(100, 80, 317, 150, play)
botonplay2 = Boton(700, 450, 300, 150, play)
botonhelp = Boton(100, 280, 317, 150, help)
botonquit = Boton(100, 380, 317, 150, quit)
botonsettings = Boton(100, 180, 317, 150, settings)

botonback = pygame.image.load('menu/back-button.png')
botonback = Boton(50, 50, 200, 200, botonback)




# Cargar imágenes
botonllanero = pygame.image.load('menu/menu2/llanero/llanero.png')
botonpaisa = pygame.image.load('menu/menu2/llanero/paisa.png')
botonrolo = pygame.image.load('menu/menu2/llanero/rolo.png')

boton_skins = {
    0: [Boton(100, 250, 100, 50, botonllanero), Boton(200, 250, 100, 50, botonpaisa), Boton(300, 250, 100, 50, botonrolo)],
    1: [Boton(100, 350, 100, 50, botonllanero), Boton(200, 350, 100, 50, botonpaisa), Boton(300, 350, 100, 50, botonrolo)],
    2: [Boton(100, 450, 100, 50, botonllanero), Boton(200, 450, 100, 50, botonpaisa), Boton(300, 450, 100, 50, botonrolo)],
    3: [Boton(100, 550, 100, 50, botonllanero), Boton(200, 550, 100, 50, botonpaisa), Boton(300, 550, 100, 50, botonrolo)],
}

botonr1 = pygame.image.load("menu/menu2/r4/r1.png")
botonr2 = pygame.image.load("menu/menu2/r4/r2.png")
botonr3 = pygame.image.load("menu/menu2/r4/r3.png")
botonr4 = pygame.image.load("menu/menu2/r4/r4.png")

# Crear botones para la selección de número de rondas
boton_ronda_1 = Boton(350, 50, 100, 50, botonr1)
boton_ronda_2 = Boton(500, 50, 100, 50, botonr2)
boton_ronda_3 = Boton(650, 50, 100, 50, botonr3)
boton_ronda_4 = Boton(800, 50, 100, 50, botonr4)

botonj1 = pygame.image.load("menu/menu2/players/p111.png")
botonj2 = pygame.image.load("menu/menu2/players/p112.png")
botonj3 = pygame.image.load("menu/menu2/players/p113.png")
botonj4 = pygame.image.load("menu/menu2/players/p114.png")

# Crear botones para la selección de número de jugadores
boton_jugador_1 = Boton(350, 150, 100, 50, botonj1)
boton_jugador_2 = Boton(500, 150, 100, 50, botonj2)
boton_jugador_3 = Boton(650, 150, 100, 50, botonj3)
boton_jugador_4 = Boton(800, 150, 100, 50, botonj4)
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

intentos_restantes = 5  # Variable para realizar seguimiento a los intentos restantes

n_jugadores = 4
jugador_actual = 0
puntajes = [0 for i in range(n_jugadores)]   # Variable para realizar seguimiento al puntaje

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS",30)

tiempo = 0
is_ball_charged = False
charge_time_seg = 2


# Variables para guardar las selecciones
num_rondas = 1
subita = False
best_player = []
#n_jugadores = 1
skins = ["Paisa", "Llanero", "Rolo", "Paisa"]  # Máximo 4 jugadores

def menu_principal():
    global current_screen, muted
    while current_screen == 'menu':
        PANTALLA.blit(background, (0, 0))
        botonplay.draw(PANTALLA)
        botonhelp.draw(PANTALLA)
        botonquit.draw(PANTALLA)
        botonsettings.draw(PANTALLA)
        press_m_mute = pygame.image.load("menu/mute.png")
        press_m_mute = pygame.transform.scale(press_m_mute, (250,250))
        PANTALLA.blit(press_m_mute, (10,440))

        pygame.display.update()
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botonplay.is_clicked():
                    pygame.time.delay(200)
                    current_screen = 'game'
                elif botonhelp.is_clicked():
                    pygame.time.delay(200)
                    current_screen = 'help'
                elif botonquit.is_clicked():
                    pygame.quit()
                    exit()
                elif botonsettings.is_clicked():
                    current_screen = 'settings'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    cambiar_cancion.set()
                elif event.key == pygame.K_m:
                    muted = not muted


# Función del menú de selección

background_seleccion = pygame.image.load('menu/menu2/background.jpeg')
def menu_seleccion():
    global num_rondas, n_jugadores, skins, current_screen, muted, puntajes
    ejecutando_menu_seleccion = True
    
    
    while ejecutando_menu_seleccion:
        PANTALLA.blit(background_seleccion, (0, 0))

        # Dibujar botones para seleccionar el número de rondas
        boton_ronda_1.draw(PANTALLA)
        boton_ronda_2.draw(PANTALLA)
        boton_ronda_3.draw(PANTALLA)
        boton_ronda_4.draw(PANTALLA)

        # Detectar clics en los botones de rondas
        if boton_ronda_1.is_clicked():
            num_rondas = 1
        if boton_ronda_2.is_clicked():
            num_rondas = 2
        if boton_ronda_3.is_clicked():
            num_rondas = 3
        if boton_ronda_4.is_clicked():
            num_rondas = 4

        # Mostrar el número de rondas seleccionado
        texto_rondas = font.render(f"Rounds: {num_rondas}", True, COLOR_BLANCO)
        PANTALLA.blit(texto_rondas, (50, 50))

        # Dibujar botones para seleccionar el número de jugadores
        boton_jugador_1.draw(PANTALLA)
        boton_jugador_2.draw(PANTALLA)
        boton_jugador_3.draw(PANTALLA)
        boton_jugador_4.draw(PANTALLA)

        # Detectar clics en los botones de jugadores
        if boton_jugador_1.is_clicked():
            n_jugadores = 1
        if boton_jugador_2.is_clicked():
            n_jugadores = 2
        if boton_jugador_3.is_clicked():
            n_jugadores = 3
        if boton_jugador_4.is_clicked():
            n_jugadores = 4
        puntajes = [0 for i in range(n_jugadores)]

        # Mostrar el número de jugadores seleccionado
        texto_jugadores = font.render(f"Players: {n_jugadores}", True, COLOR_BLANCO)
        PANTALLA.blit(texto_jugadores, (50, 150))

        # Dibujar botones de selección de skins según el número de jugadores
        for i in range(n_jugadores):
            for j, boton_skin in enumerate(boton_skins[i]):
                boton_skin.draw(PANTALLA)
                if boton_skin.is_clicked():
                    skins[i] = ["Llanero", "Paisa", "Rolo"][j]
        
        # Mostrar selección de skins
        for i in range(n_jugadores):
            texto_skin = font.render(f"P{i+1} Skin: {skins[i]}", True, COLOR_NEGRO)
            PANTALLA.blit(texto_skin, (450, 250 + i * 100))

        # Dibujar botón de inicio del juego
        enter = pygame.image.load('menu/enter.png')
        enter = pygame.transform.scale(enter, (350,350))
        PANTALLA.blit(enter,(700,330))
        

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_screen = 'game'
                    ejecutando_menu_seleccion = False
                    
                elif event.key == pygame.K_n:
                    cambiar_cancion.set()
                elif event.key == pygame.K_m:
                    muted = not muted
                elif event.key == pygame.K_ESCAPE:
                    puntajes = [0 for i in range(n_jugadores)]
                    current_screen = 'menu'
                    ejecutando_menu_seleccion = False    
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def reproducir_musica_aleatoria_indefinidamente(lista_musica_fondo, cambiar_musica_event, volumen=0.03):
    global muted
    while True:
        random.shuffle(lista_musica_fondo)
        for sonido in lista_musica_fondo:
            sonido.set_volume(volumen if not muted else 0)  # Ajustar el volumen aquí
            sonido.play()
            # Esperar hasta que el sonido termine de reproducirse o se presione "N", o se mutee con "M"
            while pygame.mixer.get_busy():
                if cambiar_musica_event.is_set():
                    sonido.stop() 
                    cambiar_musica_event.clear()
                    break
                time.sleep(0.1)
                if muted:
                    sonido.set_volume(0)
                else:
                    sonido.set_volume(volumen)



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

def dibujar_trayectoria(screen, fuerza, angulo): #codigo es compatible pero no hace uso de esta funcion 
    global px, py
    puntos = []
    total_puntos = 7
    intervalo_t = 3 #intervalos en los que se dibujan los puntos
    for t in range(0, total_puntos * intervalo_t, intervalo_t):  #calculamos puntos para t de 0 a 20 (0.1 * 200)
        tiempo = t / 10
        x, y = calcular_trayectoria(fuerza, angulo, tiempo)
        if 0 <= px + PERSONAJE_OFFSET_X + x <= W and 0 <= py + PERSONAJE_OFFSET_Y - y <= H:
            puntos.append((px + PERSONAJE_OFFSET_X + x, py + PERSONAJE_OFFSET_Y - y))
        else:
            break
    for punto in puntos:
        pygame.draw.circle(screen, (255, 255, 255), (int(punto[0]), int(punto[1])), 3)   

def calcular_trayectoria(fuerza, angulo, tiempo):
    angulo_rad = math.radians(angulo)
    x = fuerza * math.cos(angulo_rad) * tiempo
    y = fuerza * math.sin(angulo_rad) * tiempo - 0.5 * GRAVEDAD * tiempo ** 2
    return x, y

# Crear mascaras para la canica y rana
canica_mask = pygame.mask.from_surface(canica)
rana1_mask = pygame.mask.from_surface(rana1)
rana2_mask = pygame.mask.from_surface(rana2)
rana3_mask = pygame.mask.from_surface(rana3)

def reseteo(score_value): #aumenta el puntaje y resetea los valores para otro lanzamiento
    global canica_lanzada, is_ball_charged, tiempo, fuerza_lanzamiento, puntajes, intentos_restantes, jugador_actual, multiplicador, coin_taken, coin_size
    puntajes[jugador_actual] += score_value
    canica_lanzada = False  
    is_ball_charged = False
    tiempo = 0
    fuerza_lanzamiento = FUERZA_INICIAL
    multiplicador = 1
    coin_taken = False
    coin_rect.update(random.randint(300, 700), random.randint(100,300), coin_size[0], coin_size[1]) # dibuja la moneda en una posicion aleatoria

    if intentos_restantes == 0:
            intentos_restantes = 5
            #pasa el turno al siguiente jugador
            if jugador_actual == 0 and n_jugadores >= 2:
                jugador_actual = 1
            elif jugador_actual == 1 and n_jugadores == 2:
                jugador_actual = 0
                fin_de_set()
            elif jugador_actual == 1 and n_jugadores >= 3:
                jugador_actual = 2
            elif jugador_actual == 2 and n_jugadores == 3:
                jugador_actual = 0
                fin_de_set()
            elif jugador_actual == 2 and n_jugadores >= 4:
                jugador_actual = 3
            elif jugador_actual == 3:
                jugador_actual = 0
                fin_de_set()
            pygame.time.delay(100) #Cuando se llega a 0 intentos, se para el tiempo 0.1 segundos
            
def fin_de_set():
    global num_rondas, puntajes, subita, current_screen, best_player
    if num_rondas >= 2 and not subita:
        num_rondas -= 1
    else:
        max_puntaje = 0
        best_player = []
        for i in range(len(puntajes)):
            if puntajes[i] > max_puntaje:
                best_player.clear()
                best_player.append(i+1)
                max_puntaje = puntajes[i]
            elif puntajes[i] == max_puntaje:
                best_player.append(i+1)

        if len(best_player) != 1:
            subita = True
        else:
            subita = False
            current_screen = 'ganador'
            puntajes = [0 for i in range(n_jugadores)]
            num_rondas = 1


                
# Asegúrate de que la lista skins esté correctamente inicializada
if len(skins) < n_jugadores:
    # Rellenar con una skin predeterminada si no se ha seleccionado ninguna
    for i in range(n_jugadores):
        if skins[i] == '':
            skins[i] = 'Paisa'  # Asigna 'Paisa' como skin predeterminada


def recargaPantalla():
    global cuentaPasos, lanzado, cuentaLanzamiento, salto, cuentaSalto, cuentaSalto_lista, px, py, izquierda, derecha, canica_lanzada, canica_x, canica_y, canica_vx, canica_vy, canica_pos, angulo_lanzamiento, fuerza_lanzamiento, FUERZA_MAXIMA, puntajes, intentos_restantes, tiempo, is_ball_charged, jugador_actual, coin_taken, multiplicador, skins_images, skins, jugador_actual, subita

    skin_actual = skins_images[skins[jugador_actual]]
    # Actualizar la animación del personaje
    if cuentaPasos + 1 >= len(skin_actual["camina"]):
        cuentaPasos = 0

    if izquierda:
        PANTALLA.blit(skin_actual["camina_izq"][cuentaPasos // 1], (px, py))
        cuentaPasos += 1
        canica_pos = (px + 190, py + 180) 
    elif derecha:
        PANTALLA.blit(skin_actual["camina"][cuentaPasos // 1], (px, py))
        cuentaPasos += 1
        canica_pos = (px + 190, py + 180)
    elif lanzado:
        if cuentaLanzamiento >= len(skin_actual["lanzamiento"]):
            lanzado = False
            cuentaLanzamiento = 0
        else:
            PANTALLA.blit(skin_actual["lanzamiento"][cuentaLanzamiento // 1], (px, py))
            cuentaLanzamiento += 1
    else:
        PANTALLA.blit(skin_actual["quieto"], (px, py))

    # dibuja icono encima del jugador actual
    if jugador_actual == 0:
        pygame.draw.rect(PANTALLA, (0, 0, 0), pygame.Rect(px+190, py+10, icons_size[0], icons_size[1]))
        PANTALLA.blit(p1, (px + 190, py+10))
    elif jugador_actual == 1:
        pygame.draw.rect(PANTALLA, (0, 0, 0), pygame.Rect(px+190, py+10, icons_size[0], icons_size[1]))
        PANTALLA.blit(p2, (px + 190, py+10))
    elif jugador_actual == 2:
        pygame.draw.rect(PANTALLA, (0, 0, 0), pygame.Rect(px+190, py+10, icons_size[0], icons_size[1]))
        PANTALLA.blit(p3, (px + 190, py+10))
    elif jugador_actual == 3:
        pygame.draw.rect(PANTALLA, (0, 0, 0), pygame.Rect(px+190, py+10, icons_size[0], icons_size[1]))
        PANTALLA.blit(p4, (px + 190, py+10))


    # Actualizar la posición de la canica si es lanzada
    if canica_lanzada:
        tiempo += INTERVALO_TIEMPO
        x, y = calcular_trayectoria(fuerza_lanzamiento, angulo_lanzamiento, tiempo)

        canica_vy += GRAVEDAD

        # Actualizar la posición de la recta de la canica
        canica_rect.topleft = (canica_x + x,canica_y - y)

        # Comprueba si hay colisiones precisas y perfectas en píxeles con ranas
        offset_rana1 = (rana1_rect.x - canica_rect.x, rana1_rect.y - canica_rect.y)
        offset_rana2 = (rana2_rect.x - canica_rect.x, rana2_rect.y - canica_rect.y)
        offset_rana3 = (rana3_rect.x - canica_rect.x, rana3_rect.y - canica_rect.y)
        offset_coin  = (coin_rect.x - canica_rect.x, coin_rect.y - canica_rect.y)

        collision_rana1 = canica_mask.overlap(rana1_mask, offset_rana1)
        collision_rana2 = canica_mask.overlap(rana2_mask, offset_rana2)
        collision_rana3 = canica_mask.overlap(rana3_mask, offset_rana3)
        collision_coin = canica_mask.overlap(rana1_mask, offset_coin)

        PANTALLA.blit(canica, canica_rect)

        # la moneda duplica el puntaje si despues le da a una rana en el mismo lanzamiento
        if collision_coin:
            coin_taken = True
            multiplicador = 2

        if collision_rana1:
            reseteo(100 * multiplicador)
            
        elif collision_rana2:
            reseteo(200 * multiplicador)
            
        elif collision_rana3:
            reseteo(500 * multiplicador)

        if canica_rect.x > W + 25 or canica_rect.y > H + 25 or canica_rect.x < -25:
            reseteo(0)
        
    if not coin_taken: 
            PANTALLA.blit(coin, coin_rect)
    # Dibujar linea del agunlo de tiro
    if ajustando_angulo:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(PANTALLA, (255, 0, 0), (px + PERSONAJE_OFFSET_X, py + PERSONAJE_OFFSET_Y), (mouse_x, mouse_y), 2)
        dibujar_trayectoria(PANTALLA, fuerza_lanzamiento, angulo_lanzamiento)

    # Dibujar fuerza de tiro
    barra_rect = pygame.Rect(10, 60, fuerza_lanzamiento * 1.5, 20)
    barra_rect_ful = pygame.Rect(10, 60, FUERZA_MAXIMA * 1.5, 20)
    pygame.draw.rect(PANTALLA, (0, 0, 0), barra_rect_ful)
    pygame.draw.rect(PANTALLA, (0, 254, 0), barra_rect)

    # mostrar rondas restantes
    if subita == False:
        texto_rondas = font.render(f"Rounds: {num_rondas}", True, COLOR_BLANCO)
    elif subita == True:
        texto_rondas = font.render('Muerte Subita', True, (255, 0, 0))
    if n_jugadores != 1:
        PANTALLA.blit(texto_rondas, (10, 110))

    # Mostrar puntaje en pantalla

    for i in range(n_jugadores): # muestra el puntaje dependiendo de la cantidad de jugadores
        if i == 0:
            color = (255, 0, 0) # rojo -> jugador 1
        if i == 1:
            color = (0, 0, 255) # azul -> jugador 2
        if i == 2:
            color = (255, 255, 0) # amarillo -> jugador 3
        if i == 3:
            color = (0, 255, 0) # verde -> jugador 4
        puntaje_font = font.render(f'P{i+1}: {puntajes[i]}', True, color) 
        puntaje_font_2 = font.render(f'P{i+1}: {puntajes[i]}', True, (0, 0, 0))
        PANTALLA.blit(puntaje_font_2, (W - 125*n_jugadores + i*125 + 2, 12))
        PANTALLA.blit(puntaje_font, (W - 125*n_jugadores + i*125, 10))
        
    

    # Mostrar intentos restantes en pantalla
    for i in range(intentos_restantes):
        PANTALLA.blit(canica_ui, (10 + 30*i, 10))

    

    pygame.display.update()
    
# Configuración del reloj del juego
RELOJ = pygame.time.Clock()

# Variables del juego
ejecuta = True
angulo_lanzamiento = 45
ajustando_angulo = False

# Variable para controlar la ejecución del juego y el menú
# Ciclo principal del juego
game_running = False
key_pressed = False  # Track the X key state
# Variable para seguir la pantalla actual (play, menu, help)
current_screen = 'menu'

while ejecuta:
    RELOJ.tick(24)
    if current_screen == 'menu':
        menu_principal()
    
    elif current_screen == 'help':
        PANTALLA.blit(controles, (0, 0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecuta = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    cambiar_cancion.set()
                elif event.key == pygame.K_m:
                    muted = not muted
                elif event.key == pygame.K_ESCAPE:
                    current_screen = 'menu'    
        
    
    elif current_screen == 'settings':
        menu_seleccion()

    elif current_screen == 'ganador':
        PANTALLA.blit(background, (0, 0))
        #pygame.draw.rect(PANTALLA, (0, 0, 0), pygame.Rect(250, 250, 500, 50))
        texto_ganar = font.render(f'El jugador {best_player[0]} ha ganado', True, COLOR_BLANCO)
        texto_tecla =  font.render(f'Presione cualquier tecla', True, COLOR_BLANCO)
        texto_tecla2 = font.render(f'     para continuar', True, COLOR_BLANCO)
        PANTALLA.blit(texto_ganar, (100, 285))
        PANTALLA.blit(texto_tecla, (100, 330))
        PANTALLA.blit(texto_tecla2, (100, 355))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecuta = False
            if event.type == pygame.KEYDOWN:
                current_screen = 'menu'
                best_player = []

    elif current_screen == 'game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecuta = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not canica_lanzada:  # Mouse click izquierdo
                    ajustando_angulo = True
                    mouse_x, mouse_y = event.pos
                    dx = mouse_x - (px + PERSONAJE_OFFSET_X)
                    dy = (py + PERSONAJE_OFFSET_Y) - mouse_y
                    angulo_lanzamiento = math.degrees(math.atan2(dy, dx))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    ajustando_angulo = False
            elif event.type == pygame.MOUSEMOTION:
                if ajustando_angulo and not canica_lanzada:
                    mouse_x, mouse_y = event.pos
                    dx = mouse_x - (px + PERSONAJE_OFFSET_X)
                    dy = (py + PERSONAJE_OFFSET_Y) - mouse_y
                    angulo_lanzamiento = math.degrees(math.atan2(dy, dx))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    cambiar_cancion.set()
                elif event.key == pygame.K_m:
                    muted = not muted
                elif event.key == pygame.K_ESCAPE:
                    puntajes = [0 for i in range(n_jugadores)]
                    current_screen = 'menu'

        keys = pygame.key.get_pressed()
        key_mouse = pygame.mouse.get_pressed()
        if key_mouse[0] and not canica_lanzada:
            ajustando_angulo = True
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - (px + PERSONAJE_OFFSET_X)
            dy = (py + PERSONAJE_OFFSET_Y) - mouse_y
            angulo_lanzamiento = math.degrees(math.atan2(dy, dx))
            is_ball_charged = True
            fuerza_lanzamiento += (FUERZA_MAXIMA - FUERZA_INICIAL) / (charge_time_seg * RELOJ.get_fps()+0.1) #aumenta la fuerza de modo que llega al maximo al cabo de la cantidad de tiempo dictada por la variable: charge_time_seg
            dibujar_trayectoria(PANTALLA, fuerza_lanzamiento, angulo_lanzamiento)
        if fuerza_lanzamiento > FUERZA_MAXIMA:#para que no se pase del maximo
            fuerza_lanzamiento = FUERZA_MAXIMA
        if not key_mouse[0] and is_ball_charged: #ver las intrucciones en las primeras lineas para ver como funciona espacio
            is_ball_charged = False
            lanzado = True
            izquierda = False
            derecha = False
            cuentaPasos = 0
            lanzar_canica(px, py, angulo_lanzamiento, fuerza_lanzamiento)

        if keys[pygame.K_e]:
            if not key_pressed:  # Verificar si al tecla ya esta presionada
                key_pressed = True
                if intentos_restantes > 0:
                    lanzado = True
                    izquierda = False
                    derecha = False
                    cuentaPasos = 0
                    lanzar_canica(px, py, angulo_lanzamiento, fuerza_lanzamiento)
        else:
            key_pressed = False  # Resetear el estado de la tecla cuando se deja de presionar

        if keys[pygame.K_a] and px > -200:
            px -= VELOCIDAD
            izquierda = True
            derecha = False
        elif keys[pygame.K_d] and px < 250 - VELOCIDAD - 40:
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

        
        
pygame.quit()

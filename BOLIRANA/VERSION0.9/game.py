import pygame
from sys import exit
import math

pygame.init()

W, H = 1000, 600
PANTALLA = pygame.display.set_mode((W, H))
pygame.display.set_caption('Bolirana')
icono = pygame.image.load('imagenes/icon.png')
pygame.display.set_icon(icono)

# Fondo juego
fondo_surface = pygame.image.load('imagenes/Fondo1.png').convert()
fondo_surface = pygame.transform.scale(fondo_surface, (W, H))

# Canica
canica = pygame.image.load('imagenes/canica.png').convert_alpha()
canica = pygame.transform.scale(canica, (26.5, 23.3))

# Personaje
quieto = pygame.image.load('imagenes/Quieto/Idle.png')
quieto = pygame.transform.scale(quieto, (400, 324))

quieto_canica = pygame.image.load('imagenes/Quieto/Idle_canica.png')
quieto_canica = pygame.transform.scale(quieto_canica, (400, 324))

camina1 = pygame.image.load('imagenes/Caminando/Walk1.png')
camina1 = pygame.transform.scale(camina1, (400, 324))
camina2 = pygame.image.load('imagenes/Caminando/Walk2.png')
camina2 = pygame.transform.scale(camina2, (400, 324))
camina3 = pygame.image.load('imagenes/Caminando/Walk3.png')
camina3 = pygame.transform.scale(camina3, (400, 324))
camina4 = pygame.image.load('imagenes/Caminando/Walk4.png')
camina4 = pygame.transform.scale(camina4, (400, 324))
camina5 = pygame.image.load('imagenes/Caminando/Walk5.png')
camina5 = pygame.transform.scale(camina5, (400, 324))
camina6 = pygame.image.load('imagenes/Caminando/Walk6.png')
camina6 = pygame.transform.scale(camina6, (400, 324))
camina7 = pygame.image.load('imagenes/Caminando/Walk7.png')
camina7 = pygame.transform.scale(camina7, (400, 324))
camina8 = pygame.image.load('imagenes/Caminando/Walk8.png')
camina8 = pygame.transform.scale(camina8, (400, 324))

camina1izq = pygame.transform.flip(camina1, True, False)
camina2izq = pygame.transform.flip(camina2, True, False)
camina3izq = pygame.transform.flip(camina3, True, False)
camina4izq = pygame.transform.flip(camina4, True, False)
camina5izq = pygame.transform.flip(camina5, True, False)
camina6izq = pygame.transform.flip(camina6, True, False)
camina7izq = pygame.transform.flip(camina7, True, False)
camina8izq = pygame.transform.flip(camina8, True, False)

# lanzamiento 
lanzamiento1 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_1.png')
lanzamiento1 = pygame.transform.scale(lanzamiento1, (400,324))
lanzamiento2 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_2.png')
lanzamiento2 = pygame.transform.scale(lanzamiento2, (400,324))
lanzamiento3 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_3.png')
lanzamiento3 = pygame.transform.scale(lanzamiento3, (400,324))
lanzamiento4 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_4.png')
lanzamiento4 = pygame.transform.scale(lanzamiento4, (400,324))
lanzamiento5 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_5.png')
lanzamiento5 = pygame.transform.scale(lanzamiento5, (400,324))
lanzamiento6 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_6.png')
lanzamiento6 = pygame.transform.scale(lanzamiento6, (400,324))
lanzamiento7 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_7.png')
lanzamiento7 = pygame.transform.scale(lanzamiento7, (400,324))
lanzamiento8 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_8.png')
lanzamiento8 = pygame.transform.scale(lanzamiento8, (400,324))
lanzamiento9 = pygame.image.load('imagenes/imagenes-lanzamiento/Attack_9.png')
lanzamiento9 = pygame.transform.scale(lanzamiento9, (400,324))

# salto
salto1 = pygame.image.load('imagenes/Salto/Jump-1.png')
salto1 = pygame.transform.scale(salto1, (400, 324))
salto2 = pygame.image.load('imagenes/Salto/Jump-2.png')
salto2 = pygame.transform.scale(salto2, (400, 324))
salto3 = pygame.image.load('imagenes/Salto/Jump-3.png')
salto3 = pygame.transform.scale(salto3, (400, 324))
salto4 = pygame.image.load('imagenes/Salto/Jump-4.png')
salto4 = pygame.transform.scale(salto4, (400, 324))
salto5 = pygame.image.load('imagenes/Salto/Jump-5.png')
salto5 = pygame.transform.scale(salto5, (400, 324))
salto6 = pygame.image.load('imagenes/Salto/Jump-6.png')
salto6 = pygame.transform.scale(salto6, (400, 324))
salto7 = pygame.image.load('imagenes/Salto/Jump-7.png')
salto7 = pygame.transform.scale(salto7, (400, 324))
salto8 = pygame.image.load('imagenes/Salto/Jump-8.png')
salto8 = pygame.transform.scale(salto8, (400, 324))

caminaDerecha = [camina1, camina2, camina3, camina4, camina5, camina6, camina7, camina8]
caminaIzquierda = [camina1izq, camina2izq, camina3izq, camina4izq, camina5izq, camina6izq, camina7izq, camina8izq]
lanzamiento = [lanzamiento2, lanzamiento3, lanzamiento4, lanzamiento5, lanzamiento6, lanzamiento7, lanzamiento8, lanzamiento9]
salto_lista = [salto1, salto2, salto3, salto4, salto5, salto6, salto7, salto8]

x = 0
px = 50
py = 200
ancho = 40
velocidad = 15

salto = False
# altura del salto
cuentaSalto = 10
cuentaSalto_lista = 0

# Variables dirección
izquierda = False
derecha = False

# Variable de lanzamiento
lanzado = False
cuentaLanzamiento = 0

# pasos
cuentaPasos = 0

canica_lanzada = False
canica_x = 0
canica_y = 0
canica_vx = 0
canica_vy = 0
gravedad = 1

# Fuente para texto
font = pygame.font.Font(None, 36)

# Esta función inicializa y lanza una canica desde una posición (px, py) con cierto ángulo de lanzamiento.
def lanzar_canica(px, py, angulo_lanzamiento):
    global canica_lanzada, canica_x, canica_y, canica_vx, canica_vy
    canica_lanzada = True
    canica_x = px + 280  # Posición inicial de la canica, esencial para que salga de la mano del personaje
    canica_y = py + 180
    fuerza_lanzamiento = 25

    # Se convierte el ángulo de lanzamiento a radianes
    radianes = math.radians(angulo_lanzamiento)
    
    # El componente de la velocidad en el eje x (canica_vx) se calcula multiplicando la fuerza de lanzamiento por el coseno del ángulo en radianes
    canica_vx = fuerza_lanzamiento * math.cos(radianes)
    
    # El componente de la velocidad en el eje y (canica_vy) se calcula multiplicando la fuerza de lanzamiento por el seno del ángulo en radianes. Se invierte el signo para que la dirección inicial sea hacia arriba.
    canica_vy = -fuerza_lanzamiento * math.sin(radianes)

def recargaPantalla():
    global cuentaPasos, lanzado, cuentaLanzamiento, salto, cuentaSalto, cuentaSalto_lista, px, py, izquierda, derecha, canica_lanzada, canica_x, canica_y, canica_vx, canica_vy, canica_pos, angulo_lanzamiento

    # contador de pasos
    if cuentaPasos + 1 >= len(caminaDerecha):
        cuentaPasos = 0

    if izquierda:
        # creamos la lista de imágenes CaminaIzquierda. Si izquierda = True, se muestra en pantalla la imagen 0 de la lista y se le suma 1 a cada paso para mostrar toda la animación
        PANTALLA.blit(caminaIzquierda[cuentaPasos // 1], (px, py)) 
        cuentaPasos += 1
        canica_pos = (px + 190, py + 180)  # Ajusta según sea necesario

    elif derecha:
        PANTALLA.blit(caminaDerecha[cuentaPasos // 1], (px, py))
        cuentaPasos += 1
        canica_pos = (px + 190, py + 180)  # Ajusta según sea necesario

    elif salto:
        if cuentaSalto_lista < len(salto_lista):
            PANTALLA.blit(salto_lista[cuentaSalto_lista], (px, py))
            cuentaSalto_lista += 1
            canica_pos = (px + 200, py + 220)  # Ajusta según sea necesario
        else:
            PANTALLA.blit(salto_lista[-1], (px, py))
            canica_pos = (px + 200, py + 220)  # Ajusta según sea necesario

    elif lanzado:
        if cuentaLanzamiento >= len(lanzamiento):
            lanzado = False
            cuentaLanzamiento = 0
        else:
            PANTALLA.blit(lanzamiento[cuentaLanzamiento // 1], (px, py))
            cuentaLanzamiento += 1

    else:
        PANTALLA.blit(quieto, (px, py))
        # canica_pos = (px + 180, py + 180)  # Ajusta según sea necesario, esto es para poner la canica en la mano

    if canica_lanzada:
        canica_x += canica_vx
        canica_y += canica_vy
        canica_vy += gravedad  # Aceleración debida a la gravedad

        if canica_y > H:  # Si la canica sale de la pantalla por abajo
            canica_lanzada = False

        PANTALLA.blit(canica, (canica_x, canica_y))
    # else:
        # PANTALLA.blit(canica, canica_pos)

    # Dibujar la línea del ángulo de lanzamiento
    if ajustando_angulo:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(PANTALLA, (255, 0, 0), (px + 280, py + 180), (mouse_x, mouse_y), 2)

    # Dibujar el ángulo y la fuerza en la pantalla
    angulo_texto = font.render(f"Ángulo: {int(angulo_lanzamiento)}°", True, (255, 255, 255))
    PANTALLA.blit(angulo_texto, (10, 10))

    fuerza_texto = font.render(f"Fuerza: 25", True, (255, 255, 255))
    PANTALLA.blit(fuerza_texto, (10, 50))

    pygame.display.update()

RELOJ = pygame.time.Clock()

ejecuta = True
angulo_lanzamiento = 45
ajustando_angulo = False

while ejecuta:
    RELOJ.tick(24)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecuta = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                ajustando_angulo = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                ajustando_angulo = False
        elif event.type == pygame.MOUSEMOTION:
            if ajustando_angulo:
                mouse_x, mouse_y = event.pos
                dx = mouse_x - (px + 280)
                dy = (py + 180) - mouse_y
                angulo_lanzamiento = math.degrees(math.atan2(dy, dx))

    keys = pygame.key.get_pressed()  # Realiza acciones de las teclas manteniéndolas pulsadas. Repite el movimiento.

    # Tecla X: lanzamiento de la canica
    if keys[pygame.K_x]:
        lanzado = True  # comienza la animación del lanzamiento
        izquierda = False
        derecha = False
        cuentaPasos = 0
        lanzar_canica(px, py, angulo_lanzamiento)  # llamamos la función lanzar_canica con el ángulo actual
    # Tecla A: movimiento a la izquierda
    if keys[pygame.K_a] and px > -200:
        px -= velocidad
        izquierda = True
        derecha = False

    # Tecla D: movimiento a la derecha
    elif keys[pygame.K_d] and px < 900 - velocidad - ancho:  # márgenes de tope para que el personaje no se salga de la pantalla
        px += velocidad
        izquierda = False
        derecha = True
        
    # Tecla W: movimiento hacia arriba
    elif keys[pygame.K_w] and py > 200:  # margen de límite
        py -= velocidad
        derecha = True
        
    # Tecla S: movimiento hacia abajo
    elif keys[pygame.K_s] and py < 300:
        py += velocidad
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
            # no vamos a izquierda ni derecha. no contamos pasos
    else:
        # si el salto es true, el personaje está en el aire
        # el salto se controla con la variable cuentaSalto que empieza en 10 y decrece hasta -10.
        if cuentaSalto >= -10:
            py -= cuentaSalto * 3  # le restamos cuentaSalto * 3 a la posición del personaje en y. RECORDAR QUE AL RESTAR ESTAMOS SUBIENDO EL PERSONAJE
            cuentaSalto -= 1  # restamos cuentaSalto en cada ciclo para ir iterando en la animación
        else:
            cuentaSalto = 10  # resetamos para el próximo salto
            salto = False
            cuentaSalto_lista = 0  # Resetear el índice de imágenes del salto para la próxima animación

    PANTALLA.blit(fondo_surface, (0, 0))

    recargaPantalla()  # esta función se encarga de actualizar y redibujar todos los elementos de la pantalla en cada ciclo del bucle principal del juego. maneja la animación y el dibujo del personaje según su estado actual (caminando, saltando, lanzando o quieto)

pygame.quit()


    

    
    


    



       




   

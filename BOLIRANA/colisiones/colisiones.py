#icluye codigo de las colisiones
#lleva el puntaje (cada rana tiene un valor diferente) y los intentos en texto
#apunta con el mouse
#inicia el lanzamiento presionando espacio, manten para aumentar la fuerza de disparo, soltar para lanzar
#ajusta imagenes y las cosas en carpetas antes de probar :)
#Lo siento por los nombres de las variables

import sys, pygame, random, math
pygame.init()
pygame.mouse.set_visible(False)

#setea la pantalla
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)

n_de_bgs = 5
bgs = [pygame.image.load('imagenes/bgs/bg' + str(i+1) + '.jpg') for i in range(n_de_bgs)] # para almacenar diferentes fondos (todos deben llamarse igual y ser numerados de 1 en adelante ej. "bg1", "bg2", etc)
bgs = [pygame.transform.scale(i, size) for i in bgs] # escala cada fondo a la resolucion
bg = bgs[random.randint(0, len(bgs)-1)]#inicia en un fondo aleatorio de la lista


# nombre e icono de la pestaña (opcional)
icon = pygame.image.load("icon.ico")
pygame.display.set_icon(icon)
pygame.display.set_caption('=)')

clock = pygame.time.Clock()

#define las variables de texto
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

#balin
ball = pygame.image.load("migu.png")
ball_size = 64
ball = pygame.transform.scale(ball, (ball_size, ball_size)) # escala el balin a 64*64 pixeles
ballrect = ball.get_rect()

#ranas
obj = pygame.image.load("green.png") # poner imagen de rana
obj_size = 128
obj = pygame.transform.scale(obj, (obj_size, obj_size)) # escala la rana a 128*128 pixeles
obj_box = obj.get_rect()
no_spawn = 100
obj_box.update(random.randint(no_spawn, width - obj_size), random.randint(0, height - obj_size - no_spawn), obj_size, obj_size)

obj2 = pygame.image.load("pink.png") #poner imagen de rana
obj2_size = int(obj_size * 0.75)
obj2 = pygame.transform.scale(obj2, (obj2_size, obj2_size)) # escala la rana a 3/4 de la rana original -> es mas pequeña
obj2_box = obj2.get_rect()
no_spawn2 = 150
obj2_box.update(random.randint(no_spawn2, width - obj2_size), random.randint(0, height - obj2_size - no_spawn2), obj2_size, obj2_size)

obj3 = pygame.image.load("golden.png") #poner imagen de rana
obj3_size = obj_size // 2
obj3 = pygame.transform.scale(obj3, (obj3_size, obj3_size)) # escala la rana a 1/2 de la rana original -> es aun mas pequeña
obj3_box = obj3.get_rect()
no_spawn3 = 200
obj3_box.update(random.randint(no_spawn3, width - obj3_size), random.randint(0, height - obj3_size - no_spawn3), obj3_size, obj3_size)

# posicion inicial de la rana
offset = 20
start_pos_x = offset
start_pos_y = height - 64 - offset # pone la posicion de lanzamiento de la rana en la esquina inferior izquierda

score = 0
tries = 3

#definimos constante de gravedad, la fuerza y ángulo inicial
fuerza_cap = 180 #maximo valor de la fuerza
fuerza_str = 20 #minimo valor de la fuerza
fuerza = fuerza_str
charge_time_seg = 2 #tiempo de carga del tiro
angulo = 45
g = 9.8

# Flecha pa apuntar
flecha = pygame.image.load('dot.png') #cambia esto al nombre correcto de tu flecha
flecha = pygame.transform.scale(flecha, (20, 20))
flecha_angulo = flecha  

is_ball_charged = False
is_ball_move = False
tiempo = 0


#convertimos el ángulo en radianes y calculamos las posiciones de x y x usando ecuaciones de movimiento parabolico
def calcular_trayectoria(fuerza, angulo, tiempo):
    angulo_rad = math.radians(angulo)
    x = fuerza * math.cos(angulo_rad) * tiempo
    y = fuerza * math.sin(angulo_rad) * tiempo - 0.5 * g * tiempo ** 2
    return x, y

#creamos una lista de puntos con intervalos de a 5 y los almacenamos en una lista para luego dibujarlos llamando la función calcular trayectoria, sobre la trayectoria de la cánica para el ángulo actual
def dibujar_trayectoria(screen, fuerza, angulo): #codigo es compatible pero no hace uso de esta funcion 
    puntos = []
    total_puntos = 14
    intervalo_t = 5 #intervalos en los que se dibujan los puntos
    for t in range(0, total_puntos * intervalo_t, intervalo_t):  #calculamos puntos para t de 0 a 20 (0.1 * 200)
        tiempo = t / 10
        x, y = calcular_trayectoria(fuerza, angulo, tiempo)
        if 0 <= start_pos_x + x <= width and 0 <= start_pos_y - y <= height:
            puntos.append((start_pos_x + x, start_pos_y - y))
        else:
            break
    for punto in puntos:
        #pygame.draw.circle(screen, (255, 255, 255), (int(punto[0]), int(punto[1])), 10)
        screen.blit(flecha, (int(punto[0]), int(punto[1])))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit() #cerrar pestaña
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f: # cambia a un fondo aleatorio al presionar f incluido el fondo ya en pantalla (a veces no cambia)
                bg = bgs[random.randint(0, len(bgs)-1)]

    # texto con puntaje e intentos
    text_surface = my_font.render('Score: ' + str(score) + '  Tries: ' + str(tries), False, (255, 255, 255))

    # pitagoraso y trigonometria para calcular el angulo en base a la posicion del mouse
    if not is_ball_move:
        a = pygame.mouse.get_pos()[1] - start_pos_y
        b = pygame.mouse.get_pos()[0] - start_pos_x
        c = round(math.sqrt((a*a) + (b*b)), 2)
        angulo = math.degrees(math.asin(round(-a/c, 2)))

    #inputs
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] and not is_ball_move:
        is_ball_charged = True
        fuerza += (fuerza_cap - fuerza_str) / (charge_time_seg * clock.get_fps()) #aumenta la fuerza de modo que llega al maximo al cabo de la cantidad de tiempo dictada por la variable: charge_time_seg
        if fuerza > fuerza_cap:#para que no se pase del maximo
            fuerza = fuerza_cap

    # resetear por si acaso
    if key[pygame.K_e]:
        fuerza = fuerza_str
        is_ball_move = False
        tiempo = 0
        
    
    screen.blit(bg, (0,0))
    #inicia lanzamiento
    if not key[pygame.K_SPACE] and is_ball_charged: #ver las intrucciones en las primeras lineas para ver como funciona espacio
        is_ball_charged = False
        is_ball_move = True
        tiempo = 0
    if is_ball_move:
        tiempo += 0.1
        x, y = calcular_trayectoria(fuerza, angulo, tiempo)
        ballrect.topleft = (start_pos_x + x, start_pos_y - y)
    else:
        ballrect.topleft = (start_pos_x, start_pos_y)
        #dibujar_trayectoria(screen, fuerza, angulo)

    # Resetear posición cuando sale de la pantalla, resta un intento
    if ballrect.x > width + 25 or ballrect.y > height + 25 or ballrect.x < -25:
        ballrect.x = start_pos_x
        ballrect.y = start_pos_y
        is_ball_move = False
        is_ball_charged = False
        tiempo = 0
        tries -= 1
        if tries < 1: #resetea el puntuaje al quedarse sin intentos
            tries = 3
            score = 0
        fuerza = fuerza_str
        angulo = 45

    #colision ranas (el codigo de las tres es igual pero con los valores para cada una)
    if ballrect.colliderect(obj_box):
       obj_box.update(random.randint(no_spawn, width - obj_size), random.randint(0, height - obj_size - no_spawn), obj_size, obj_size)
       score += 1
       tries = 3
       ballrect.x = 0
       is_ball_move = False
       tiempo = 0
       fuerza = fuerza_str
       angulo = 45

    if ballrect.colliderect(obj2_box):
       obj2_box.update(random.randint(no_spawn2, width - obj2_size), random.randint(0, height - obj2_size - no_spawn), obj2_size, obj2_size)
       score += 2
       tries = 3
       ballrect.x = 0
       is_ball_move = False
       tiempo = 0
       fuerza = fuerza_str
       angulo = 45

    if ballrect.colliderect(obj3_box):
       obj3_box.update(random.randint(no_spawn3, width - obj3_size), random.randint(0, height - obj3_size - no_spawn3), obj3_size, obj3_size)
       score += 3
       tries = 3
       ballrect.x = 0
       is_ball_move = False
       tiempo = 0
       fuerza = fuerza_str
       angulo = 45

    #dibujacion
    #screen.blit(bg, (0,0))
    screen.blit(obj, obj_box) #rana1
    screen.blit(obj2, obj2_box) #rana2
    screen.blit(obj3, obj3_box) #rana3
    screen.blit(ball, ballrect) #balin
    
    if not is_ball_move: # dibuja la flecha a modo de mira al apuntar
        flecha_angulo_rotada = pygame.transform.rotate(flecha_angulo, -angulo)
        screen.blit(flecha_angulo_rotada, (start_pos_x + 10 * start_pos_x * math.cos(math.radians(angulo)), start_pos_y - 10 * start_pos_x * math.sin(math.radians(angulo))))
        if is_ball_charged: # al cargar dibuja una segunda flecha como indicativo de la fuerza
            screen.blit(flecha_angulo_rotada, (start_pos_x + (fuerza * 10 / fuerza_cap) * start_pos_x * math.cos(math.radians(angulo)), start_pos_y - (fuerza * 10 / fuerza_cap) * start_pos_x * math.sin(math.radians(angulo))))
    

    screen.blit(flecha, pygame.mouse.get_pos()) # pone una flecha en el cursor
    screen.blit(text_surface, (width - 310,0)) # dibuja texto esquina ↗️
    pygame.display.flip()
    clock.tick(30)

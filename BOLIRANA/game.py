import pygame
from sys import exit
import math


pygame.init()

W, H = 1000,600
PANTALLA = pygame.display.set_mode((W, H))


pygame.display.set_caption('Bolirana')
icono = pygame.image.load('imagenes/icon.png')
pygame.display.set_icon(icono)

#Fondo juego
fondo_surface = pygame.image.load('imagenes/Fondo1.png').convert()
x = 0
fondo_surface = pygame.transform.scale(fondo_surface, (1000,600))


#Música de fondo
#pygame.mixer.music.load('sonido/Musictrack.mp3')
#pygame.mixer.music.play(-1)


#Canica
canica = pygame.image.load('imagenes/canica.png')
canica = pygame.transform.scale(canica, (26.5,23.3))
canica_rect = canica.get_rect()
canica_lanzada = False
canica_velocidad = 0
canica_angulo = 0
canica_tiempo = 0

#Personaje
quieto = pygame.image.load('imagenes/Quieto/Idle.png')
quieto = pygame.transform.scale(quieto, (400,324))

quieto_canica = pygame.image.load('imagenes/Quieto/Idle_canica.png')
quieto_canica = pygame.transform.scale(quieto, (400,324))

camina1 = pygame.image.load('imagenes/Caminando/Walk1.png')
camina1 = pygame.transform.scale(camina1, (400,324))
camina2 = pygame.image.load('imagenes/Caminando/Walk2.png')
camina2 = pygame.transform.scale(camina2, (400,324))
camina3 = pygame.image.load('imagenes/Caminando/Walk3.png')
camina3 = pygame.transform.scale(camina3, (400,324))
camina4 = pygame.image.load('imagenes/Caminando/Walk4.png')
camina4 = pygame.transform.scale(camina4, (400,324))
camina5 = pygame.image.load('imagenes/Caminando/Walk5.png')
camina5 = pygame.transform.scale(camina1, (400,324))
camina6 = pygame.image.load('imagenes/Caminando/Walk6.png')
camina6 = pygame.transform.scale(camina6, (400,324))
camina7 = pygame.image.load('imagenes/Caminando/Walk7.png')
camina7 = pygame.transform.scale(camina7, (400,324))
camina8 = pygame.image.load('imagenes/Caminando/Walk8.png')
camina8 = pygame.transform.scale(camina8, (400,324))

camina1izq = pygame.transform.flip(camina1, True, False)
camina2izq = pygame.transform.flip(camina2, True, False)
camina3izq = pygame.transform.flip(camina3, True, False)
camina4izq = pygame.transform.flip(camina4, True, False)
camina5izq = pygame.transform.flip(camina5, True, False)
camina6izq = pygame.transform.flip(camina6, True, False)
camina7izq = pygame.transform.flip(camina7, True, False)
camina8izq = pygame.transform.flip(camina8, True, False)

#lanzamiento 

lanzamiento1 = pygame.image.load('imagenes/Attack/Attack_1.png')
lanzamiento1 = pygame.transform.scale(lanzamiento1, (400,324))
lanzamiento2 = pygame.image.load('imagenes/Attack/Attack_2.png')
lanzamiento2 = pygame.transform.scale(lanzamiento2, (400,324))
lanzamiento3 = pygame.image.load('imagenes/Attack/Attack_3.png')
lanzamiento3 = pygame.transform.scale(lanzamiento3, (400,324))
lanzamiento4 = pygame.image.load('imagenes/Attack/Attack_4.png')
lanzamiento4 = pygame.transform.scale(lanzamiento4, (400,324))
lanzamiento5 = pygame.image.load('imagenes/Attack/Attack_5.png')
lanzamiento5 = pygame.transform.scale(lanzamiento5, (400,324))
lanzamiento6 = pygame.image.load('imagenes/Attack/Attack_6.png')
lanzamiento6 = pygame.transform.scale(lanzamiento6, (400,324))
lanzamiento7 = pygame.image.load('imagenes/Attack/Attack_7.png')
lanzamiento7 = pygame.transform.scale(lanzamiento7, (400,324))
lanzamiento8 = pygame.image.load('imagenes/Attack/Attack_8.png')
lanzamiento8 = pygame.transform.scale(lanzamiento8, (400,324))
lanzamiento9 = pygame.image.load('imagenes/Attack/Attack_9.png')
lanzamiento9 = pygame.transform.scale(lanzamiento9, (400,324))

#salto

salto1 = pygame.image.load('imagenes/Salto/Jump-1.png')
salto1 = pygame.transform.scale(salto1, (400,324))
salto2 = pygame.image.load('imagenes/Salto/Jump-2.png')
salto2 = pygame.transform.scale(salto2, (400,324))
salto3 = pygame.image.load('imagenes/Salto/Jump-3.png')
salto3 = pygame.transform.scale(salto3, (400,324))
salto4 = pygame.image.load('imagenes/Salto/Jump-4.png')
salto4 = pygame.transform.scale(salto4, (400,324))
salto5 = pygame.image.load('imagenes/Salto/Jump-5.png')
salto5 = pygame.transform.scale(salto5, (400,324))
salto6 = pygame.image.load('imagenes/Salto/Jump-6.png')
salto6 = pygame.transform.scale(salto6, (400,324))
salto7 = pygame.image.load('imagenes/Salto/Jump-7.png')
salto7 = pygame.transform.scale(salto7, (400,324))
salto8 = pygame.image.load('imagenes/Salto/Jump-8.png')
salto8 = pygame.transform.scale(salto8, (400,324))



caminaDerecha = [camina1,camina2,camina3,camina4,camina5,camina6,camina7,camina8]

caminaIzquierda = [camina1izq,camina2izq,camina3izq,camina4izq,camina5izq,camina6izq,camina7izq,camina8izq]

lanzamiento = [lanzamiento2,lanzamiento3,lanzamiento4,lanzamiento5,lanzamiento6,lanzamiento7,lanzamiento8,lanzamiento9]

salto_lista = [salto1,salto2,salto3,salto4,salto5,salto6,salto7, salto8]

x = 0
px = 50
py = 200
ancho = 40
velocidad = 15

salto = False
#altura del salto
cuentaSalto = 10
cuentaSalto_lista = 0

#Variables dirección
izquierda = False
derecha = False

#Variable de lanzamiento
lanzado = False
cuentaLanzamiento = 0
fuerza = 50
angulo = 45
g = 9.81


#pasos
cuentaPasos = 0

def calcular_trayectoria(fuerza, angulo, tiempo):
    g = 9.81  # Aceleración debida a la gravedad
    angulo_rad = math.radians(angulo)
    x = fuerza * math.cos(angulo_rad) * tiempo
    y = fuerza * math.sin(angulo_rad) * tiempo - 0.5 * g * tiempo ** 2
    return x, y


def dibujar_trayectoria(pantalla, fuerza, angulo):
    puntos = []
    for t in range(0,70, 2):
        tiempo = t / 5
        x, y = calcular_trayectoria(fuerza, angulo, tiempo)
        if 0 <= 50 + x <= 200 and 0 <= 300 - y <= 700:
            puntos.append((50 + x, 300 - y))
        else:
            break
    for punto in puntos:
        pygame.draw.circle(PANTALLA, (255, 255, 255), (int(punto[0]), int(punto[1])), 3)


lanzamiento_completado = False

def recargaPantalla():
    global cuentaPasos, lanzado, cuentaLanzamiento, salto, cuentaSalto, cuentaSalto_lista, canica_lanzada, canica_tiempo, lanzamiento_completado
    
    
    #contador de pasos
    if cuentaPasos + 1 >= len(caminaDerecha): #mientras cuenta pasos sea menor a la longitud de la lista- caminaDerecha
        cuentaPasos = 0 #iniciamos cuentaPasos en 0 para acceder a todos los indices de la lista
    if izquierda:
        PANTALLA.blit(caminaIzquierda[cuentaPasos // 1], (px, py))
        cuentaPasos += 1
        
    #tenemos 8 imagenes en la lista caminaIzquierda. el cuentaPasos nos sirve para acceder a cada imagen y ponerla en su respectiva posición. Convertimos a int para que no nos retorne valores float y poner la imagen en esa posicion  
        
    #movimiento a la derecha
    elif derecha:
        PANTALLA.blit(caminaDerecha[cuentaPasos//1], (px, py))
        cuentaPasos += 1
        
    #salto    
    elif salto:
        if cuentaSalto_lista < len(salto_lista):
            
            PANTALLA.blit(salto_lista[cuentaSalto_lista], (px, py))
            cuentaSalto_lista += 1 # si salto se vuelve verdadero accedemos a cada imagen por su indice y vamos sumando uno mientras recoremos la lista de imagenes.
            
        else:
            PANTALLA.blit(salto_lista[-1], (px,py))    
                    
    elif lanzado:
        if cuentaLanzamiento < len(lanzamiento):
            PANTALLA.blit(lanzamiento[cuentaLanzamiento], (px,py))
            cuentaLanzamiento += 1 # si lanzamos y la cuenta del lanzamiento es menor a la longitud de la lista de imagenes de lanzamiento, accedemos a cada indice sumando uno en cada itereación.
        else:    
            lanzado = False
            cuentaLanzamiento = 0
            canica_lanzada = True
            canica_tiempo = 0
            lanzamiento_completado = True #marcamos lanzamiento como completado
            PANTALLA.blit(quieto, (px, py))
            # si no lanzamos ponemos el personaje quieto
            
    
                
     
    else:
        PANTALLA.blit(quieto, (px, py)) 
        
        # actualizar la posición de la canica si ha sido lanzada
    if canica_lanzada:
        canica_tiempo += 0.1  # Incrementar el tiempo para la trayectoria
        x, y = calcular_trayectoria(canica_velocidad, canica_angulo, canica_tiempo)
        canica_rect.x = px + x + 260  # 50 es un ajuste para la posición inicial de la canica
        canica_rect.y = py - y + 150  # 50 es un ajuste para la posición inicial de la canicas
        

    else:
        # Si la canica no está lanzada, dibujarla en la mano del personaje
        PANTALLA.blit(canica, (px + 180, py + 180))
        dibujar_trayectoria(PANTALLA, canica_velocidad, canica_angulo)   
        
    #actualizamos ventana
    PANTALLA.blit(canica, canica_rect)
    pygame.display.update() 
    
          
    

RELOJ = pygame.time.Clock()

ejecuta = True

while ejecuta:
    
    RELOJ.tick(20)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecuta = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #accedemos al mouse
            if event.button == 1: # 1 se refiere a click izquierdo
                lanzado = True
                cuentaLanzamiento = 0 #DOBLE CLICK IZQUIERDO PARA LANZAR
            if event.button == 4: #Rueda hacia arriba
                canica_velocidad += 20
            if event.button == 5: #rueda hacia abajo
                canica_velocidad -= 20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                canica_angulo += 10
            if event.key == pygame.K_DOWN: 
                canica_angulo -= 10                
            
           
                    
                
                   
            
            
    keys = pygame.key.get_pressed() #realice acciones de las teclas manteniendolas pulsadas. Repite el movimiento.
        
    
    #Tecla A: movimiento a la izquierda
    if keys[pygame.K_a] and px > -100:
        px -= velocidad
        izquierda = True
        derecha = False
        
    #Tecla D: movimiento a la derecha
    elif keys[pygame.K_d] and px < 900 - velocidad - ancho: #margenes de tope para que el personaje no se salga de la pantalla
        px += velocidad
        izquierda = False
        derecha = True
    
    #personaje quieto    
    else:
        izquierda = False
        derecha = False
        cuentaPasos = 0 
    
    #Tecla W: movimiento hacia arriba
    if keys[pygame.K_w] and py > 200: #margen de limite
        py -= velocidad            
    
    #Tecla S: movimiento hacia abajo
    if keys[pygame.K_s] and py < 300:
        py += velocidad
        
    #Tecla Space: Salto
    if not salto: #verificamos si el personaje no está saltando
        if keys[pygame.K_SPACE]:
            salto = True #personaje comenzó el salto
            izquierda = False
            derecha = False
            cuentaPasos = 0
            #no vamos a izquierda ni derecha. no contamos pasos
    else:
        # si el salto es true, el personaje está en el aire
        # el salto se controla con la variable cuentaSalto que empieza en 10 y decrece hasta -10.
        if cuentaSalto >= -10:
            py -= cuentaSalto * 3 #le restamos cuentaSalto* 3 a la posición del personaje en y. RECORDAR QUE AL RESTAR ESTAMOS SUBIENDO EL PERSONAJE
            cuentaSalto -= 1 #restamos cuentaSalto en cada ciclo para ir iterando en la animación
            
        else:
            cuentaSalto = 10 #resetamos para el proximo salto
            salto = False 
            cuentaSalto_lista = 0 #Resetear el indice de imagenes del salto para la proxima animacion              
        
                 
            
            
    #PARA MOVER EL FONDO        
    
    #x_relativa = x % fondo_surface.get_rect().width         
    #PANTALLA.blit(fondo_surface, (x_relativa - fondo_surface.get_rect().width , 0))
    #if x_relativa < W:
        #PANTALLA.blit(fondo_surface,(x_relativa,0))
    #x -= 1
    
    PANTALLA.blit(fondo_surface, (0,0))
    
    recargaPantalla() #está función se encarga de actualizar y redibujar todos los elementos de la pantalla en cada ciclo del bucle principal del juego. maneja la animación y el dibujo del personaje según su estado actual (caminando. saltando, lanzando o quieto)
    
pygame.quit()    

    
    


    



       




   

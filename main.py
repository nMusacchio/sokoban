# Alumno: Ignacio Alfredo Musacchio - Padrón N°105815

import soko
import gamelib
from pila import Pila
import solver

TAMAÑO_IMAGEN = 64

DIRECCIONES = {
            "NORTE": (0,-1),
            "SUR": (0,1),
            "ESTE": (1,0),
            "OESTE": (-1,0)
            }
IMAGENES = {
            "#": "wall.gif", 
            " ": "ground.gif",
            "$": "box.gif",
            "@": "player.gif",
            ".": "goal.gif"
            }

def cargar_teclas():
    teclas = {}
    with open("teclas.txt") as f:
        linea = f.readline()
        while linea:
            if linea =="\n": linea = f.readline() 
            linea = linea.rstrip("\n")
            tecla, accion = linea.split(" = ")
            teclas[tecla] = accion
            linea = f.readline()
    return teclas

def cargar_niveles():
    niveles = {}
    with open("niveles.txt") as f:
        nivel = 0
        nuevo_nivel = True
        linea = f.readline()
        while linea:
            if linea == "\n":
                nuevo_nivel = True
                linea = f.readline()
            if nuevo_nivel:
                nivel = nivel+1
                nuevo_nivel = False
            else:
                if linea[0] in IMAGENES:
                    if nivel in niveles:
                        niveles[nivel].append(linea[:-1])
                    else: 
                        niveles[nivel] = [linea[:-1]]
            linea = f.readline()
    return niveles

def reiniciar(juego, niveles, nivel, soluciones):
    return soko.crear_grilla(niveles[int(nivel)])

def pintar_piso(ancho, alto):
    for i in range(alto):
        for j in range(ancho):
            gamelib.draw_image("img/ground.gif", i*TAMAÑO_IMAGEN, j*TAMAÑO_IMAGEN)

def setear_juego(niveles, nivel):
    juego = soko.crear_grilla(niveles[nivel]) 
    resize(juego)
    gamelib.title("Sokoban - Nivel: " + str(nivel))

    return juego


def dibujar(juego):
    alto, ancho = soko.dimensiones(juego)
    pintar_piso(ancho, alto)
    for j in range(len(juego)):
        for i in range(len(juego[j])):
            x = TAMAÑO_IMAGEN*i
            y = TAMAÑO_IMAGEN*j
            if juego[j][i] == "*":
                gamelib.draw_image("img/goal.gif", x, y)
                gamelib.draw_image("img/box.gif", x, y)
            elif juego[j][i] == "+":
                gamelib.draw_image("img/goal.gif", x, y)
                gamelib.draw_image("img/player.gif", x, y)
            else:
                gamelib.draw_image("img/"+IMAGENES[juego[j][i]], x, y)

def resize(juego):
    ancho, largo = soko.dimensiones(juego)

    gamelib.resize(ancho*TAMAÑO_IMAGEN, largo*TAMAÑO_IMAGEN)
    
def deshacer(pila, juego):
    return pila.desapilar()

def main():
    niveles = cargar_niveles()
    nivel = 1
    teclas = cargar_teclas()
    juego = setear_juego(niveles, nivel)
    movimientos = Pila()
    soluciones = Pila()
    mensaje = ""
    while gamelib.is_alive():
        gamelib.draw_begin()
        dibujar(juego)
        gamelib.draw_end()
        gamelib.draw_text(mensaje,15,15,anchor="w")
        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev: break

        tecla = ev.key
        
        if tecla in teclas:
            if teclas[tecla] == "REINICIAR":
                juego = reiniciar(juego, niveles, nivel, soluciones)
            elif teclas[tecla] == "SALIR":
                break
            elif teclas[tecla] == "DESHACER": 
                if movimientos.tope:
                    juego = deshacer(movimientos, juego)
            elif teclas[tecla] == "AYUDA":
                if soluciones.esta_vacia():
                    gamelib.draw_text("Pensando...", 15, 15, anchor="w")
                    gamelib.get_events() #Utilizo .get_events() como una especie de mutex para evitar que el usuario interactúe
                    solucion_encontrada, soluciones = solver.buscar_solucion(juego, DIRECCIONES)
                    gamelib.get_events()
                    if solucion_encontrada:
                        mensaje = "Hay pista disponible"
                    else:
                        mensaje = "No hay chance"
                else:
                    movimientos.apilar(juego)
                    juego = soko.mover(juego, soluciones.desapilar())
            else:
                movimientos.apilar(juego)
                juego = soko.mover(juego, DIRECCIONES[teclas[tecla]])

            if tecla and not teclas[tecla] == "AYUDA":
                soluciones = Pila()
                mensaje = ""

            if soko.juego_ganado(juego):
                nivel = nivel + 1
                juego = setear_juego(niveles, nivel)
                movimientos = Pila()

gamelib.init(main)
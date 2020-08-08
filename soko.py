"""Nombre: Ignacio Alfredo Musacchio - Padron: 105815"""

def crear_grilla(desc):
    grilla = []
    for fila in desc:
        fila_grilla = []
        for col in fila:
            fila_grilla.append(col)
        grilla.append(fila_grilla)
    return grilla

def dimensiones(grilla):
    max_ancho = 0
    for fila in grilla:
        if len(fila)>max_ancho:
            max_ancho = len(fila)
    return max_ancho, len(grilla)

def hay_pared(grilla, c, f):
    return grilla[f][c] == "#"

def hay_objetivo(grilla, c, f):
    tipos_objetivos = [".", "*", "+"]
    return grilla[f][c] in tipos_objetivos

def hay_caja(grilla, c, f):
    return grilla[f][c] == "$" or grilla[f][c] == "*"

def hay_jugador(grilla, c, f):
    return grilla[f][c] == "@" or grilla[f][c] == "+"

def juego_ganado(grilla):
    for fila in grilla:
        if "." in fila or "+" in fila:
            return False

    return True

def posicion_jugador(grilla): #Función que devuelve una tupla con las coordenadas del jugador
    for fila in range(len(grilla)):
        for col in range(len(grilla[fila])):
            if hay_jugador(grilla, col, fila):
                return (fila,col)

def mover_caja(grilla, pos_caja_x, pos_caja_y, direc_x, direc_y): #Realiza el movimiento de la caja
    if hay_objetivo(grilla, pos_caja_x + direc_x, pos_caja_y + direc_y) and hay_objetivo(grilla, pos_caja_x,pos_caja_y):
        pos_actual, pos_siguiente = ".", "*"
    elif hay_objetivo(grilla, pos_caja_x + direc_x, pos_caja_y + direc_y):
        pos_actual, pos_siguiente = " ", "*"
    elif hay_objetivo(grilla, pos_caja_x,pos_caja_y):
        pos_actual, pos_siguiente = ".", "$"
    else:
        pos_actual, pos_siguiente = grilla[pos_caja_y + direc_y][pos_caja_x + direc_x], grilla[pos_caja_y][pos_caja_x]

    grilla[pos_caja_y][pos_caja_x], grilla[pos_caja_y + direc_y][pos_caja_x + direc_x] = pos_actual, pos_siguiente

    return grilla

def mover_personaje(nueva_grilla, pos_jug_x,pos_jug_y,direc_x,direc_y):
    if nueva_grilla[pos_jug_y][pos_jug_x] == "+": #Si estoy en un objetivo y salgo de ahi
        if nueva_grilla[pos_jug_y+direc_y][pos_jug_x+direc_x] == ".":
            pos_actual, pos_siguiente = ".", "+"    
        else:
            pos_actual, pos_siguiente = ".", "@"
    elif nueva_grilla[pos_jug_y+direc_y][pos_jug_x+direc_x] == ".":
        pos_actual, pos_siguiente = " ", "+"
    else:
        pos_actual, pos_siguiente = nueva_grilla[pos_jug_y+direc_y][pos_jug_x+direc_x], nueva_grilla[pos_jug_y][pos_jug_x]
    
    nueva_grilla[pos_jug_y][pos_jug_x], nueva_grilla[pos_jug_y+direc_y][pos_jug_x+direc_x] = pos_actual, pos_siguiente

    return nueva_grilla

def clonar_grilla(grilla): 
    nueva_grilla = []
    for i in range(len(grilla)):
        fila = []
        for j in range(len(grilla[i])):
            fila.append(grilla[i][j])
        nueva_grilla.append(fila)

    return nueva_grilla
        
def mover(grilla, direccion):
    nueva_grilla = clonar_grilla(grilla)
    jugador = posicion_jugador(nueva_grilla)

    pos_jug_x = jugador[1]
    pos_jug_y = jugador[0]
    direc_x = direccion[0]
    direc_y = direccion[1]

    if hay_pared(nueva_grilla, pos_jug_x+direc_x, pos_jug_y+direc_y):
        return nueva_grilla 
    
    if hay_caja(nueva_grilla,pos_jug_x+direc_x, pos_jug_y+direc_y):
        if hay_caja(nueva_grilla, pos_jug_x+direc_x*2, pos_jug_y+direc_y*2) or hay_pared(nueva_grilla, pos_jug_x+direc_x*2, pos_jug_y+direc_y*2):
            return nueva_grilla
        
        mover_caja(nueva_grilla, pos_jug_x+direc_x, pos_jug_y+direc_y, direc_x, direc_y)
    
    mover_personaje(nueva_grilla, pos_jug_x, pos_jug_y, direc_x, direc_y)

    return nueva_grilla

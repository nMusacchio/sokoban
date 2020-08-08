"""Nombre: Ignacio Alfredo Musacchio - Padron: 105815"""
import soko
from pila import Pila

def transformar(estado):
    estado_inmutable = ""
    for fila in estado:
        for columna in fila: 
            estado_inmutable += columna
    
    return estado_inmutable

def buscar_solucion(estado_inicial, direcciones):
    visitados = set()
    solucion_encontrada, acciones = backtrack(estado_inicial, visitados, direcciones)
    
    return solucion_encontrada, acciones

def backtrack(estado, visitados, direcciones):
    visitados.add(transformar(estado))
    if soko.juego_ganado(estado):
        return True, Pila()

    for direccion in direcciones.values():
        nuevo_estado = soko.mover(estado, direccion)
        if transformar(nuevo_estado) in visitados:
            continue
        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados, direcciones)
        if solucion_encontrada:
            acciones.apilar(direccion)
            return True, acciones

    return False, None

    
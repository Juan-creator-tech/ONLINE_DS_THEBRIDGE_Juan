# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:47:00 2024

@author: juanmoreno
"""

# funciones.py
import random
from clases import Tablero

def generar_coordenada_aleatoria():
    return random.randint(0, 9), random.randint(0, 9)

def mostrar_mensaje_bienvenida():
    print("¡Bienvenido al juego de Hundir la Flota! Intenta hundir todos los barcos enemigos.")

def verificar_fin_juego(jugador, maquina):
    if jugador.barcos_restantes == 0:
        print("¡Te acaba de ganar una máquina XD! Vuelve cuando quieras a intentarlo de nuevo ;-3")
        return True
    elif maquina.barcos_restantes == 0:
        print("Enhorabuena, ¡Has ganado! Esperamos que hayas disfrutado de nuestro juego, ¡vuelve pronto!")
        return True
    return False

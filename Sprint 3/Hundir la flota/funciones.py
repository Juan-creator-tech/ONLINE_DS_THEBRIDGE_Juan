# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:47:00 2024

@author: juanmoreno
"""

# funciones.py
import random
from variables import DIMENSIONES_TABLERO, BARCOS, AGUA, BARCO, IMPACTO, FALLO, HUNDIDO, BORDE
from clases import Tablero

def mostrar_mensaje_bienvenida():
    print("¡Bienvenido al juego de Hundir la Flota! Intenta hundir todos los barcos enemigos.")

def seleccionar_nivel():
    print("Selecciona el nivel de dificultad:")
    print("1. Fácil: La máquina dispara aleatoriamente.")
    print("2. Medio: La máquina busca coordenadas adyacentes al impactar.")
    print("3. Difícil: La máquina combina disparos aleatorios y dirigidos.")
    while True:
        try:
            nivel = int(input("Elige el nivel (1-3): "))
            if nivel in [1, 2, 3]:
                return nivel
            else:
                print("Por favor, introduce un número válido (1, 2 o 3).")
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número.")

def verificar_fin_juego(jugador, maquina):
    if jugador.barcos_restantes == 0:
        print("¡Te acaba de ganar una máquina XD! Vuelve cuando quieras a intentarlo de nuevo ;-3")
        return True
    elif maquina.barcos_restantes == 0:
        print("Enhorabuena, ¡Has ganado! Esperamos que hayas disfrutado de nuestro juego, ¡vuelve pronto!")
        return True
    return False

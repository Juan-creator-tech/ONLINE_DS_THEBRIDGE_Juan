# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:46:15 2024

@author: juanmoreno
"""

# clases.py
import numpy as np
from variables import DIMENSIONES_TABLERO, BARCOS, AGUA, BARCO, IMPACTO, FALLO, HUNDIDO, BORDE
import random

class Tablero:
    def __init__(self, id_jugador):
        self.id_jugador = id_jugador
        self.tablero = np.full((DIMENSIONES_TABLERO, DIMENSIONES_TABLERO), AGUA)
        self.disparos = np.full((DIMENSIONES_TABLERO, DIMENSIONES_TABLERO), AGUA)
        self.barcos = []  # Lista para almacenar las posiciones de cada barco
        self.barcos_restantes = sum([BARCOS[barco]['cantidad'] * BARCOS[barco]['eslora'] for barco in BARCOS])
        self.colocar_barcos()

    def colocar_barcos(self):
        for tipo, datos in BARCOS.items():
            for _ in range(datos['cantidad']):
                intentos = 0
                while intentos < 100:  # Limite de intentos para evitar bucles infinitos
                    fila, columna = random.randint(0, DIMENSIONES_TABLERO - 1), random.randint(0, DIMENSIONES_TABLERO - 1)
                    orientacion = random.choice(['H', 'V'])
                    if self.validar_espacio(fila, columna, datos['eslora'], orientacion):
                        coordenadas_barco = self.posicionar_barco(fila, columna, datos['eslora'], orientacion)
                        self.barcos.append(coordenadas_barco)
                        break
                    intentos += 1
                if intentos >= 100:
                    print(f"No se pudo colocar el barco {tipo} de eslora {datos['eslora']} después de muchos intentos.")
                    return  # Sale del bucle si no encuentra un espacio válido

    def validar_espacio(self, fila, columna, eslora, orientacion):
        def espacio_libre(f, c):
            if 0 <= f < DIMENSIONES_TABLERO and 0 <= c < DIMENSIONES_TABLERO:
                return self.tablero[f, c] == AGUA
            return False

        for i in range(eslora):
            if orientacion == 'H':
                if not (espacio_libre(fila, columna + i) and
                        all(espacio_libre(fila + df, columna + i + dc)
                            for df in [-1, 0, 1] for dc in [-1, 0, 1])):
                    return False
            elif orientacion == 'V':
                if not (espacio_libre(fila + i, columna) and
                        all(espacio_libre(fila + i + df, columna + dc)
                            for df in [-1, 0, 1] for dc in [-1, 0, 1])):
                    return False
        return True

    def posicionar_barco(self, fila, columna, eslora, orientacion):
        coordenadas = []
        for i in range(eslora):
            if orientacion == 'H':
                self.tablero[fila, columna + i] = BARCO
                coordenadas.append((fila, columna + i))
            else:
                self.tablero[fila + i, columna] = BARCO
                coordenadas.append((fila + i, columna))
        return coordenadas

    def disparo(self, fila, columna):
        if self.tablero[fila, columna] == BARCO:
            self.tablero[fila, columna] = IMPACTO
            self.disparos[fila, columna] = IMPACTO
            hundido = self.verificar_hundimiento(fila, columna)
            if hundido:
                print("¡Barco hundido!")
            self.barcos_restantes -= 1
            return True, hundido  # Impacto y hundimiento si aplica
        else:
            self.disparos[fila, columna] = FALLO
            return False, False  # Agua y no hundido

    def verificar_hundimiento(self, fila, columna):
        for barco in self.barcos:
            if (fila, columna) in barco:
                if all(self.tablero[f, c] == IMPACTO for f, c in barco):
                    self.marcar_hundido(barco)
                    return True
        return False

    def marcar_hundido(self, barco):
        for f, c in barco:
            self.tablero[f, c] = HUNDIDO
        self.recuadrar_barco(barco)

    def recuadrar_barco(self, barco):
        for f, c in barco:
            for df in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nf, nc = f + df, c + dc
                    if 0 <= nf < DIMENSIONES_TABLERO and 0 <= nc < DIMENSIONES_TABLERO:
                        if self.tablero[nf, nc] == AGUA:
                            self.tablero[nf, nc] = BORDE

    def mostrar_tablero(self, visible=False):
        if visible:
            print("\n".join(" ".join(row) for row in self.tablero))
        else:
            print("\n".join(" ".join(row) for row in self.disparos))

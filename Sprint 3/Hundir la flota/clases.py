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
        """
        Muestra el tablero. Si visible=True, muestra los barcos, disparos y hundimientos.
        Si visible=False, oculta los barcos no impactados, pero muestra los disparos realizados.
        """
        tablero_a_mostrar = self.tablero.copy()  # Crea una copia del tablero
        for fila in range(DIMENSIONES_TABLERO):
            for columna in range(DIMENSIONES_TABLERO):
                if not visible and tablero_a_mostrar[fila, columna] == BARCO:
                    # Oculta los barcos no impactados si el tablero no es visible
                    tablero_a_mostrar[fila, columna] = AGUA
                elif self.disparos[fila, columna] == FALLO:
                    # Muestra los disparos fallidos como 'O'
                    tablero_a_mostrar[fila, columna] = FALLO
                elif self.disparos[fila, columna] == IMPACTO:
                    # Muestra los impactos como '*'
                    tablero_a_mostrar[fila, columna] = IMPACTO
        # Imprime el tablero procesado
        print("\n".join(" ".join(row) for row in tablero_a_mostrar))

class DisparoMaquina:
    def __init__(self, nivel):
        self.nivel = nivel
        self.impacto_previo = None  # Guarda la última coordenada con impacto
        self.intentos_adyacentes = []  # Lista de coordenadas adyacentes a probar
        self.disparos_realizados = set()  # Coordenadas ya disparadas
        self.turnos_hasta_trampa = 3  # Para nivel difícil, cuenta disparos aleatorios

    def disparar(self, jugador, dimensiones):
        fila, columna = None, None
    
        if self.nivel == 1:  # Fácil
            while True:
                fila, columna = self.generar_coordenada_aleatoria()
                if (fila, columna) not in self.disparos_realizados:
                    break
    
        elif self.nivel in [2, 3]:  # Medio y Difícil comparten lógica de disparos dirigidos
            # Nivel 3: Comprobar si es el turno "trampa"
            if self.nivel == 3 and self.turnos_hasta_trampa == 0:
                # Turno "trampa": Seleccionar una coordenada con un barco del jugador
                for barco in jugador.barcos:
                    for f, c in barco:
                        if (f, c) not in self.disparos_realizados:
                            fila, columna = f, c
                            break
                    if fila is not None and columna is not None:
                        break
                self.turnos_hasta_trampa = 3  # Reiniciar contador
            else:
                if self.nivel == 3:
                    self.turnos_hasta_trampa -= 1
    
                # Disparos dirigidos basados en impactos previos
                if self.impacto_previo:
                    impactos = self.obtener_impactos_consecutivos()
                    
                    if len(impactos) >= 2:
                        # Determinar alineación y disparar en los extremos
                        alineacion = self.determinar_alineacion(impactos)
                        if alineacion == "horizontal":
                            fila = impactos[0][0]
                            extremos = [(fila, impactos[0][1] - 1), (fila, impactos[-1][1] + 1)]
                        elif alineacion == "vertical":
                            columna = impactos[0][1]
                            extremos = [(impactos[0][0] - 1, columna), (impactos[-1][0] + 1, columna)]
                        
                        # Elegir el primer extremo válido
                        for f, c in extremos:
                            if 0 <= f < dimensiones and 0 <= c < dimensiones and (f, c) not in self.disparos_realizados:
                                fila, columna = f, c
                                break
    
                    if fila is None or columna is None:
                        # Si no hay alineación o extremos válidos, dispara adyacente
                        if self.intentos_adyacentes:
                            fila, columna = self.intentos_adyacentes.pop()
                        else:
                            self.intentos_adyacentes = self.generar_adyacentes(*self.impacto_previo, dimensiones)
                            fila, columna = self.intentos_adyacentes.pop()
                else:
                    # Disparo aleatorio hasta impactar
                    while True:
                        fila, columna = self.generar_coordenada_aleatoria()
                        if (fila, columna) not in self.disparos_realizados:
                            break
    
        # Registra el disparo realizado
        self.disparos_realizados.add((fila, columna))
        return fila, columna
    
    def obtener_impactos_consecutivos(self):
        # Devuelve las coordenadas de impactos consecutivos basados en self.disparos_realizados
        impactos = [
            (f, c) for f, c in self.disparos_realizados
            if (f, c) in self.intentos_adyacentes or self.impacto_previo == (f, c)
        ]
        return sorted(impactos)
    
    def determinar_alineacion(self, impactos):
        # Determina si los impactos están alineados horizontal o verticalmente
        if all(f == impactos[0][0] for f, _ in impactos):
            return "horizontal"
        elif all(c == impactos[0][1] for _, c in impactos):
            return "vertical"
        return None

    def registrar_impacto(self, fila, columna, impacto, hundido, dimensiones):
        if impacto and not hundido:
            self.impacto_previo = (fila, columna)
            self.intentos_adyacentes = self.generar_adyacentes(fila, columna, dimensiones)
        elif hundido:
            self.impacto_previo = None
            self.intentos_adyacentes = []

    def generar_adyacentes(self, fila, columna, dimensiones):
        adyacentes = [
            (fila + 1, columna), (fila - 1, columna),
            (fila, columna + 1), (fila, columna - 1)
        ]
        return [
            (f, c) for f, c in adyacentes
            if 0 <= f < dimensiones and 0 <= c < dimensiones
        ]

    def generar_coordenada_aleatoria(self):
        return random.randint(0, DIMENSIONES_TABLERO-1), random.randint(0, DIMENSIONES_TABLERO-1)
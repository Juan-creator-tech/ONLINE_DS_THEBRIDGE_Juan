# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:44:35 2024

@author: juanmoreno
"""

# variables.py

# Dimensiones del tablero
DIMENSIONES_TABLERO = 15

# Configuración de los barcos
BARCOS = {
    'barco_1': {'cantidad': 4, 'eslora': 1},
    'barco_2': {'cantidad': 3, 'eslora': 2},
    'barco_3': {'cantidad': 2, 'eslora': 3},
    'barco_4': {'cantidad': 1, 'eslora': 4}
}

# Caracteres para representar el tablero
AGUA = '~'
BARCO = 'P'
IMPACTO = '*'
FALLO = 'X'
HUNDIDO = '#'
BORDE = 'X'

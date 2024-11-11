# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:50:45 2024

@author: juanmoreno
"""

# main.py
import random
from clases import Tablero
from funciones import mostrar_mensaje_bienvenida, verificar_fin_juego, generar_coordenada_aleatoria

def main():
    mostrar_mensaje_bienvenida()
    jugador = Tablero(id_jugador=input("Introduce tu nombre o alias: "))
    maquina = Tablero(id_jugador="Soy la Máquina ;-3")

    turno_jugador = True
    while True:
        if turno_jugador:
            # Turno del jugador
            try:
                fila = int(input("Ingresa la fila (0-9): "))
                columna = int(input("Ingresa la columna (0-9): "))
                
                # Realiza el disparo en el tablero de la máquina
                impacto, hundido = maquina.disparo(fila, columna)
                
                # Mensajes de impacto o agua con mensajes aleatorios
                if impacto:
                    respuestas = [
                        "¡Impacto!", 
                        "¡Un disparo perfecto!", 
                        "Podía haber sido peor... ¡te podía haber pasado a ti! ¡Blanco!"
                    ]
                    print(random.choice(respuestas))
                    if hundido:
                        print("¡Has hundido un barco de la máquina!")
                else:
                    respuestas = [
                        "Agua.", 
                        "Donde pones el ojo, ¡bala de cañon que pierdes!", 
                        "Hoy no es tu día, ¡agua!", 
                        "¿quieres un vaso de... sí, eso, ¡agua!"
                    ]
                    print(random.choice(respuestas))
                    turno_jugador = False  # Cambia de turno si falla
            except ValueError:
                print("Ups, parece que quieres huir o no sabes bien a donde disparas. ¡Inténtalo de nuevo!.")

            print("\n--- Disparos realizados en el tablero de la Máquina ---")
            maquina.mostrar_tablero()

        else:
            # Turno de la máquina
            print("¡Mi turno! A ver a dónde te disparo...")
            fila, columna = generar_coordenada_aleatoria()
            print(f"Creo que te dispararé en las coordenadas {fila, columna} a ver si hay suerte")
            
            # Realiza el disparo en el tablero del jugador
            impacto, hundido = jugador.disparo(fila, columna)
            
            # Mensajes de impacto o agua de la máquina con respuestas aleatorias
            if impacto:
                respuestas = [
                    "¡Soy la Máquina, y te hago pupa!", 
                    "Un disparo teledirigido, ¡Te han dado!", 
                    "¡La era de los robots ha llegado, muahaha! ¡Voy a destruirte!"
                ]
                print(random.choice(respuestas))
                if hundido:
                    print("La máquina ha hundido uno de tus barcos.")
            else:
                print("¡Vaya, fallé!. La próxima no tendrás tanta suerte ;-3")
                turno_jugador = True  # Cambia de turno si falla

            print("\n--- Tu tablero ---")
            jugador.mostrar_tablero(visible=True)
            
        # Verifica si el juego ha terminado
        if verificar_fin_juego(jugador, maquina):
            break

if __name__ == "__main__":
    main()


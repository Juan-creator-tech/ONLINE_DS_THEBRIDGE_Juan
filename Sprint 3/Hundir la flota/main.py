# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:50:45 2024

@author: juanmoreno
"""

# main.py
import random
import time  # Importa el módulo para pausas
from variables import DIMENSIONES_TABLERO, BARCOS, AGUA, BARCO, IMPACTO, FALLO, HUNDIDO, BORDE
from clases import Tablero, DisparoMaquina
from funciones import mostrar_mensaje_bienvenida, verificar_fin_juego, seleccionar_nivel

def main():
    mostrar_mensaje_bienvenida()
    nivel = seleccionar_nivel()
    jugador = Tablero(id_jugador=input("Introduce tu nombre o alias: "))
    maquina = Tablero(id_jugador="Soy la Máquina ;-3")
    disparador = DisparoMaquina(nivel)  # Controlador de disparos de la máquina
    
    turno_jugador = True
    while True:
        if turno_jugador:
            # Turno del jugador
            try:
                print("¡Es tu turno de disparo!")
                print("\n--- Disparos realizados en el tablero de la Máquina ---")
                maquina.mostrar_tablero(visible=False)
                
                fila = int(input(f"Ingresa la fila (0-{DIMENSIONES_TABLERO}): "))
                columna = int(input(f"Ingresa la columna (0-{DIMENSIONES_TABLERO}): "))
                if not (0 <= fila < DIMENSIONES_TABLERO) or not (0 <= columna < DIMENSIONES_TABLERO):
                    print("¡Coordenadas fuera de los límites! Inténtalo de nuevo.")
                    continue

                # Realiza el disparo en el tablero de la máquina
                impacto, hundido = maquina.disparo(fila, columna)
                
                # Mensajes de impacto o agua con mensajes aleatorios
                if impacto:
                    respuestas = [
                        "¡Impacto!", 
                        "¡Un disparo perfecto!", 
                        "Podía haber sido peor... ¡te podía haber pasado a ti! ¡Blanco!",
                        "¡Directo al objetivo!",
                        "¡Qué puntería! ¡Le has dado!",
                        "¡Bum! ¡El barco está tocado!",
                        "¡Increíble disparo, lo has alcanzado!",
                        "¡Esto va a doler! ¡Blanco perfecto!",
                        "¡Bien hecho! Otro barco en peligro."
                    ]
                    print(random.choice(respuestas))
                    if hundido:
                        print("¡Has hundido un barco de la máquina!")
                else:
                    respuestas = [
                        "Agua.", 
                        "Donde pones el ojo, ¡bala de cañon que pierdes!", 
                        "Hoy no es tu día, ¡agua!", 
                        "¿quieres un vaso de... sí, eso, ¡agua!",
                        "¡Plaf! Solo has salpicado.",
                        "¡Nada por aquí, sigue buscando!",
                        "¡Oops! Te has pasado de largo.",
                        "¡El mar agradece tu contribución!",
                        "¡Fallo! El barco estaba en otra parte."
                    ]
                    print(random.choice(respuestas))
                    turno_jugador = False  # Cambia de turno si falla
                
                # Retardo para dar tiempo al jugador a procesar el resultado
                time.sleep(2)  # Pausa de 2 segundos antes del siguiente disparo
                
            except ValueError:
                print("Ups, parece que quieres huir o no sabes bien a donde disparas. ¡Inténtalo de nuevo!.")
            
            # Retardo para dar tiempo al jugador a procesar el resultado
            time.sleep(2)  # Pausa de 2 segundos antes del siguiente disparo
            
            print("\n--- Disparos realizados en el tablero de la Máquina ---")
            maquina.mostrar_tablero(visible=False)

        else:
            # Turno de la máquina
            print("¡Mi turno! A ver a dónde te disparo...")
            fila, columna = disparador.disparar(jugador, DIMENSIONES_TABLERO)
            print(f"Creo que te dispararé en las coordenadas {fila, columna} a ver si hay suerte")
            
            # Retardo para dar tiempo al jugador a procesar el resultado
            time.sleep(2)  # Pausa de 2 segundos antes del siguiente disparo
            
            # Realiza el disparo en el tablero del jugador
            impacto, hundido = jugador.disparo(fila, columna)
            
            # Mensajes de impacto o agua de la máquina con respuestas aleatorias
            if impacto:
                respuestas = [
                    "¡Soy la Máquina, y te hago pupa!", 
                    "Un disparo teledirigido, ¡Te han dado!", 
                    "¡La era de los robots ha llegado, muahaha! ¡Voy a destruirte!",
                    "¡Zas! ¿Te dolió? ¡Impacto directo!",
                    "¡Otro golpe maestro de la Máquina!",
                    "¿Eso fue suerte? No, ¡es mi precisión perfecta!",
                    "¡Tocado y casi hundido, humano!",
                    "¡Soy imparable! ¡Un impacto más para mí!",
                    "¡No puedes escapar de mis cálculos!"
                ]
                print(random.choice(respuestas))
                
                disparador.registrar_impacto(fila, columna, impacto, hundido, DIMENSIONES_TABLERO)
                
                if hundido:
                    print("La máquina ha hundido uno de tus barcos.")
            else:
                print("¡Vaya, fallé!. La próxima no tendrás tanta suerte ;-3")
                turno_jugador = True  # Cambia de turno si falla
            
            # Retardo para dar tiempo al jugador a procesar el resultado
            time.sleep(2)  # Pausa de 2 segundos antes del siguiente disparo
            
            print("\n--- Tu tablero ---")
            jugador.mostrar_tablero(visible=True)
            
            # Retardo para dar tiempo al jugador a procesar el resultado
            time.sleep(2)  # Pausa de 2 segundos antes del siguiente disparo
            
        # Verifica si el juego ha terminado
        if verificar_fin_juego(jugador, maquina):
            break

if __name__ == "__main__":
    main()


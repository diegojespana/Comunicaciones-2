import numpy as np
import math


texto=input("introduzca el valor que se desea: ")#sirve para introducir letras con el teclado y que el programa no avanze
print(texto)
texto = texto.upper().strip().replace(" ", "");#se ponen mayusculas se extraen caracteres y se eliminan espacios
print(texto)
print(texto[1])

diccionario_letras = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8,
                          'J': 9,'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16,
                          'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
                          'Z': 25}
print(diccionario_letras[texto[1]])


from socket import *
import threading
import os
import sys

import gtts

from connection import set_connection
from colors import print_color, format_string
import string
from sympy import Matrix
import numpy as np
import random
from playsound import playsound
from gtts import gTTS

language = 'es'

llave = np.array([
    [2, 5],
    [3, 4]
])

matpi = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4, 6, 2, 6, 4, 3, 3, 8, 3, 2, 7, 9, 5, 2,
                  8, 8, 4, 1, 9, 7, 1, 6, 9, 3, 9, 9, 3, 7, 5, 1, 0, 5, 8, 2, 9, 7, 4, 9, 4, 4, 5, 9])

filas = llave.shape[0]
columnas = llave.shape[1]

# Obtener matriz inversa de matriz llave
llave_inversa = Matrix(llave).inv_mod(26)
llave_inversa = np.array(llave_inversa)  # sympy to numpy
llave_inversa = llave_inversa.astype(float)

# Funcion para pasar de numeros a letras
diccionario_numeros = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G ', 7: 'H', 8: 'I', 9: 'J', 10: 'K',
                       11: 'L', 12: 'M',
                       13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W',
                       23: 'X', 24: 'Y',
                       25: 'Z'}


# funcion para pasar de letras a numeros
def letrasanumeros(letter):
    return string.ascii_lowercase.index(letter)


CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_IP = ''
SERVER_PORT = 0


def receive():
    while True:
        try:
            message = CLIENT_SOCKET.recv(1024).decode('ascii')

            if message == 'USER':
                CLIENT_SOCKET.send(USERNAME.encode())
            else:
                print(message)
                tts = gtts.gTTS(text=message, lang=language, slow=True)
                tts.save("mensaje.mp3")
                playsound("mensaje.mp3")

        except:
            print_color('')


def wait_for_input():
    while True:
        message1 = input('')
        mensaje = []

        for i in range(0, len(message1)):  # Se convierten todas las letras a minusculas
            current_letter = message1[i:i + 1].lower()
            if current_letter != ' ':  # se eliminan los espacios
                letter_index = letrasanumeros(current_letter)  # se convierten las letras a numeros
                mensaje.append(letter_index)

        if len(mensaje) % filas != 0:  # Se almacenan los numeros en un array
            for i in range(0, len(mensaje)):
                mensaje.append(mensaje[i])
                if len(mensaje) % filas == 0:
                    break

        mensaje = np.array(mensaje)
        cociente = np.array(mensaje)
        binario = []
        d = ""
        m = ""
        m2 = ""
        cifrado = random.randint(0, 2)

        if cifrado == 0:

            for i in range(0, len(mensaje)):
                mensaje[i] = mensaje[i] + 3
                if mensaje[i] > 25:
                    mensaje[i] = mensaje[i] - 26
            for i in range(0, len(mensaje)):
                m = m + diccionario_numeros[mensaje[i]]
                binario.append(np.binary_repr(mensaje[i]))
            for i in range(0, len(binario), 1):
                d = d + binario[i]
        elif cifrado == 2:

            for i in range(0, len(mensaje)):
                mensaje[i] = mensaje[i] * matpi[i]
                cociente[i] = mensaje[i] // 26
                mensaje[i] = mensaje[i] % 26

            for i in range(0, len(mensaje)):
                m = m + diccionario_numeros[mensaje[i]]
                binario.append(np.binary_repr(mensaje[i]))
            for i in range(0, len(mensaje)):
                m = m + diccionario_numeros[cociente[i]]
            for i in range(0, len(binario), 1):
                d = d + binario[i]
        elif cifrado == 1:

            mensaje_largo = mensaje.shape[0]
            mensaje.resize(int(mensaje_largo / filas), filas)  # se ordenan los numeros en pares

            encriptacion = np.matmul(mensaje, llave)  # se multiplica la matriz mensaje por la matriz llave
            encriptacion = np.remainder(encriptacion, 26)  # se saca el modulo de 26 del valor obtenido

            for i in range(0, mensaje_largo // filas, 1):  # se imprime el mensaje encriptado
                for j in range(0, 2, 1):
                    binario.append(np.binary_repr(encriptacion[i][j]))

            for i in range(0, mensaje_largo // filas, 1):
                for j in range(0, 2, 1):
                    m = m + diccionario_numeros[encriptacion[i][j]]
            for i in range(0, len(binario), 1):
                d = d + binario[i]

        data = list(d)
        data.reverse()
        n, p2, p3, n_paridad, h = 0, 0, 0, 0, []

        while (len(d) + n_paridad + 1) > (pow(2, n_paridad)):
            n_paridad = n_paridad + 1

        for i in range(0, (n_paridad + len(data))):
            p = (2 ** n)

            if p == (i + 1):
                h.append(0)
                n = n + 1

            else:
                h.append(int(data[p3]))
                p3 = p3 + 1

        for parity in range(0, (len(h))):
            ph = (2 ** p2)
            if ph == (parity + 1):
                startIndex = ph - 1
                i = startIndex
                toXor = []

                while i < len(h):
                    block = h[i:i + ph]
                    toXor.extend(block)
                    i += 2 * ph

                for z in range(1, len(toXor)):
                    h[startIndex] = h[startIndex] ^ toXor[z]
                p2 += 1

        bit_error = random.randint(0, (len(h) - 1))
        error = random.randint(0, 1)

        h[bit_error] = error

        h.reverse()

        d2 = h
        data2 = list(d2)
        data2.reverse()
        c2, ch2, j3, r2, error2, h2, parity_list2, h_copy2 = 0, 0, 0, 0, 0, [], [], []

        for k2 in range(0, len(data2)):
            p4 = (2 ** c2)
            h2.append(int(data2[k2]))
            h_copy2.append(data2[k2])
            if p4 == (k2 + 1):
                c2 = c2 + 1

        for parity2 in range(0, (len(h2))):
            ph2 = (2 ** ch2)
            if ph2 == (parity2 + 1):

                startIndex2 = ph2 - 1
                i2 = startIndex2
                toXor2 = []

                while i2 < len(h2):
                    block2 = h2[i2:i2 + ph2]
                    toXor2.extend(block2)
                    i2 += 2 * ph2

                for z2 in range(1, len(toXor2)):
                    h2[startIndex2] = h2[startIndex2] ^ toXor2[z2]
                parity_list2.append(h2[parity2])
                ch2 += 1
        parity_list2.reverse()
        error2 = sum(int(parity_list2) * (2 ** i2) for i2, parity_list2 in enumerate(parity_list2[::-1]))

        if error == 0:
            h_copy2.reverse()
        else:
            if h_copy2[error2 - 1] == '0':
                h_copy2[error2 - 1] = '1'
                h_copy2.reverse()
            elif h_copy2[error2 - 1] == '1':
                h_copy2[error2 - 1] = '0'
                h_copy2.reverse()

        cif = cifrado

        if cif == 1:

            mensaje2 = []

            for i in range(0, len(m)):
                current_letter = m[i:i + 1].lower()
                if current_letter != ' ':  # discard blank characters
                    letter_index = letrasanumeros(current_letter)
                    mensaje2.append(letter_index)

            if len(mensaje2) % filas != 0:
                for i in range(0, len(mensaje2)):
                    mensaje2.append(mensaje[i])
                    if len(mensaje2) % filas == 0:
                        break

            mensaje2 = np.array(mensaje2)
            mensaje_largo2 = mensaje2.shape[0]
            mensaje2.resize(int(mensaje_largo2 / filas), filas)

            encriptacion2 = np.matmul(mensaje2, llave_inversa)
            encriptacion2 = np.remainder(encriptacion2, 26)

            for i in range(0, mensaje_largo2 // filas, 1):
                for j2 in range(0, 2, 1):
                    m2 = m2 + diccionario_numeros[encriptacion2[i][j2]]
        elif cif == 2:

            mensaje2 = []

            for i in range(0, len(m)):
                current_letter = m[i:i + 1].lower()
                if current_letter != ' ':  # discard blank characters
                    letter_index = letrasanumeros(current_letter)
                    mensaje2.append(letter_index)

            if len(mensaje2) % filas != 0:
                for i in range(0, len(mensaje2)):
                    mensaje2.append(mensaje2[i])
                    if len(mensaje2) % filas == 0:
                        break

            for i in range(0, int((len(mensaje2) / 2))):
                mensaje2[i] = mensaje2[int((len(mensaje2) / 2)) + i] * 26 + mensaje2[i]

                mensaje2[i] = mensaje2[i] // matpi[i]

            for i in range(0, int((len(mensaje2) / 2))):
                m2 = m2 + diccionario_numeros[mensaje2[i]]

        elif cif == 0:

            mensaje2 = []

            for i in range(0, len(m)):
                current_letter = m[i:i + 1].lower()
                if current_letter != ' ':  # discard blank characters
                    letter_index = letrasanumeros(current_letter)
                    mensaje2.append(letter_index)

            if len(mensaje2) % filas != 0:
                for i in range(0, len(mensaje2)):
                    mensaje2.append(mensaje2[i])
                    if len(mensaje2) % filas == 0:
                        break

            mensaje2 = np.array(mensaje2)
            for i in range(0, len(mensaje2)):
                mensaje2[i] = mensaje2[i] - 3
                if mensaje2[i] < 0:
                    mensaje2[i] = mensaje2[i] + 26
            for i in range(0, len(mensaje2)):
                m2 = m2 + diccionario_numeros[mensaje2[i]]

        if len(m2) % 2 != 0:
            largo = len(m2)
            m3 = list(m2)
            m3[largo - 1] = ""
            m2 = "".join(m3)

        message = f'{USERNAME}: Mensaje Original: {m} \n'
        hamming = f'Hamming: {h} \n'
        hammingcorregido = f'Hamming Corregido: {h_copy2} \n'
        mensajedescifrado = f'{USERNAME}: {m2} \n'
        # CLIENT_SOCKET.send(message.encode())
        # CLIENT_SOCKET.send(hamming.encode())
        # CLIENT_SOCKET.send(hammingcorregido.encode())
        CLIENT_SOCKET.send(mensajedescifrado.encode())


input("Presione enter para comenzar")
os.system('cls')

if 'default' in sys.argv:
    SERVER_IP = 'localhost'
    SERVER_PORT = 12000
else:
    SERVER_IP, SERVER_PORT = set_connection()

print_color(f'\nAbriendo servidor...', 'yellow')

try:
    CLIENT_SOCKET.connect((SERVER_IP, SERVER_PORT))
except OSError as e:
    print(f'\n{e}', 'red')
    exit(-1)

os.system('cls')

USERNAME = input('Nombre de Usuario: ')
USERNAME = format_string(USERNAME, 'random')

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=wait_for_input)
write_thread.start()

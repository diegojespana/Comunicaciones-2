import string
from sympy import Matrix
import numpy as np
import random

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


seleccion = int(input("Desea enviar o leer un mensaje. Ingrese 1 para enviar, 2 para leer: "))

if seleccion == 1:
    mensaje_original = input("Ingrese el mensaje a enviar: ")  # Se pide el mensaje a encriptar
    print("Mensaje Original: ", mensaje_original)

    mensaje = []

    for i in range(0, len(mensaje_original)):  # Se convierten todas las letras a minusculas
        current_letter = mensaje_original[i:i + 1].lower()
        if current_letter != ' ':  # se eliminan los espacios
            letter_index = letrasanumeros(current_letter)  # se convierten las letras a numeros
            mensaje.append(letter_index)

    if len(mensaje) % filas != 0:  # Se almacenan los numeros en un array
        for i in range(0, len(mensaje)):
            mensaje.append(mensaje[i])
            if len(mensaje) % filas == 0:
                break

    mensaje = np.array(mensaje)
    cociente=np.array(mensaje)
    binario = []
    d = ""
    m = ""
    cifrado = 0

    if cifrado == 0:
        print("Cifrado César")
        for i in range(0, len(mensaje)):
            mensaje[i] = mensaje[i] + 3
            if mensaje[i] > 25:
                mensaje[i] = mensaje[i] - 26
        for i in range(0, len(mensaje)):
            m = m + diccionario_numeros[mensaje[i]]
            binario.append(np.binary_repr(mensaje[i]))
        print("El mensaje cifrado es: ", m)
        for i in range(0, len(binario), 1):
            d = d + binario[i]
        print("\n El mensaje en binario es: ", d)
    elif cifrado == 2:
        print("Cifrado Propio")
        for i in range(0, len(mensaje)):
            mensaje[i] = mensaje[i] * matpi[i]
            cociente[i] = mensaje[i] // 26
            mensaje[i] = mensaje[i] % 26

        for i in range(0, len(mensaje)):
            m = m + diccionario_numeros[mensaje[i]]
            binario.append(np.binary_repr(mensaje[i]))
        for i in range(0, len(mensaje)):
            m = m + diccionario_numeros[cociente[i]]
        print("El mensaje cifrado es: ", m)
        for i in range(0, len(binario), 1):
            d = d + binario[i]
        print("\n El mensaje en binario es: ", d)
    elif cifrado == 1:
        print("Cifrado Hill")
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
        print("El mensaje cifrado es: ", m)
        for i in range(0, len(binario), 1):
            d = d + binario[i]

        print("\n El mensaje en binario es: ", d)

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
    print('El Código Hamming generado es: ', end="")
    print(int(''.join(map(str, h))))
elif seleccion == 2:
    print('Ingrese el mensaje recibido en Hamming:')
    d = input()
    data = list(d)
    data.reverse()
    c, ch, j, r, error, h, parity_list, h_copy = 0, 0, 0, 0, 0, [], [], []

    for k in range(0, len(data)):
        p = (2 ** c)
        h.append(int(data[k]))
        h_copy.append(data[k])
        if p == (k + 1):
            c = c + 1

    for parity in range(0, (len(h))):
        ph = (2 ** ch)
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
            parity_list.append(h[parity])
            ch += 1
    parity_list.reverse()
    error = sum(int(parity_list) * (2 ** i) for i, parity_list in enumerate(parity_list[::-1]))

    if error == 0:
        print('No hay ningún error en el Código Hamming enviado.')

    elif error >= len(h_copy):
        print('El error no puede ser detectado')

    else:
        print('El error está en la posición:', error, 'bit')

        if h_copy[error - 1] == '0':
            h_copy[error - 1] = '1'

        elif h_copy[error - 1] == '1':
            h_copy[error - 1] = '0'
            print('El Código Hamming corregido es: ')
        h_copy.reverse()
        print(int(''.join(map(str, h_copy))))

    cif = int(input("Tipo de Cifrado. 0 para Cesar, 1 para Hill y 2 para Propio: "))

    if cif == 1:
        m2 = "Hola Juan Carlos"
        mensaje_original = m2

        mensaje = []

        for i in range(0, len(mensaje_original)):
            current_letter = mensaje_original[i:i + 1].lower()
            if current_letter != ' ':  # discard blank characters
                letter_index = letrasanumeros(current_letter)
                mensaje.append(letter_index)

        if len(mensaje) % filas != 0:
            for i in range(0, len(mensaje)):
                mensaje.append(mensaje[i])
                if len(mensaje) % filas == 0:
                    break

        mensaje = np.array(mensaje)
        mensaje_largo = mensaje.shape[0]
        mensaje.resize(int(mensaje_largo / filas), filas)

        encriptacion = np.matmul(mensaje, llave_inversa)
        encriptacion = np.remainder(encriptacion, 26)

        for i in range(0, mensaje_largo // filas, 1):
            for j2 in range(0, 2, 1):
                print(diccionario_numeros[encriptacion[i][j2]], end=" ")
    elif cif == 2:
        mensaje_original = input("Ingrese el mensaje a desencriptar: ")
        print("Mensaje Original: ", mensaje_original)

        mensaje = []

        for i in range(0, len(mensaje_original)):
            current_letter = mensaje_original[i:i + 1].lower()
            if current_letter != ' ':  # discard blank characters
                letter_index = letrasanumeros(current_letter)
                mensaje.append(letter_index)

        if len(mensaje) % filas != 0:
            for i in range(0, len(mensaje)):
                mensaje.append(mensaje[i])
                if len(mensaje) % filas == 0:
                    break

        for i in range(0, int((len(mensaje)/2))):
            mensaje[i] = mensaje[int((len(mensaje)/2))+i] * 26 +mensaje[i]

            mensaje[i] = mensaje[i] // matpi[i]

        print("El mensaje descifrado es: ")
        for i in range(0, int((len(mensaje)/2))):
            print(diccionario_numeros[mensaje[i]], end="")

    elif cif == 0:
        mensaje_original = input("Ingrese el mensaje a desencriptar: ")
        print("Mensaje Original: ", mensaje_original)

        mensaje = []

        for i in range(0, len(mensaje_original)):
            current_letter = mensaje_original[i:i + 1].lower()
            if current_letter != ' ':  # discard blank characters
                letter_index = letrasanumeros(current_letter)
                mensaje.append(letter_index)

        if len(mensaje) % filas != 0:
            for i in range(0, len(mensaje)):
                mensaje.append(mensaje[i])
                if len(mensaje) % filas == 0:
                    break

        mensaje = np.array(mensaje)
        for i in range(0, len(mensaje)):
            mensaje[i] = mensaje[i] - 3
            if mensaje[i] < 0:
                mensaje[i] = mensaje[i] + 26
        print("El mensaje descifrado es: ")
        for i in range(0, len(mensaje)):
            print(diccionario_numeros[mensaje[i]], end="")

else:
    print('La opción ingresada no existe')
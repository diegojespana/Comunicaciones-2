from socket import *
import threading
import os
import sys
from colors import print_color, format_string
from connection import set_connection

SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)

CLIENTS = list()
ADDRESSES = list()
USERS = list()

SERVER_IP = ''
SERVER_PORT = 0


def print_connections():
    os.system('cls')
    print_color(f'\nListo para recibir {SERVER_IP}:{SERVER_PORT}\n', 'green')
    if len(ADDRESSES) > 0:
        print_color(f'\nConexiones: \n', 'green')
    for address in ADDRESSES:
        print_color(f'\tConectado con {address}', 'cyan')


def broadcast(message, sender=None):
    for client in CLIENTS:
        if client == sender:
            continue
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = CLIENTS.index(client)
            CLIENTS.remove(client)
            client.close()
            user = USERS[index]
            broadcast(format_string(f'{user} ha salido!', color='red').encode())
            USERS.remove(user)
            del ADDRESSES[index]
            print_connections()
            break


def receive():
    while True:
        connection_socket, addr = SERVER_SOCKET.accept()

        connection_socket.send('USER'.encode())
        user = connection_socket.recv(1024).decode()

        USERS.append(user)
        CLIENTS.append(connection_socket)
        ADDRESSES.append(addr)

        print_connections()

        broadcast(f'{user} se unio'.encode(), sender=connection_socket)
        connection_socket.send(format_string(f'Conectado al servidor!', color='green').encode())

        client_thread = threading.Thread(target=handle, args=(connection_socket,))
        client_thread.start()


os.system('cls')
input("Presiona enter para iniciar")
os.system('cls')

if 'default' in sys.argv:
    SERVER_IP = 'localhost'
    SERVER_PORT = 12000
else:
    SERVER_IP, SERVER_PORT = set_connection()

print_color('\nAbriendo servidor...', color='yellow')

try:
    SERVER_SOCKET.bind((SERVER_IP, SERVER_PORT))
except OSError as e:
    print_color(f'\n{e}', color='red')
    exit(-1)

SERVER_SOCKET.listen()

print_color(f'\nListo para recibir desde {SERVER_IP}:{SERVER_PORT}\n', color='green')

receive()

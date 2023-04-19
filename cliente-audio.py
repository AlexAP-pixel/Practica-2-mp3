#!/usr/bin python3

import socket
import time
HOST = "127.0.0.1"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket: # Creamos socket
    TCPClientSocket.connect((HOST, PORT)) # Conectamos
    print("Enviando audio...")
    with open("/Users/alejandro/Desktop/sexto semestre/Redes 2/Practica-2/audio.mp3", "rb") as archivo: # Abrimos el archivo para lectura en formato binario
        while True:

            audio = archivo.read(buffer_size)

            if not audio:
                break

            TCPClientSocket.sendall(audio)

print("El audio se envio")

#!/usr/bin python3

# Selectors la utilizamos para monitorear eventos de entrada y salida en los sockets
# para saber cuando hay datos para leer o escribir
import selectors
import socket
import os

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 1024

sel = selectors.DefaultSelector()
connections = {}

# Se usa cuando un nuevo cliente se conecta al servidor
def accept(sock_a, mask):
    sock_conn, addr = sock_a.accept() # Se acepta la conexion
    sock_conn.setblocking(False)
    sel.register(sock_conn, selectors.EVENT_READ | selectors.EVENT_WRITE, read_write) # Lo registramos en el selector para escuchar eventos de lectura

    # Asigna una ruta de archivo única a una conexión de socket en particular
    connections[sock_conn] = os.path.join(os.getcwd(), f"{addr[0]}_{addr[1]}.mp3")
    """
        os.path.join() = Une varias cadenas de textp
        os.getcwd() = Devuelve la ruta del directorio actual en el que se está ejecutando el programa
        addr[0]}_{addr[1]} = Estas variables contienen la dirección IP y el número de puerto de la conexión de socket, respectivamente. 
                            Estos valores se utilizan para crear un nombre de archivo único para la conexión de socket.
    """

# Se usa cuando se detecta que hay datos disponibles para leer en un socket cliente
def read_write(sock_b, mask):
    if mask & selectors.EVENT_READ:

        data = sock_b.recv(BUFFER_SIZE)

        # Si no hay datos, la conexión se cierra y se elimina del diccionario de conexiones
        if not data:
            sel.unregister(sock_b)
            sock_b.close()
            del connections[sock_b]
            print('Conexión cerrada')

        # Si hay datos, se escriben en un archivo en el directorio actual
        else:
            print("Recibiendo datos")
            # Guarda el archivo mp3 en formato del host
            with open(connections[sock_b], 'ab') as f:
                f.write(data)

    if mask & selectors.EVENT_WRITE:
        print("")


with socket.socket() as socket_accept:
    socket_accept.bind((HOST, PORT))
    socket_accept.listen(100)
    socket_accept.setblocking(False)
    sel.register(socket_accept, selectors.EVENT_READ, accept)  # Lo registramos en el selector

    print(f"Servidor activo")

    while True:
        print("Esperando evento...")
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
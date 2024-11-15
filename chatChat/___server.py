import socket
import threading

# Lista para almacenar los clientes conectados y sus nombres de usuario
clientes = []
nombres_usuarios = {}

# Función para retransmitir mensajes a todos los clientes conectados, excepto al que envió el mensaje
def retransmitir(mensaje, cliente_actual):
    for cliente in clientes:
        if cliente != cliente_actual:  # Evita enviar el mensaje al cliente que lo envió
            try:
                cliente.send(mensaje)
            except:
                # Remueve el cliente de la lista si hay algún error en la conexión
                clientes.remove(cliente)

# Función para manejar cada cliente conectado
def manejar_cliente(cliente):
    try:
        # Solicita al cliente que ingrese su nombre de usuario
        cliente.send("Escribe tu nombre de usuario: ".encode("utf-8"))
        nombre_usuario = cliente.recv(1024).decode("utf-8")
        nombres_usuarios[cliente] = nombre_usuario  # Almacena el nombre de usuario
        bienvenida = f"{nombre_usuario} se ha unido al chat.".encode("utf-8")
        retransmitir(bienvenida, cliente)
        print(f"{nombre_usuario} conectado.")

        # Bucle que recibe y retransmite los mensajes del cliente
        while True:
            mensaje = cliente.recv(1024)
            if mensaje:
                mensaje_con_nombre = f"{nombre_usuario}: {mensaje.decode('utf-8')}".encode("utf-8")
                retransmitir(mensaje_con_nombre, cliente)
    except:
        # Maneja la desconexión del cliente
        if cliente in clientes:
            clientes.remove(cliente)  # Elimina el cliente de la lista de conectados
        if cliente in nombres_usuarios:
            salida = f"{nombres_usuarios[cliente]} ha salido del chat.".encode("utf-8")
            print(salida.decode("utf-8"))
            retransmitir(salida, cliente)
            del nombres_usuarios[cliente]  # Elimina el nombre de usuario de la lista
        cliente.close()  # Cierra la conexión del socket

# Configura y lanza el servidor de chat
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("127.0.0.1", 12345))  # Enlaza el servidor a la dirección y puerto especificados
    servidor.listen(5)  # Escucha hasta 5 conexiones pendientes
    print("Servidor iniciado y esperando conexiones...")

    while True:
        cliente, direccion = servidor.accept()  # Acepta una conexión de cliente
        clientes.append(cliente)  # Añade el cliente a la lista de conectados
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(cliente,))  # Crea un hilo para manejar al cliente
        hilo_cliente.start()  # Inicia el hilo

iniciar_servidor()  # Inicia el servidor

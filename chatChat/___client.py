import socket
import threading
import tkinter as tk
from tkinter import simpledialog

# Clase que define el cliente de chat
class ClienteChat:
    def __init__(self, host, port):
        # Configura el socket y conecta al servidor
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((host, port))
        
        # Solicita el nombre de usuario al cliente mediante una ventana de diálogo
        self.nombre_usuario = simpledialog.askstring("Nombre de Usuario", "Escribe tu nombre de usuario:")
        self.cliente.send(self.nombre_usuario.encode("utf-8"))  # Envía el nombre de usuario al servidor
        
        # Configura la interfaz gráfica utilizando tkinter
        self.root = tk.Tk()
        self.root.title("Cliente de Chat")
        
        # Marco y scrollbar para la lista de mensajes
        self.mensajes_frame = tk.Frame(self.root)
        self.scrollbar = tk.Scrollbar(self.mensajes_frame)
        self.mensajes = tk.Listbox(self.mensajes_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mensajes.pack(side=tk.LEFT, fill=tk.BOTH)
        self.mensajes.pack()
        self.mensajes_frame.pack()
        
        # Campo de entrada para escribir y enviar mensajes
        self.mensaje_var = tk.StringVar()
        self.mensaje_var.set("Escribe aquí tu mensaje...")
        self.campo_entrada = tk.Entry(self.root, textvariable=self.mensaje_var)
        self.campo_entrada.bind("<Return>", self.enviar_mensaje)  # Enviar mensaje al presionar Enter
        self.campo_entrada.pack()
        
        # Configura el cierre de la ventana para finalizar la conexión
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_conexion)
        
        # Inicia un hilo para recibir mensajes de manera asíncrona
        hilo_recibir = threading.Thread(target=self.recibir_mensajes)
        hilo_recibir.start()

    # Método para recibir mensajes del servidor
    def recibir_mensajes(self):
        while True:
            try:
                mensaje = self.cliente.recv(1024).decode("utf-8")  # Recibe el mensaje del servidor
                if mensaje:
                    self.mensajes.insert(tk.END, mensaje)  # Agrega el mensaje a la lista de mensajes
                    self.mensajes.see(tk.END)  # Desplaza automáticamente para ver el último mensaje
                else:
                    break  # Termina el bucle si no se recibe mensaje
            except:
                self.cliente.close()  # Cierra el socket en caso de error
                break

    # Método para enviar mensajes al servidor
    def enviar_mensaje(self, event=None):
        mensaje = self.mensaje_var.get()  # Obtiene el mensaje del campo de entrada
        self.mensaje_var.set("")  # Limpia el campo de entrada
        self.cliente.send(mensaje.encode("utf-8"))  # Envía el mensaje al servidor
        if mensaje == "/salir":
            self.cerrar_conexion()  # Finaliza la conexión si el mensaje es "/salir"

    # Método para cerrar la conexión y salir de la aplicación
    def cerrar_conexion(self, event=None):
        self.cliente.send("/salir".encode("utf-8"))  # Notifica al servidor que se desconecta
        self.cliente.close()  # Cierra el socket
        self.root.quit()  # Cierra la ventana de la interfaz gráfica

    # Método para iniciar la interfaz gráfica de usuario
    def iniciar(self):
        self.root.mainloop()

# Inicia el cliente de chat conectándose al servidor en la dirección y puerto especificados
cliente_chat = ClienteChat("127.0.0.1", 12345)
cliente_chat.iniciar()

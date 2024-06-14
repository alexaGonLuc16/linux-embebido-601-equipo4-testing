import socket
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime

ADDRESS = 'localhost'
PORT = 3333

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor de Registro de Usuarios")
        
        # Configurar estilos
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 14))
        self.style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="#4CAF50", foreground="white")
        self.style.map("Treeview.Heading", background=[('pressed', '!disabled', '#388E3C'), ('active', '#66BB6A')])
        
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Obtener la fecha actual
        current_date = datetime.now().strftime("%d de %B")
        
        self.label_date = ttk.Label(self.frame, text=current_date, anchor="center", font=("Helvetica", 14))
        self.label_date.grid(row=0, column=0, columnspan=3, padx=20, pady=10)
        
        self.label_users = ttk.Label(self.frame, text="Usuarios Registrados", anchor="center", font=("Helvetica", 14))
        self.label_users.grid(row=1, column=0, columnspan=3, padx=20, pady=10)
        
        self.tree = ttk.Treeview(self.frame, columns=("Hora de Acceso", "Usuario", "Estado"), show='headings')
        self.tree.heading("Hora de Acceso", text="Hora")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Estado", text="Estado")
        self.tree.column("Hora de Acceso", anchor="center")
        self.tree.column("Usuario", anchor="center")
        self.tree.column("Estado", anchor="center")
        
        self.tree.grid(row=2, column=0, columnspan=3, padx=20, pady=(0, 10), sticky="nsew")
        
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=3, padx=(0, 20), pady=(0, 10), sticky="ns")
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ADDRESS, PORT))
        self.sock.listen()
        
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Configurar el peso de las filas y columnas para que sean expansibles
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

    def run_server(self):
        while True:
            connection, address = self.sock.accept()
            print(f"Accepted connection from: {address}")
            threading.Thread(target=self.handle_client, args=(connection,)).start()

    def handle_client(self, connection):
        with connection:
            while True:
                received = connection.recv(1024)
                if not received:
                    break
                message = received.decode()
                print(f"Received: {message}")
                self.root.after(0, self.update_tree, message)

    def update_tree(self, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tree.insert('', 'end', values=(current_time, message, "Ingresado"))

    def stop_server(self):
        self.sock.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    
    # Definir la acción a realizar cuando se cierre la ventana
    root.protocol("WM_DELETE_WINDOW", app.stop_server)
    
    root.mainloop()

import socket as sock
import threading
import protocol as prot
from dearpygui import core, simple
import tkinter as tk

class Client:
    def __init__(self):
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.buffer = []
    def connect(self, address, port, nick):
        try:   
            self.sock.connect((address, int(port)))
            
            # send the nickname to the server
            self.sock.send(nick.encode())
        except:
            print("oops")

        recv_t = threading.Thread(target=self.recv)
        recv_t.start()

    def disconnect(self):
        self.sock.close()
        return

    def recv(self):
        while True:
            data = self.sock.recv(512)
            if data != b"!ping":
                recv = data.decode()
                print(recv)
            else:
                continue

    def send(self, receiver, msg):
        protocol = prot.Protocol()
        msg = protocol.build_msg("msg", receiver, msg)
        self.sock.send(msg.encode())

server_names = []
servers = []

def get_servers_from_file():
    lines = open("servers.txt", "r+").readlines()
    
    for line in lines:
        tmp = line.split(",")
        server_names.append(tmp[0])
        servers.append(tmp)

# the main window
class app(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry("600x800")

        # some canvases for structure
        self.chat_canvas = tk.Canvas(self.parent, bg="#ff0000")
        self.connection_canvas = tk.Canvas(self.parent, bg="#00ff00")
        self.list_canvas = tk.Canvas(self.parent, bg="#0000ff")

        self.chat_canvas.place(relwidt=0.7, relheight=1)
        self.connection_canvas.place(relx=0.7, relwidt=0.3, relheight=0.2)
        self.list_canvas.place(relx=0.7, rely=0.2, relwidt=0.3, relheight=0.8)



root = tk.Tk()
app(root).pack(side="top", fill="both", expand=True)
root.mainloop()
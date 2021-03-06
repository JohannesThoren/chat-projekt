# remove the line above if u are on windows

import socket as sock
import threading
import protocol as prot
import tkinter as tk


class Client:
    def __init__(self, app):

        # creating the socket and tell it to use ipv4
        self.sock = None
        self.app = app

    def connect(self, address, port, nick):
        # try to connect to the server
        print(
            f"trying to connect to the server [{address}:{port}] as [{nick}]")
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        try:
            self.sock.connect((address, int(port)))

            # send the nickname to the server
            self.sock.send(nick.encode())
        except:
            print("oops")

        # start the receiverer thread
        recv_t = threading.Thread(target=self.recv)
        recv_t.start()

    # disconnect from server and clean up some stuff
    def disconnect(self):
        self.sock.shutdown(2)
        self.sock.close()

        return

    def recv(self):
        while True:
            # receive data add run it through the protocol parser
            try:
                data = self.sock.recv(512)
                if data != b"!ping" and data != b"":
                    p = prot.Protocol()
                    p.parse(data)
                    if p.type == "usrList":
                        usrList = p.msg.split(",")
                        self.app.user_list.delete(0, tk.END)
                        self.app.user_list.insert(0, *usrList)

                    if p.type == "msg":
                        self.app.chat_box.configure(state="normal")
                        self.app.chat_box.insert(tk.END, p.msg+"\n")
                        self.app.chat_box.configure(state="disabled")

                    
                else:
                    continue
            except:
                break

    def send(self, receiver, msg):
        protocol = prot.Protocol()
        msg = protocol.build_msg_s(msg, "msg", receiver)
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
        self.parent.geometry("900x900")

        # some canvases for structure
        self.chat_canvas = tk.Canvas(self.parent, bg="#ff0000")
        self.connection_canvas = tk.Canvas(self.parent, bg="#00ff00")
        self.list_canvas = tk.Canvas(self.parent, bg="#0000ff")

        self.chat_canvas.place(relwidt=0.7, relheight=1)
        self.connection_canvas.place(relx=0.7, relwidt=0.3, relheight=0.2)
        self.list_canvas.place(relx=0.7, rely=0.2, relwidt=0.3, relheight=0.8)

        #small workaround
        self.ip = tk.Canvas(self.connection_canvas)
        self.port = tk.Canvas(self.connection_canvas)
        self.nick = tk.Canvas(self.connection_canvas)

        self.ip.pack(fill=tk.X)
        self.port.pack(fill=tk.X)
        self.nick.pack(fill=tk.X)

        # server connect menu
        self.ip_entry = tk.Entry(self.ip, text="server ip address")
        self.port_entry = tk.Entry(self.port, text="server port")
        self.nick_entry = tk.Entry(self.nick, text="nickname")

        self.ip_lbl = tk.Label(self.ip, text="Ip address",)
        self.port_lbl = tk.Label(self.port, text="server port")
        self.nick_lbl = tk.Label(self.nick, text="nickname")

        self.connect_btn = tk.Button(self.connection_canvas, text="Connect")
        self.disconnect_btn = tk.Button(self.connection_canvas, text="disconnect")

        self.status_lbl = tk.Label(self.connection_canvas, text="not connected!",font=44)

        self.ip_lbl.pack(fill=tk.X, side="left")
        self.port_lbl.pack(fill=tk.X, side="left")
        self.nick_lbl.pack(fill=tk.X, side="left")

        self.ip_entry.pack(side="right")
        self.port_entry.pack(side="right")
        self.nick_entry.pack(side="right")
        self.connect_btn.pack(fill=tk.X)
        self.disconnect_btn.pack(fill=tk.X)
        self.status_lbl.pack(fill=tk.BOTH, expand=1)

        # connected users
        self.user_list = tk.Listbox(self.list_canvas)
        self.user_list.pack(fill=tk.BOTH, expand=1)

        # chat area
        self.chat_box = tk.Text(self.chat_canvas, font=24)
        self.chat_input = tk.Entry(self.chat_canvas, font=24)
        self.send_btn = tk.Button(self.chat_canvas, text="send")

        self.chat_box.pack(fill=tk.BOTH, expand=1)
        self.chat_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.send_btn.pack(side=tk.RIGHT)


def connect(app, client):
    try:
        client.connect(app.ip_entry.get(), app.port_entry.get(), app.nick_entry.get())
        app.chat_box.delete("1.0", "end")
        app.user_list.delete(0, tk.END)
        app.status_lbl.config(text=f"connected to {app.ip_entry.get()}")
    except:
        app.status_lbl.config(text="could not connect to the server!")


def disconnect(app, client):
    client.disconnect()
    app.chat_box.configure(state="normal")
    app.chat_box.delete("1.0", "end")
    app.user_list.delete(0, tk.END)
    app.status_lbl.config(text="not connected")
    app.chat_box.configure(state="disabled")

root = tk.Tk()
app = app(root)
c = Client(app)


def send(*args):
    # try:
    c.send("all", app.chat_input.get())
    app.chat_input.delete(0, tk.END)
    # except:
    # app.chat_box.insert(tk.END, "you must be connected to a server to be able to send anyting!")


app.connect_btn.config(command=lambda: connect(app, c))
app.disconnect_btn.config(command=lambda: disconnect(app, c))

app.send_btn.config(command=send)

root.bind("<Return>", send)

root.mainloop()

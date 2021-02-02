import socket as sock
import threading
import protocol as prot
from dearpygui import core, simple


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
                core.configure_item("##chat_box", items=self.buffer)
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




get_servers_from_file()

# TODO make size of widgets dynamic!!

# dear imgui stuff
core.set_main_window_size(800, 776)

with simple.window("add_server", height=200, width=200, show=False):
    core.add_input_text("ip", width=120)
    core.add_input_text("port", width=120)
    core.add_input_text("nickname", width=120)

with simple.window("win", width=700, height=800):
    # serverlist widgets 
    core.add_combo("##server_list", width=280, items=server_names)
    core.add_same_line()
    core.add_button("add server", width=102)
    core.add_same_line()
    core.add_button("delete server", width=102)

    #connection widgets
    core.add_button("connect", width=246)
    core.add_same_line()
    core.add_button("disconnect", width=246)
    core.add_separator()

    # chat widgets
    core.add_listbox("##chat_box", width=500, num_items=40)
    core.add_same_line()
    core.add_listbox("##connected", width=276, num_items=40)
    core.add_input_text("##chat_input", width=442)
    core.add_same_line()
    core.add_button("send", width=50)

client = Client()
client.connect("localhost", "3000", "hej")

core.set_primary_window("win", True)
core.start_dearpygui()


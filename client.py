import socket as sock
import threading
import protocol as prot
from dearpygui import core, simple

class Client: 
    def __init__(self):
        self.sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def connect(self, address, port, nick): 
        try:
            self.sock.connect((address, int(port)))
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
                print("poof")
            else:
                continue

    def send(self, receiver, msg):
        protocol = prot.Protocol()
        msg = protocol.build_msg("msg", receiver, msg)
        self.sock.send(msg.encode())


# dear imgui stuff

core.set_main_window_size(1015, 800)
core.set_global_font_scale(1,5)

with simple.window("chat", width=700, height=800):
    print("chat window initialized")
    simple.set_window_pos("chat", 0, 0)


with simple.window("connection", width=300, height=300):
    print("connection window initialized")
    simple.set_window_pos("connection", 700, 0)
    core.add_input_text("ip")
    core.add_input_text("port")
    core.add_input_text("nick")

    core.add_button("connect")

with simple.window("list", width=300, height=500):
    print("list window initialized")
    simple.set_window_pos("list", 700, 300)

core.start_dearpygui()

client = Client()
client.connect("localhost", "3000", "johannes")


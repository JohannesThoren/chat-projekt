import socket
import threading
from time import sleep
import protocol
PORT = 3001
HOST = "0.0.0.0"

# the class that will take care of the clients and make stuff easier for me
class Client:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.nick = None

    # just a thing to set the nick name
    def set_nick(self, nick):
        self.nick = nick


# help for later
class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    # sets all variables that is needed for the sockets
    def init(self):
        self.sock.bind((HOST, PORT))

        while True:
            try:
                print(f"===[now listening for connections on port {PORT}!]===")

                # listen for connections and connect them if the server is not full
                self.sock.listen()
                conn, addr = self.sock.accept()
                print(f"[{addr}]\tjust connected to the server!")
                client = Client(conn, addr)

                # set the clients nick name
                # this will be auto sent from the client when it tries to connect
                nick = client.conn.recv(512).decode()
                client.set_nick(nick)
                print(f"[{client.addr}]\tnick name set to {client.nick}!")

                # append the client to the clients list
                self.clients.append(client)
                print(f"[{client.addr}]\tclient added to clients list!")

                # start a thread for receiving data from the clients
                recv_thread = threading.Thread(
                    target=self.recv_func, args=(client,)).start()

            except:
                # if error clos all connections and exit
                for client in self.clients:
                    client.conn.close()

                self.sock.close()
                print("an error occurred!")

                exit()
                break

    # this is the function that will recv data from all connected clients.
    # this will be started in different threads.
    # 1 for each connected client.

    def recv_func(self, client):
        print(f"[{client.addr}]\trecv thread started for client!")


        while True:

            try:
                # this pings the client for each iteration and checks if it is still connected
                client.conn.send(b"!ping")
                data = client.conn.recv(512)

            except:
                # id client is disconnected then close connection and remove client from the list
                client.conn.close()
                self.clients.remove(client)
                print(f"[{client.addr}]\tclient disconnected from the server!")
                break

            if data != b"!ping" and data != b"":
                try:
                    parsed = protocol.Protocol(data)
                    print(parsed.type)
                except:
                    print("something went wrong trying to parse the data!")


                if parsed.type == "msg":
                    for client_recv in self.clients:
                        print(client_recv.nick)
                        if client_recv.nick == parsed.receiver:
                            print("yeee")
     
            else:
                continue

serv = Server()
serv.init()

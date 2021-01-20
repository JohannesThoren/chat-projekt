import socket
import threading
from time import sleep


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
# data will be received like this "type|from|receiver|data"

# types     :   command, msg, etc
# from      :   either the sender or the server
# receiver  :   either the server or another connected client,
# data      :   either the msg or the command


# TODO force the user to set a nickname in some way
class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    # sets all variables that is needed for the sockets
    def init(self):
        self.sock.bind((HOST, PORT))

        while True:
            try:
                print(f"now listening for connections on port {PORT}!")

                # listen for connections and connect them if the server is not full
                self.sock.listen()
                conn, addr = self.sock.accept()
                print("------------------")
                print(f"[{addr}]\tjust connected to the server!")
                client = Client(conn, addr)
                
                # set the clients nick name
                # this will be auto sent from the client when the try to connect
                nick = client.conn.recv(512).decode()
                client.set_nick(nick)
                print(f"[{client.addr}]\tnick name set to {client.nick}!")

                self.update_lists(nick,"add")
                self.send_list(conn)

                # append the client to the clients list
                self.clients.append(client)
                print(f"[{client.addr}]\tclient added to clients list!")

                # start a thread for receiving data from the clients
                recv_thread = threading.Thread(target=self.recv_func, args=(client,)).start()


            except:
                # if error clos all connections and exit
                for client in self.clients:
                    client.conn.close()

                self.sock.close()
                print("an error occurred!")

                exit()
                break

    def send_list(self, conn):
        for client in self.clients:
            conn.send(f"ulist|add|{client.nick}".encode("UTF-8"))
            sleep(0.05)
    #update the conn_list for each client
    def update_lists(self, nick, method):
        for client in self.clients:
            client.conn.send(f"ulist|{method}|{nick}".encode("UTF-8")) 

    # this is the function that will recv data from all connected clients.
    # this will be started in different threads.
    # 1 for each connected client.
    def recv_func(self, client):
        print(f"[{client.addr}]\trecv thread started for client!")
        print("------------------\n")

        while True:

            # this is pings the client for each iteration and checks if it is still connected
            # if not clos the connection and remove the client form the clients list
            try:
                client.conn.send(b"!ping")
                data = client.conn.recv(512)

                
            except:
                client.conn.close()
                self.clients.remove(client)
                self.update_lists(client.nick, "del")
                print(f"[{client.addr}]\tclient disconnected from the server!")
                break

            
            
            if data != b"!ping":
                

            else:
                continue



serv = Server()
serv.init()
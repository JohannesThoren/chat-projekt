import socket
import threading

PORT = 3300
HOST = "0.0.0.0"
CONNECTIONS = 10

# the class that will take care of the
# clients.


class Client:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.nick = None

    # send data to this client
    def send(self):
        return

    # just a thing to set the nick name
    def set_nick(self, nick):
        self.nick = nick


# help for later
# data will be received like this "type|receiver|data"

# types     :   command, msg, etc
# receiver  :   either the server or another connected client,
# data      :   either the msg or the command

class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = []

    # sets all variables that is needed for the sockets
    def init(self):
        self.sock.bind((HOST, PORT))

        while True:
            try:

                # listen for connections and connect them if the server is not full
                self.sock.listen(CONNECTIONS)
                conn, addr = self.sock.accept()

                print(f"{addr} just connected to the server")
                client = Client(conn, addr)

                # append the client to the clients list

                self.clients.append(client)
                print(f"client {addr} added to clients list")

                conn.send(b"you are now connected to the server!\n")

                # start a thread for receiving data from the clients
                threading.Thread(target=self.recv_func(conn))
                

            except:
                for client in self.clients:
                     client.conn.close()

                self.sock.close()
                print("an error occurred!")
                break
                
        # if loop stops then close the server socket
        self.sock.close()

    # this is the function that will recv data from all connected clients.
    # this will be started in different threads.
    # 1 for each connected client.
    def recv_func(self, conn):
        print(f"recv thread started for client")

        while True: 
            data = conn.recv()
            self.process(data)


    # this will process the data received and parse it according to the above text
    def process(self, data):
        print(data)
        return


serv = Server()
serv.init()

import socket
import tkinter as tk
import threading
import process_data


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = None
        self.nick = None
        self.root = None
        self.conn_list = None

    def init_client(self, host, port, nick, root, conn_list):
        self.host = host
        self.port = port
        self.nick = nick
        self.root = root
        self.conn_list = conn_list
      

        self.start_client()

    def disconnect(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.root.title("Chat")
        except:
            print("you'r not connected to any server!")

    def connected_clients(self):
        return 0

    def start_client(self):
        # connect the client to the server
        self.sock.connect((self.host, int(self.port)))
        self.sock.send(self.nick.encode())

        # start a thread for receiving and sending data

        threading.Thread(target=self.recv_func).start()
        print("recv thread started!")

        self.root.title(f"{self.nick} [{self.host} : {self.port}]")

    def recv_func(self):
        while True:
            # check if your still connected else close the socket
            try:
                data = self.sock.recv(512)
                process_data.process_received(data, self)
            except:
                self.disconnect()
                break

    def send_func(self, data, receiver):
        data_process = process_data.ProcessData()
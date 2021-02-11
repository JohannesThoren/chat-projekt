#!/bin/python3

import socket
import threading
from time import sleep
import protocol
import datetime


PORT = 3000

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
        self.client_name_list = ""

    # sets all variables that is needed for the sockets
    def init(self):
        self.sock.bind((HOST, PORT))

        while True:
        #try:
            print(f"===[now listening for connections on port {PORT}!]===")

            # listen for connections and connect them if the server is not full
            self.sock.listen()
            conn, addr = self.sock.accept()
            print(f"[{addr}]\tjust connected to the server!")
            client = Client(conn, addr)

            # set the clients nick name
            # this will be auto sent from the client when it tries to connect
            nick = client.conn.recv(512).decode().rstrip()

            client.set_nick(nick)

            print(f"[{client.addr}]\tnick name set to {client.nick}!")

            # append the client to the clients list
            self.clients.append(client)
            print(f"[{client.addr}]\tclient added to clients list!")

            # update connected list
            try:
                self.update_name_list()
                sleep(0.05)
            except:
                continue
            
            p = protocol.Protocol()
            conn.send(protocol.Protocol().build_msg("you are now connected to the server!", "msg", "server", "client").encode())

            # start a thread for receiving data from the clients
            recv_thread = threading.Thread(
                target=self.recv_func, args=(client,)).start()

        #except:
            # if error clos all connections and exit
            # for client in self.clients:
            #     self.user_disconnect(client)
            # self.sock.close()
            # print("an error occurred!")

            # exit()
            # break

    # this is the function that will recv data from all connected clients.
    # this will be started in different threads.
    # 1 for each connected client.

    def recv_func(self, client):
        print(f"[{client.addr}]\trecv thread started for client!")

        while True:

            try:
                # this pings the client for each iteration of and checks if it is still connected
                # the sleep to make sure that it will be sent and not interfere with other stuff
                client.conn.send(b"!ping")
                sleep(0.5)

                data = client.conn.recv(512)

            except:
                # if client is disconnected then close connection and remove client from the list
                self.user_disconnect(client)

                break

            if data != b"":

                p = protocol.Protocol()
                p.parse(data)
                p.respond_clients(self.clients, client.nick)

            else:
                continue

    def update_name_list(self):
        self.client_name_list = "usrList|all|"

        for client in self.clients:
            self.client_name_list = self.client_name_list+client.nick+","

        for client in self.clients:
            client.conn.send(self.client_name_list.encode())

    def user_disconnect(self, client):
        self.clients.remove(client)
        client.conn.close()
        print(f"[{client.addr}]\tclient disconnected from the server!")

        self.update_name_list()


serv = Server()
serv.init()

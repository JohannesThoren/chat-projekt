import client
import tkinter as tk

def process_to_send(data_type, sender, receiver, msg):
    data = str(f"{data_type}|{sender}|{receiver}|{msg}").encode("UTF-8")
    return data

def process_received(data,  client):

    data = data.decode().split("|")
    print(data)

    if data[0] == "msg":
        print("yee")

    if data[0] == "ulist":
        if data[1] == "add":
            client.conn_list.insert(tk.END, data[2])
        elif data[1] == "del":
            idx = client.conn_list.get(0, tk.END).index(data[2])
            client.conn_list.delete(idx)
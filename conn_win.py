import tkinter as tk
import client


def connection_win(client, root, conn_list):
    conn_win = tk.Toplevel()
    conn_win.geometry("200x100")

    host_in = tk.Entry(conn_win)
    host_in.insert(0, "host address")
    host_in.pack()

    port_in = tk.Entry(conn_win)
    port_in.insert(0, "host port")
    port_in.pack()

    nick_in = tk.Entry(conn_win)
    nick_in.insert(0, "nickname")
    nick_in.pack()

    connect_btn = tk.Button(conn_win, text="connect", command=lambda: client.init_client(
        host_in.get(), port_in.get(), nick_in.get(), root, conn_list))
    connect_btn.pack()


import tkinter as tk
import socket as sock
import threading

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

root = tk.Tk()
root.geometry("800x800")

canvas = tk.Canvas(root)
canvas.place(relwidth=1, relheight=1)

chat_text = tk.Listbox(canvas)

def connect(address, port, nick): 
    try:
        s.connect((address, int(port)))
        s.send(nick.encode())
    except:
        print("oops")

    recv_t = threading.Thread(target=recv)
    recv_t.start()

def disconnect():
    s.close()
    return

def recv():
    while True:
        data = s.recv(512)
        if data != b"!ping":
            chat_text.insert(tk.END, data.decode())
        else:
            continue


chat_text = tk.Listbox(canvas)
chat_text.place(relwidth=0.7, relheight=0.95)

chat_scroll = tk.Scrollbar(chat_text)
chat_scroll.pack(side="right", fill="y")

chat_text.configure(yscrollcommand=chat_scroll.set)

chat_input = tk.Entry(canvas)
chat_input.place(rely=0.96, relwidth=0.6, relheight=0.03)

chat_send = tk.Button(canvas, text="Send", command=lambda: s.send(f"msg|{chat_input.get()}".encode()))
chat_send.place(relx=0.6, rely=0.96, relwidth=0.1, relheight=0.03)

address = tk.Entry(canvas)
address.insert(0, "host address")
address.place(relx=0.7, rely=0.00, relwidth=0.20)

port = tk.Entry(canvas)
port.insert(0, "port")
port.place(relx=0.9, rely=0.00, relwidth=0.10)

nickname = tk.Entry(canvas)
nickname.insert(0, "nickname")
nickname.place(relx=0.7, rely=0.03, relwidth=0.30)

connect_btn = tk.Button(canvas, text="connect", command=lambda: connect(address.get(), port.get(), nickname.get()))
connect_btn.place(relx=0.7, rely=0.06, relwidth=0.15)

disconnect_btn = tk.Button(canvas, text="disconnect", command=lambda: disconnect())
disconnect_btn.place(relx=0.85, rely=0.06, relwidth=0.15)

root.mainloop()

import tkinter as tk
import client

def chat_win(client, receiver):
    chat_win = tk.Toplevel()
    chat_win.geometry("350x500")

    chat_lbl = tk.Label(chat_win, text="chating to :")
    chat_lbl.pack()

    chat_text = tk.Listbox(chat_win)
    chat_text.place(relwidth=1, relx=0, rely=0.05, relheight=0.9)

    chat_entry = tk.Entry(chat_win)
    chat_entry.place(relwidth=0.8, relx=0, rely=0.95, relheight=0.05)

    chat_send = tk.Button(chat_win, text="send", command=lambda: client.send(data, receiver))
    chat_send.place(relwidth=0.2, relx=0.8, rely=0.95, relheight=0.05)

    print(receiver)

    return (chat_text, chat_entry, chat_lbl, chat_win)
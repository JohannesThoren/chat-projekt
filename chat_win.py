import tkinter as tk
import client as c


def chat_win(client, receiver):
    chat_win = tk.Toplevel()
    chat_win.geometry("350x500")

    chat_lbl = tk.Label(chat_win, text=f"chating to : {receiver}")
    chat_lbl.pack()

    chat_text = tk.Listbox(chat_win)
    chat_text.place(relwidth=1, relx=0, rely=0.05, relheight=0.9)

    chat_entry = tk.Entry(chat_win)
    chat_entry.place(relwidth=0.8, relx=0, rely=0.95, relheight=0.05)

    chat_send = tk.Button(chat_win, text="send", command=lambda: client.send_func(chat_entry.get(), receiver))
    chat_send.place(relwidth=0.2, relx=0.8, rely=0.95, relheight=0.05)

    client.chat.append(c.Chat(chat_text, receiver))
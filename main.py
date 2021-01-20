import tkinter as tk
import chat_win
import client
import conn_win

WIDTH = 350
HEIGHT = 500


# create a client object
client = client.Client()




# creating a tk instance
root = tk.Tk()
root.title("Chat")

# the main canvas
canvas = tk.Canvas(root)
canvas.place(relwidth=1, relheight=1)

# the list frame will contain the connection button and all connected clients
list_frame = tk.Frame(canvas, bd=2, relief="groove")
list_frame.place(relwidth=1, relx=0, rely=0, relheight=1)

conn_list = tk.Listbox(list_frame)
conn_list.place(relwidth=1, relx=0, rely=0.05, relheight=0.90)

# button to open connection window
connect_btn = tk.Button(
    list_frame, text="connect to server", command=lambda: conn_win.connection_win(client, root, conn_list))
connect_btn.place(relwidth=0.5, relx=0, rely=0, relheight=0.05)

# disconnect button
disconnect_btn = tk.Button(
    list_frame, text="disconnect", command=lambda: client.disconnect())
disconnect_btn.place(relwidth=0.5, relx=0.5, rely=0, relheight=0.05)

# open chat window button
open_chat_btn = tk.Button(list_frame, text="open chat", command=lambda: chat_win.chat_win(client, conn_list.get()))
open_chat_btn.place(relwidth=1, relx=0, rely=0.95, relheight=0.05)

root.config(width=WIDTH, height=HEIGHT)
root.mainloop()

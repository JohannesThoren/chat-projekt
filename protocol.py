# how the data protocol will look
# type      = command, data, msg
# receiver  = well receiver of the data
# data      = the data sent

# type|recv|msg

import datetime
import time

class Protocol():
    def __init__(self):
        self.data = None
        self.type = None
        self.receiver = None
        self.msg = None

    def parse(self, data):
        self.data = data.decode().split('|')
        self.type = self.data[0].rstrip()
        self.receiver = self.data[1].rstrip()
        self.msg = self.data[2].rstrip()




    def respond_clients(self, clients, sender):
        if self.type == "msg" and self.receiver == "all":
            for client in clients:
                client.conn.send(self.build_msg(self.msg, self.type, sender, self.receiver).encode())
            time.sleep(0.5)

    #yes this is a bodge dont judge!!!
    def build_msg_s(self, msg, msg_type, receiver):
 
        return f"{msg_type}|{receiver}|{msg}"
        
    def build_msg(self, msg, msg_type, sender, receiver):
        now = datetime.datetime.now()
        now = now.strftime("%H:%M:%S")

        return f"{msg_type}|{receiver}|[{now}] [{sender}] : {msg}"
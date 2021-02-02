# how the data protocol will look
# type      = command, data, msg
# receiver  = well receiver of the data
# data      = the data sent

# type|recv|msg

class Protocol():
    def __init__(self, data):
        self.data = data
        self.type = None
        self.receiver = None
        self.msg = None

    def parse(self):
        self.data = self.data.decode().split('|')
        self.type = self.data[0].rstrip()
        self.receiver = self.data[1].rstrip()
        self.msg = self.data[2].rstrip()

        print(f"{self.data}\t{self.type}\t{self.receiver}\t{self.msg}")


    def build_msg(self, msg_type, receiver, data):
        return f"{msg_type}|{receiver}|{self.data}"
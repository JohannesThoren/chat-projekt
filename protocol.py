# how the data protocol will look
# type      = command, data, msg
# receiver  = well receiver of the data
# data      = the data sent

# type|msg

class Protocol():
    def __init__(self):
        self.data = None
        self.type = None
        self.receiver = None
        self.msg = None

    def parss_data(self, data):
        self.data = data.decode().split('|')
        self.type = self.data[0].rstrip()
        self.receiver = self.data[1].rstrip()
        self.msg = self.data[2].rstrip()


    def build_msg(self, type, receiver, data):
        return f"msg|{receiver}|{self.data}"
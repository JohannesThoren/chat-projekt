# how the data protocol will look
# type      = command, data, msg
# receiver  = well receiver of the data
# data      = the data sent

# type|receiver|data/msg

class Protocol():
    def __init__(self, data):
        self.data = data.decode().split('|')
        self.type = self.data[0]
        self.receiver = self.data[1]
        self.msg = self.data[2]


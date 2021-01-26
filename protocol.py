# how the data protocol will look
# type      = command, data, msg
# receiver  = well receiver of the data
# data      = the data sent

# type|msg

class Protocol():
    def __init__(self, data):
        self.data = data.decode().split('|')
        self.type = self.data[0].rstrip()
        self.msg = self.data[1].rstrip()


import socket
import sys

class Robot():
    def __init__(self, dir):
        self.dir = dir
        self.start()

    def start(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.dir == "right": # ErnestTubb
            serversocket.bind(('10.214.159.125', 8089))
        elif self.dir == "left": # LorrettaLynn
            serversocket.bind(("10.214.159.122", 8089))
        serversocket.listen(5) # become a server socket, maximum 5 connections

        while True:
            connection, address = serversocket.accept()
            buf = connection.recv(64).decode()
            if(len(buf) > 0):
                self.execute_action(buf)
            connection.close()

    def execute_action(self, gesture):
        if(gesture == "front"):
            self.react_front()
        elif(gesture == "back"):
            self.react_back()
        elif(gesture == "fist"):
            self.react_fist()
        elif(gesture == "gun"):
            self.react_gun()
        else:
            print("Unrecognized gesture!")

    def react_front(self):
        print(f"Called react_front: side={self.dir}")

    def react_back(self):
        print(f"Called react_back: side={self.dir}")

    def react_fist(self):
        print(f"Called react_fist: side={self.dir}")

    def react_gun(self):
        print(f"Called react_fist: side={self.dir}")

if(__name__ == "__main__"):
    try:
        robot = Robot(sys.argv[1])
    except IndexError:
        print(f"Usage: {sys.argv[0]} left/right")
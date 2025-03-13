import socket

class Robot():
    def __init__(self):
        self.start()

    def start(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('10.214.159.125', 8089))
        serversocket.listen(5) # become a server socket, maximum 5 connections

        while True:
            connection, address = serversocket.accept()
            buf = connection.recv(64).decode()
            if(len(buf) > 0):
                self.execute_action(buf)

    def execute_action(self, gesture):
        gesture, side = gesture.split("_")
        if(gesture == "front"):
            self.react_front(side)
        elif(gesture == "back"):
            self.react_back(side)
        elif(gesture == "fist"):
            self.react_fist(side)
        elif(gesture == "gun"):
            self.react_gun(side)
        else:
            print("Unrecognized gesture!")

    def react_front(self, side):
        print(f"Called react_front: side={side}")

    def react_back(self, side):
        print(f"Called react_back: side={side}")

    def react_fist(self, side):
        print(f"Called react_fist: side={side}")

    def react_gun(self, side):
        print(f"Called react_fist: side={side}")

if(__name__ == "__main__"):
    robot = Robot()
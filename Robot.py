import socket
import sys
import time

sys.path.append('/home/pi/ArmPi/HiwonderSDK/')

import ActionGroupControl as AGC

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
        serversocket.listen(5) # become a server socket, maximum 5 connection

        data = ""
        while True:
            connection, address = serversocket.accept()
            data += connection.recv().decode()
            if(len(data) > 0):
                if('~' not in data):
                    continue
                length, message = data.split('~')
                if(int(length) == len(message)):
                    self.execute_action(message)
                    data = ""
            connection.close()

    def execute_action(self, gesture):
        # Wait to stop current action
        while(AGC.runningAction):
            print(f"Waiting to cancel gesture to begin running {gesture} gesture")
            AGC.stopRunning = True
            time.sleep(0.01)
        # Call specific action to run
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
        AGC.runAction("hand turn "+ self.dir)
        print(f"Called react_front: side={self.dir}")

    def react_back(self):
        AGC.runAction(f"hand turn {self.dir}")
        print(f"Called react_back: side={self.dir}")

    def react_fist(self):
        AGC.runAction(f"circle")
        print(f"Called react_fist: side={self.dir}")

    def react_gun(self):
        AGC.runAction("dead")
        print(f"Called react_fist: side={self.dir}")

if(__name__ == "__main__"):
    try:
        robot = Robot(sys.argv[1])
    except IndexError:
        print(f"Usage: {sys.argv[0]} left/right")
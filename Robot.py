import socket
import sys
import time
import json

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

        while True:
            connection, address = serversocket.accept()
            # get the data from the connection
            buffer_clear = False
            data = ""
            # loop through all buffer values until there are none to read from
            while(not buffer_clear):
                recent_message = connection.recv(64).decode()
                if(len(recent_message) > 0):
                    print(f"Updating data from! Prev data: {data}")
                    data = recent_message
                else:
                    print("Buffer is clear!")
                    buffer_clear = True
                print(f"Sending data: {data}")
            # execute action is data is a gesture
            if(len(data) > 0):
                self.execute_action(data)
            # close the connection
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
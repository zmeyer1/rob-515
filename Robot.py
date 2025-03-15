import socket
import sys
import time
import json
import threading

sys.path.append('/home/pi/ArmPi/HiwonderSDK/')

import ActionGroupControl as AGC

class Robot():
    def __init__(self, dir):
        self.dir = dir
        self.latest_gesture = ""
        self.current_gesture = ""
        self.start()

    def start(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.dir == "right": # ErnestTubb
            serversocket.bind(('10.214.159.125', 8089))
        elif self.dir == "left": # LorrettaLynn
            serversocket.bind(("10.214.159.122", 8089))
        serversocket.listen(5) # become a server socket, maximum 5 connection

        t1 = threading.Thread(target=self.read_gesture, args=(serversocket,))
        t2 = threading.Thread(target=self.execute_latest_gesture, args=())

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    
    def read_gesture(self, serversocket):
        while True:
            connection, address = serversocket.accept()
            data = connection.recv(64).decode()
            data = data.strip('"')
            # save the gesture if it is larger than 0
            if(len(data) > 0):
                self.latest_gesture = data
                print(f"New Gesture: {self.latest_gesture}")
            # close the connection
            connection.close()
            if data == "die":
                print(f"Alas, I die")
                break


    def execute_latest_gesture(self):
        while(True):
            if(self.latest_gesture != self.current_gesture):
                # Wait to stop current action
                while(AGC.runningAction):
                    print(f"Waiting to cancel gesture to begin running {self.current_gesture} gesture")
                    AGC.stopRunning = True
                    time.sleep(0.01)
                self.current_gesture = self.latest_gesture
                self.execute_action(self.latest_gesture)
            else:
                self.execute_action(self.latest_gesture)
            time.sleep(0.01)
            if self.latest_gesture == 'gun':
                break

    def execute_action(self, gesture):
        # Call specific action to run
        if(gesture == "front"):
            self.react_front()
        elif(gesture == "back"):
            self.react_back()
        elif(gesture == "fist"):
            self.react_fist()
        elif(gesture == "gun"):
            self.react_gun()
        elif(gesture == "None"):
            self.react_straight()
        else:
            print(f"Unrecognized gesture! {gesture}")

    def react_straight(self):
        AGC.runAction("hand up")
        print(f"Called None")

    def react_front(self):
        # AGC.runAction(f"hand turn {self.dir}")
        print(f"hand front {self.dir}")
        AGC.runAction(f"hand front {self.dir}")
        print(f"Called react_front: side={self.dir}")

    def react_back(self):
        # AGC.runAction(f"hand turn {self.dir}")
        print(f"hand back {self.dir}")
        AGC.runAction(f"hand back {self.dir}")
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
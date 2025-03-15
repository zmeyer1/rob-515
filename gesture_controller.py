import socket, cv2, time
import numpy as np
from classify_hand import HandClassifier
import json


class DefaultDict(dict):

    def __init__(self, default = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = default
    
    def __getitem__(self, key):
        try:
            super().__getitem__(key)
        except KeyError:
            return self.default

PERSISTENCE =  DefaultDict(0.2)
PERSISTENCE["gun"] == 1

if __name__ == "__main__":
    print("first print")
    cap = cv2.VideoCapture(0)

    classifier = HandClassifier("hand_signs.pickle")
    start = [None, None]
    old_label = [None, None]
    last_sent = [None, None]

    ips = ('10.214.159.122', '10.214.159.125')

    while cap.isOpened():
        ret, frame = cap.read()
        labels, dists = classifier.classify(frame, display=True)

        for i, label in enumerate(labels):
            if (label == "None" or dists[i] < 10) and label == old_label[i]:
                if not start[i]:
                    start[i] = time.time()
                elif time.time() - start[i] > PERSISTENCE[label]:
                    # we've held the same gesture on the same hand for PERSISTENCE seconds
                    # only send a consecutive label once
                    if label != last_sent[i]:
                        try:
                            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            clientsocket.connect((ips[i], 8089))
                            clientsocket.send(label.encode())
                            clientsocket.close()
                        except OSError as e:
                            print(f"Failed to send reach robot: {e}")
                        start[i] = None
                    last_sent[i] = label

            old_label[i] = label

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"{labels[0]} ({np.round(dists[0],2)})", (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"{labels[1]} ({np.round(dists[1],2)})", (frame.shape[0] - 50, 50), font, 1, (50, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('window', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Press 'q' to quit
            break

    for ip in ips:
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect((ips, 8089))
            clientsocket.send("die".encode())
            clientsocket.close()
        except OSError as e:
            print(f"Failed to send reach robot: {e}")
    cap.release()
    cv2.destroyAllWindows()
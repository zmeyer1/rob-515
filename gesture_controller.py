import socket, cv2, time
import numpy as np
from classify_hand import HandClassifier

PERSISTENCE = 0.5

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    classifier = HandClassifier("hand_signs.pickle")
    start = (None, None)
    old_label = (None, None)
    last_sent = (None, None)

    ips = ('10.214.159.125', '10.214.159.122')
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while cap.isOpened():
        ret, frame = cap.read()

        labels, dists = classifier.classify(frame, display=True)

        for i, label in enumerate(labels):
            if dists[i] < 10 and label == old_label[i]:
                if not start[i]:
                    start[i] = time.time()
                elif time.time() - start[i] > PERSISTENCE:
                    # we've held the same gesture on the same hand for PERSISTENCE seconds
                    # only send a consecutive label once
                    if label != last_sent[i]:
                        clientsocket.connect((ips[i], 8089))
                        clientsocket.send(label.encode())
                        clientsocket.close()
                        start = None
                    last_sent[i] = label

            old_label[i] = label

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"{label} ({np.round(np.mean(dists),2)})", (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('window', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()
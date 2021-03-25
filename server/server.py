from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
ap.add_argument("-mw", "--montage_w", required=True, type=int, help="montage frame width")
ap.add_argument("-mh", "--montage_h", required=True, type=int, help="montage frame height")
args = vars(ap.parse_args())

imageHub = imagezmq.ImageHub()
# MobileNet SSD class labels
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

CONSIDER = {"dog", "person", "car"}  # class labels
obj_count = {obj: 0 for obj in CONSIDER}  # counters of object in FoV
frame_dict = {}
last_active = {}  # last time of each device's activity
last_active_check = datetime.now()
ESTIMATED_NUM_PIS = 4  # estimated number of RPis FIXME: customize eg. form browser
ACTIVE_CHECK_PERIOD = 10  # check period [s]
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

# assign montage width and height so we can view all incoming frames
# in a single "dashboard" FIXME: view in browser
m_w = args["montage_w"]
m_h = args["montage_h"]
print("[INFO] detecting: {}...".format(", ".join(obj for obj in CONSIDER)))

while True:
    rpi_name, frame = imageHub.recv_image()
    imageHub.send_reply(b'OK')
    if rpi_name not in last_active.keys():  # registering new device
        print("[INFO] receiving data from {}...".format(rpi_name))
    last_active[rpi_name] = datetime.now()  # update activity record

    frame = imutils.resize(frame, width=400)
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)  # pass blob through network
    detections = net.forward()
    obj_count = {obj: 0 for obj in CONSIDER}  # reset counters before new render

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:  # filtering 'weak' detections
            index = int(detections[0, 0, i, 1])
            if CLASSES[index] in CONSIDER:
                obj_count[CLASSES[index]] += 1
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])  # box sizes
                start_x, start_y, end_x, end_y = box.astype("int")
                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)  # draw rectangle

    cv2.putText(frame, rpi_name, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    label = ", ".join("{}: {}".format(obj, count) for (obj, count) in obj_count.items())  # draw the object count
    cv2.putText(frame, label, (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    frame_dict[rpi_name] = frame
    montages = build_montages(frame_dict.values(), (w, h), (m_w, m_h))
    for (i, montage) in enumerate(montages):  # display
        cv2.imshow("Home pet location monitor ({})".format(i), montage)
    key = cv2.waitKey(1) & 0xFF

    if (datetime.now() - last_active_check).seconds > ACTIVE_CHECK_SECONDS:
        for (rpi_name, ts) in list(last_active.items()):
            if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:  # drop devices that weren't active for to long
                print("[INFO] lost connection to {}".format(rpi_name))
                last_active.pop(rpi_name)
                frame_dict.pop(rpi_name)
        last_active_check = datetime.now()

    if key == ord("q"):
        break

cv2.destroyAllWindows()

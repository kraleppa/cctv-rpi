from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True, help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())

sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(args["server_ip"]))

rpiName = socket.gethostname()
# vs = VideoStream(usePiCamera=True).start()  # just leave it XDD
vs = VideoStream(src=0).start()  # uncomment for USB camera
time.sleep(2.0)

while True:
	frame = vs.read()
	sender.send_image(rpiName, frame)

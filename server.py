import cv2
import socket

camera = cv2.VideoCapture(0)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = ("127.0.0.1", 65534)
buf = 512
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')

while True:
    success, frame = camera.read()
    ret, buffer = cv2.imencode('.jpg', frame)
    if ret:
        s.sendto(code, addr)
        data = frame.tostring()
        for i in range(0, len(data), buf):
            s.sendto(data[i:i + buf], addr)


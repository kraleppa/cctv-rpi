import threading

import cv2
from threading import Thread
import time


class Camera(Thread):
    def __init__(self, fps=20, video_source=0):
        Thread.__init__(self)
        self.lock = threading.Lock()
        self.gpio_controller = None

        self.fps = fps
        self.camera = cv2.VideoCapture(video_source)

        # buffering last 5 seconds
        self.buffer_max_size = 5 * self.fps
        self.frame_buffer = []

        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.__face_detection__ = False

    def run(self):
        delay_time = 1 / self.fps
        while True:
            code, frame = self.camera.read()
            if len(self.frame_buffer) == self.buffer_max_size:
                self.frame_buffer = self.frame_buffer[1:]

            if self.__face_detection__:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if code:
                    faces = self.faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )

                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            time.sleep(delay_time)
            self.frame_buffer.append(frame)

    def get_frame(self):
        return cv2.imencode('.png', self.frame_buffer[-1])[1].tobytes()

    def switch_face_detection(self):
        self.lock.acquire()
        self.face_detection = not self.__face_detection__
        self.gpio_controller.switch_led(self.__face_detection__)
        self.lock.release()

    def get_face_detection(self):
        self.lock.acquire()
        ret = self.__face_detection__
        self.lock.release()
        return ret

import threading
from concurrent.futures import ThreadPoolExecutor
import cv2
from threading import Thread
import datetime
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
        self.__save_photo__ = False

        self._tpe = ThreadPoolExecutor(100)

        self.cooldown_reverse_counter = 0

    def run(self):
        delay_time = 1 / self.fps
        while True:
            code, frame = self.camera.read()
            if len(self.frame_buffer) == self.buffer_max_size:
                self.frame_buffer = self.frame_buffer[1:]

            self.cooldown_reverse_counter += 1

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

                    print(self.cooldown_reverse_counter)

                    if len(faces) > 0 and self.cooldown_reverse_counter > 100:
                        self.cooldown_reverse_counter = 0
                        self._tpe.submit(self._save_photo, frame)

                    if self.__save_photo__:
                        self._tpe.submit(self._save_photo, frame)
                        self.__save_photo__ = False

            time.sleep(delay_time)
            self.frame_buffer.append(frame)

    def get_frame(self):
        return cv2.imencode('.png', self.frame_buffer[-1])[1].tobytes()

    def switch_face_detection(self):
        self.lock.acquire()
        self.__face_detection__ = not self.__face_detection__
        self.gpio_controller.switch_led(self.__face_detection__)
        self.lock.release()

    def get_face_detection(self):
        self.lock.acquire()
        ret = self.__face_detection__
        self.lock.release()
        return ret

    def save_photo(self):
        self.lock.acquire()
        self.__save_photo__ = True
        self.lock.release()

    @staticmethod
    def _save_photo(frame):
        name = f'images/frame_{datetime.datetime.now().isoformat("T")}.jpg'  # name in RFC 3339 format
        cv2.imwrite(name, frame)

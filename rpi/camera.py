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

        # buffering last 5 seconds of video (frames)
        self.buffer_max_size = 5 * self.fps
        self.frame_buffer = []

        # Loading file containing instructions for face detection
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # flag indicating whether to detect face or not. Turned off by default
        self.__face_detection__ = False

        # flag used to mark current frame to be saved on disk
        self.__save_photo__ = False

        # pool of threads used for delegating blocking operations
        self._tpe = ThreadPoolExecutor(100)

        # counts frames between saving images
        self.cooldown_reverse_counter = 0

    def run(self):
        delay_time = 1 / self.fps
        while True:
            code, frame = self.camera.read()
            if len(self.frame_buffer) == self.buffer_max_size:
                self.frame_buffer = self.frame_buffer[1:]

            self.cooldown_reverse_counter += 1

            if self.__face_detection__:

                # copy of current frame in gray. Necessary for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if code:

                    # detect faces present on frame. Returns points used to draw rectangles that mark faces
                    faces = self.faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )

                    # mark each detected face on frame
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # save image on disk if any face is detected and if enough
                    #  time (frames) has passed since last detection
                    if len(faces) > 0 and self.cooldown_reverse_counter > 100:
                        self.cooldown_reverse_counter = 0
                        self._tpe.submit(self._save_photo, frame)

            # save frame if it manually ordered to do so
            if self.__save_photo__:
                self._tpe.submit(self._save_photo, frame)
                self.__save_photo__ = False

            time.sleep(delay_time)
            self.frame_buffer.append(frame)

    # get frame from buffer as na .PNG image
    def get_frame(self):
        return cv2.imencode('.png', self.frame_buffer[-1])[1].tobytes()

    # switch face detection (ON/OFF)
    def switch_face_detection(self):
        self.lock.acquire()
        self.__face_detection__ = not self.__face_detection__
        self.gpio_controller.switch_led(self.__face_detection__)
        self.lock.release()

    # get current status of face detection
    def get_face_detection_status(self):
        self.lock.acquire()
        ret = self.__face_detection__
        self.lock.release()
        return ret

    # change flag to mark current frame to be saved on disk
    def set_save_photo_flag(self):
        self.lock.acquire()
        self.__save_photo__ = True
        self.lock.release()

    # save frame on disk as .JPG image. Name of an image matches RFC 3339 date format
    @staticmethod
    def _save_photo(frame):
        name = f'images/frame_{datetime.datetime.now().isoformat("T")}.jpg'  # name in RFC 3339 format
        cv2.imwrite(name, frame)

import cv2
from threading import Thread
import time


class Camera(Thread):
    def __init__(self, fps=20, video_source=0):
        Thread.__init__(self)
        self.fps = fps
        self.camera = cv2.VideoCapture(video_source)

        # buffering last 5 seconds
        self.buffer_max_size = 5 * self.fps
        self.frame_buffer = []

        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def run(self):
        delay_time = 1 / self.fps
        while True:
            code, frame = self.camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if code:
                if len(self.frame_buffer) == self.buffer_max_size:
                    self.frame_buffer = self.frame_buffer[1:]

                faces = self.faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                self.frame_buffer.append(frame)
            time.sleep(delay_time)

    def get_frame(self):
        return cv2.imencode('.png', self.frame_buffer[-1])[1].tobytes()
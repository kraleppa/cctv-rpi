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

    def run(self):
        delay_time = 1 / self.fps
        while True:
            code, frame = self.camera.read()
            if code:
                if len(self.frame_buffer) == self.buffer_max_size:
                    self.frame_buffer = self.frame_buffer[1:]

                self.frame_buffer.append(frame)
            time.sleep(delay_time)

    def get_frame(self):
        return cv2.imencode('.png', self.frame_buffer[-1])[1].tobytes()

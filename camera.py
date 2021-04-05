import cv2
import threading
import time

thread = None


class Camera:
    def __init__(self, fps=20, video_source=0):
        self.fps = fps
        self.camera = cv2.VideoCapture(video_source)
        self.max_frames = 5 * self.fps
        self.frames = []

    def run(self):
        global thread
        if thread is None:
            thread = threading.Thread(target=self._capture_loop, daemon=True)
            thread.start()

    def _capture_loop(self):
        dt = 1 / self.fps
        while True:
            v, im = self.camera.read()
            if v:
                if len(self.frames) == self.max_frames:
                    self.frames = self.frames[1:]
                # print(self.frames)
                self.frames.append(im)
            time.sleep(dt)

    def get_frame(self):
        print(self.frames)
        return cv2.imencode('.png', self.frames[-1])[1].tobytes()

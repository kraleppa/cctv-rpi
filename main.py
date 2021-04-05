from flask import Flask, render_template, Response
from camera import Camera
import time

app = Flask(__name__)
camera = Camera()
camera.run()

@app.after_request
def add_header(r):
    """
	Add headers to both force latest IE rendering or Chrome Frame,
	and also to cache the rendered page for 10 minutes
	"""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(cam):
    while True:
        frame = cam.get_frame()
        print(frame)
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(gen(camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

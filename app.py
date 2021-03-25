from motion_detection import motiondetecor
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
output_frame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
# initialize the video stream and allow the camera sensor to
# warmup
# vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


def detect_motion(frame_count):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, output_frame, lock
    # initialize the motion detector and the total number of frames
    # read thus far
    md = motiondetecor.SingleMotionDetector(accum_weight=0.5)
    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frame_count:
            # detect motion in the image
            motion = md.detect(gray)
            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                # FIXME problems with infinity values
                INF = 1e6
                (thresh, (min_x, min_y, max_x, max_y)) = motion
                (thresh, (min_x, min_y, max_x, max_y)) = (thresh, (min(min_x, -INF), min(min_y, -INF), max(max_x, INF), max(max_y, INF)))
                cv2.rectangle(img=frame, pt1=(int(min_x), int(min_y)), pt2=(int(max_x), int(max_y)), color=(0, 0, 255), thickness=2)

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1
        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            output_frame = frame.copy()


def generate():
    # grab global references to the output frame and lock variables
    global output_frame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if output_frame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--ip", type=str, required=True,
    #                 help="ip address of the device")
    # ap.add_argument("-o", "--port", type=int, required=True,
    #                 help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=30,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())
    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()
    # start the flask app
    app.run(host="0.0.0.0", port=8000, debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()

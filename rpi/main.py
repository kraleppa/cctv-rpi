from flask import Flask, Response, jsonify
from camera import Camera

app = Flask(__name__)
camera = Camera()
camera.start()


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


def gen(cam):
    while True:
        frame = cam.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def video_feed():
    return Response(gen(camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/detection/face', methods=['POST'])
def face_detection_trigger():
    camera.face_detection = not camera.face_detection
    if camera.face_detection:
        return jsonify({'isTurnedOn': True}), 200
    else:
        return jsonify({'isTurnedOn': False}), 200


@app.route('/detection/face/status', methods=['GET'])
def face_detection_status():
    if camera.face_detection:
        return jsonify({'isTurnedOn': True}), 200
    else:
        return jsonify({'isTurnedOn': False}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

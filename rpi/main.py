import json

from flask import Flask, Response, send_file
from camera import Camera
from gpio_controller import GpioController
from os import walk, remove

app = Flask(__name__)
camera = Camera()
gpio_controller = GpioController(camera)
camera.gpio_controller = gpio_controller
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
    camera.switch_face_detection()
    face_detection = camera.get_face_detection()
    return json.dumps({
        "face_detection": face_detection
    })

@app.route('/state')
def get_state():
    return json.dumps({
        "face_detection": camera.get_face_detection()
    })


@app.route('/images/names')
def get_images_names():
    img_names = []
    for _, _, img_names in walk('./images/'):
        pass
    for file in img_names:
        if ".jpg" not in file:
            img_names.remove(file)
    return json.dumps({
        "images": img_names
    })


@app.route('/images/id/<name>', methods=['GET'])
def get_image_by_name(name):
    for _, _, img_names in walk('./images/'):
        if name in img_names:
            return send_file('./images/' + name, mimetype='image/jpeg')
    return "Error: Image does not exists", 404


@app.route('/images/id/<name>', methods=['DELETE'])
def delete_image_by_name(name):
    for _, _, img_names in walk('./images/'):
        if name in img_names:
            remove(f'./images/{name}')
            return "OK", 200
    return "Error: Image not found", 404


@app.route('/images/save', methods=['POST'])
def save_photo():
    camera.save_photo()
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

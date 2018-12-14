import cv2
import sys
from mailer import sendEmail
from flask import Flask, render_template, Response
from capture import Camera
from flask_basicauth import flask_basicauth
import time
import threading

update_interval = 600
camera = Camera(flip=True)
object_classifier = cv2.CascadeClassifier("models/fullbody_recognition_model.xml")

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0

def check_for_objects():
    global last_epoch
    while True:
        try: 
            frame, found_obj = camera.get_object(object_classifier)
            if found_obj and (time.time()-last_epoch) > update_interval:
                last_epoch = time.time()
                sendEmail(frame)

        except: 
                print( "error sending email:", sys.exc_info()[0])

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False) # change host ip
from flask import Flask, render_template, Response, url_for 
import cv2

app = Flask(__name__)

# initialize face detection model
face_model = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(face_model)

# initializes video capture from web-cam
video_capture = None
anterior = 0

# function to generate frames from camera for face detection model to process 
def generate_frames():
    global video_capture  
    while True:
        if video_capture is None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')
            continue

        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not ret:
            break

        # converts frames to gray-scale for model to process
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # draws a rectangle around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # encodes the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# home page route
@app.route('/')
def index():
    return render_template('index.html')

# video streaming route
@app.route('/video_feed')
def video_feed():

    # uses the global video_capture variable to access the camera stream
    global video_capture
    if video_capture is None:
        video_capture = cv2.VideoCapture(0)

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()

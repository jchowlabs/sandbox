from flask import Flask, render_template
import speech_recognition as sr

# Initialize the Flask application
app = Flask(__name__)

# Default URL of the web app
@app.route('/')
def index():
    return render_template('index.html')

# Route to recognize the user's voice
@app.route('/recognize', methods=['POST'])
def recognize():

    # Get the user's voice from POST request
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    # Recognize the user's voice
    try:
        text = recognizer.recognize_google(audio)
    
    # Exception handling for errors
    except sr.UnknownValueError:
        text = "Sorry, I didn't understand. Please try again."
    except sr.RequestError as e:
        text = "Error: {0}".format(e)

    return text

if __name__ == '__main__':
    app.run()

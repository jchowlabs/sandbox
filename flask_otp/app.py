from flask import Flask, render_template, request, redirect, url_for
import random
import threading
import time

# creates Flask app
app = Flask(__name__)

# hard coded global variables for demo purposes
username = "jason"
password = "Hello123!!"
current_otp = None
message = None

# generates random number every 15 seconds
def generate_otp():
    global current_otp
    while True:
        current_otp = random.randint(100000, 999999)
        time.sleep(15)

# starts new thread for generate_otp function
number_thread = threading.Thread(target=generate_otp)
number_thread.daemon = True
number_thread.start()

# route for index.html page that handles username, password and otp input and validation
@app.route('/', methods=['GET', 'POST'])
def index():
    global message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_otp = request.form['user_otp']
        if (
            username == username
            and password == password
            and user_otp.isdigit()
            and int(user_otp) == current_otp
        ):
            return redirect(url_for('dashboard'))
        else:
            message = "Authentication failed, please try again."

    return render_template('index.html', number=current_otp, message=message)

# route for dashboard.html page that is displayed after successful authentication
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()

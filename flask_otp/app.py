from flask import Flask, render_template, request, redirect, url_for
import random
import threading
import time

app = Flask(__name__)

# Variables to store the current random number, username, and password
current_number = None
username = "jason"
password = "Hello123!!"
message = None

# Function to generate a random 6-digit number
def generate_otp():
    global current_otp
    while True:
        current_otp = random.randint(100000, 999999)
        time.sleep(10)

# Start a separate thread for the number generation
number_thread = threading.Thread(target=generate_otp)
number_thread.daemon = True
number_thread.start()

# Route to render the HTML template with the random number and handle form submission
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

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()

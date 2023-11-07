from flask import Flask, render_template, request
import hashlib
import os

app = Flask(__name__)

# Function to generate a random salt
def generate_salt():
    return os.urandom(16)  # 16 bytes (128 bits)

# Function to hash a password with the provided salt
def hash_password(password, salt):
    salted_password = password.encode('utf-8') + salt
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return hashed_password, salted_password  # Return the hashed password and salted password

@app.route('/', methods=['GET', 'POST'])
def login():
    original_password = ''
    salt = ''
    hashed_password = ''
    salted_password = ''
    
    if request.method == 'POST':
        password = request.form['password']
        salt = generate_salt()
        hashed_password, salted_password = hash_password(password, salt)
        original_password = password

    return render_template('index.html', original_password=original_password, salt=salt, hashed_password=hashed_password, salted_password=salted_password)

if __name__ == '__main__':
    app.run(debug=True)

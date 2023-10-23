from flask import Flask, render_template, request
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

app = Flask(__name__)

# Initialize global variables for RSA key pair
rsa_key = None
private_key = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_keys", methods=["POST"])
def generate_keys():
    global rsa_key, private_key
    # Generate an RSA key pair
    rsa_key = RSA.generate(2048)
    private_key = rsa_key.export_key()
    public_key = rsa_key.publickey().export_key()
    
    return render_template("index.html", public_key=public_key.decode(), private_key=private_key.decode())

@app.route("/encrypt", methods=["POST"])
def encrypt():
    global rsa_key
    if rsa_key is None:
        return "RSA key pair not generated. Please generate keys first."
    
    word_to_encrypt = request.form.get("word_to_encrypt")
    #if not word_to_encrypt:
    #    return "Please enter a word to encrypt."

    # Create a cipher object with the public key
    cipher = PKCS1_OAEP.new(rsa_key.publickey())
    encrypted_message = cipher.encrypt(word_to_encrypt.encode())
    
    return render_template("index.html", encrypted_message=encrypted_message.hex())

@app.route("/decrypt", methods=["POST"])
def decrypt():
    global rsa_key
    if rsa_key is None:
        return "RSA key pair not generated. Please generate keys first."
    
    encrypted_message = request.form.get("encrypted_message")
    if not encrypted_message:
        return "Please enter the encrypted message."
    
    # Create a cipher object with the private key
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted_message = cipher.decrypt(bytes.fromhex(encrypted_message)).decode()
    
    return render_template("index.html", decrypted_message=decrypted_message)

if __name__ == "__main__":
    app.run()

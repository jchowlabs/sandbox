from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    start_time = request.form['start_time']
    end_time = time.time()
    time_elapsed = end_time - float(start_time)
    
    return jsonify({'time_elapsed': time_elapsed})

if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = 'jchowlabs' # jchowlabs API key

# Define a function to analyze logs
def analyze_logs(log_file, query):
    # Read the log file
    with open(log_file, 'r') as file:
        logs = file.readlines()

    # Process logs and find relevant information
    results = []
    for log in logs:
        if query.lower() in log.lower():
            results.append(log.strip())

    if not results:
        results.append("No matching logs found for the query.")

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        log_file = 'server_logs.txt'
        results = analyze_logs(log_file, query)
        return render_template('index.html', query=query, results=results)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()

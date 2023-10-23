from flask import Flask, request, render_template
import openai

app = Flask(__name__)
openai.api_key = 'jchowlabs' # jchowlabs API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/complete', methods=['POST'])
def complete():

    # gets text from form and sends to OpenAI for text completion
    text = request.form['text']
    response = openai.Completion.create(engine="text-davinci-002", prompt=text, max_tokens=10, n=1)
    completed_text = response.choices[0].text
    return completed_text

if __name__ == '__main__':
    app.run()

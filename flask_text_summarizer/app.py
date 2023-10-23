from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

def summarize(text, max_length=125):

    # initializes the huggingface text summarization model with pre-defined length
    summarizer = pipeline("summarization")
    summarized = summarizer(text, max_length=max_length, min_length=25, do_sample=False)
    return summarized[0]['summary_text']

@app.route('/', methods=['GET', 'POST'])
def summarize_text():

    # gets original text from form, summarizes and returns summarized text
    if request.method == 'POST':
        original_text = request.form['original_text']
        max_length = int(request.form['max_length'])  
        summarized_text = summarize(original_text, max_length)
    else:
        original_text = ''
        summarized_text = ''

    return render_template('index.html', original_text=original_text, summarized_text=summarized_text)


if __name__ == '__main__':
    app.run()

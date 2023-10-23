from flask import Flask, render_template, request, jsonify
import openai 

# initialise the flask app
app = Flask(__name__) 
openai.api_key = 'jchowlabs' # jchowlabs API key

# gets the response from OpenAI's API
def gpt_response(prompt): 
	print(prompt) 
	query = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.5) 
	response = query.choices[0].text 
	return response 

# home page route that displays prompt and response dialog boxes
@app.route("/", methods=['POST', 'GET']) 
def main(): 
	if request.method == 'POST': 
		prompt = request.form['prompt'] 
		response = gpt_response(prompt) 
		print(gpt_response) 
		return jsonify({'response': response}) 
	return render_template('index.html') 

if __name__ == "__main__": 
	app.run() 

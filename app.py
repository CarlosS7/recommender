from flask import Flask,render_template,url_for,request
import pandas as pd
import requests

app = Flask(__name__)

API_TOKEN = '[YOUR DR API TOKEN HERE]'
USERNAME = '[YOUR USERNAME HERE]'

PROJECT_ID = '[YOUR PROJECT ID HERE]'
MODEL_ID = '[YOUR MODEL ID HERE]'

# Set HTTP headers
# Note: The charset should match the contents of the file.
headers = {'Content-Type': 'text/plain; charset=UTF-8'}

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		full_text = 'Call Category,Purpose\r\n,'+rawtext+'\r\n'
		data = full_text.encode('utf-8')
		predictions_response = requests.post('https://osmae2lnxs129.amer.sykes.com/predApi/v1.0/%s/%s/predict' % (PROJECT_ID, MODEL_ID),
                                     auth=(USERNAME, API_TOKEN), data=data, headers=headers, verify=False)
		predictions = predictions_response.json()
		pred_results = []
		for item in predictions.values():
			for value in item:
				pred_results.append(value['prediction'])
		
	
	return render_template("index.html",results=pred_results)


if __name__ == '__main__':
	app.run(debug=True)
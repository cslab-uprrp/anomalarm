#!/usr/bin/env python
from flask import Flask, render_template, request
from client import handle

app = Flask(__name__)
app._static_folder = "static/"

@app.route("/")
def main():
	return render_template('index.html')

@app.route('/', methods = ['POST'])
def getInput():
	fromDate = request.form['From']
	toDate = request.form['To']
	print("The from date is " + fromDate)
	print("The to date is " + toDate)
	handle(3, fromDate, toDate)
	return render_template('graph.html')

if __name__ == "__main__":
	app.run(host= '0.0.0.0', debug = True)
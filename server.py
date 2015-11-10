from flask import Flask, render_template, redirect, request,session,flash

import re

EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

from mysqlconnection import MySQLConnector

app = Flask(__name__)

mysql = MySQLConnector('emaildb')

app.secret_key = 'ItsASecret'


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def submit():
	if len(request.form['email']) < 1:
		flash("Email cannot be empty")
	elif not EMAIL_REGEX.match(request.form['email']):
		flash ("Invalid Email Address")
	else:
		print request.form['email']
		sqlstr = "INSERT INTO emails (email, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(request.form['email'])
		print sqlstr
		mysql.run_mysql_query(sqlstr)
		return redirect('/success/'+request.form['email'])
	return render_template('/process')

@app.route('/success/<neaddr>', methods=['GET'])
def list(neaddr):
	emailaddrs = mysql.fetch("SELECT * FROM emails")
	print emailaddrs
	return render_template('success.html', neaddr=neaddr ,emailaddrs=emailaddrs)

app.run(debug=True)


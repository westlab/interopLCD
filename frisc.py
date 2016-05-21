# -*- coding: utf-8 -*-
###########################################
# Flaskr & Rest server wIth Socket Client #
###########################################

#flaskr & rest
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,jsonify,make_response
from contextlib import closing
#socket client
import socket
import sys

#socketclient
HOST,PORT="localhost",9999
data=u""

#Flaskr
# configuration
DATABASE = '/home/pi/ledmatrix/flasker.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g,'db',None)
	if db is not None:
		db.close()

@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, text) values (?, ?)',[request.form['title'], request.form['text']])

        #send data to socketserver
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        data=request.form['text'].encode("utf-8")
        print data
        try:
#            print "socket opened"
            sock.connect((HOST,PORT))
            sock.sendall(data+"\n")
        finally:
            sock.close()
#            print "socket closed"

	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['username'] != app.config['USERNAME']:
			error='Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error='Invalid password'
		else:
			session['logged_in']=True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

@app.route('/rest/api/data',methods=['POST'])
def recieve_send_data():
    if not request.json or not 'text' in request.json:
        abort(400)
    #send data to socketserver
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
#        print "socket opened"
        sock.connect((HOST,PORT))
        sock.sendall(request.json)
    finally:
        sock.close()
#        print "socket closed"

    
if __name__ == '__main__':
	app.run(debug=True,host='10.24.128.182')

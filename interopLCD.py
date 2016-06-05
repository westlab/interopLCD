# -*- coding:  utf-8 -*-
#########################################
# LCD Control with Flaskr & Rest Server #
#########################################

# LCD control
from wledmatrix import WGFX
from rgbmatrix import graphics
import time
from datetime import datetime
from PIL import Image
import threading
import time
import drawLCD

# Flaskr & Rest
import sqlite3
from flask import Flask,  request, session, g, redirect, url_for, \
abort, render_template, flash, jsonify, make_response
from contextlib import closing


# Thread for ledmatrix
class LEDMatrix(threading.Thread):
    def run(self):

        # create Draw instance
        parser = drawLCD.Draw()
        if(not parser.process()):
            parser.print_help()


# Flaskr
# configuration
DATABASE = '/home/pi/ledmatrix/flasker.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

insertdb = False


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql',  mode = 'r') as f:
            db.cursor().executescript(f.read())
            db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select text from entries order by id desc')
    entries = [dict(text = row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html',  entries = entries)


@app.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    for data in drawLCD.myWordData:
        g.db.execute('insert into entries (background, text, color, showImage) values (?, ?, ?, ?)', [data['background'], data['text'], data['color'], data['showImage']])
    g.db.execute('insert into entries (background, text, color, showImage) values (?, ?, ?, ?)', [request.form['background'], request.form['text'], request.form['color'], request.form['showImage']])
    # Insert sent data to myWordData
    i = 0
    drawLCD.myWordData = [{},{},{}]
    while i < 3:
        row = cur.fetchone()
        if row != None:
            drawLCD.myWordData[i].update({
                    'background': str(row[0]),
                    'text': u''.join(row[1]).strip(),
                    'color': str(row[2]),
                    'showImage': str(row[3])
            })
        i = i + 1
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error = error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/api/lcd', methods = ['POST'])
def recieve_data():
    global insertdb
    #if not request.json:
    if not request.json:
        abort(400)
    # insert myWordData to db
    cur = g.db.execute('select background, text, color, showImage from entries order by id asc')
    if insertdb == False:
        for data in drawLCD.myWordData:
            g.db.execute('insert into entries (background, text, color, showImage) values (?, ?, ?, ?)', [data['background'], data['text'], data['color'], data['showImage']])
    # insert newly added data to db
    for data in request.json:
        print data
        g.db.execute('insert into entries (background, text, color, showImage) values (?, ?, ?, ?)', [data.get('background',''), data.get('text',''), data.get('color',''), data.get('showImage','')])
    # insert sent data to myWordData
    i = 0
    drawLCD.dnum_max = 3
    drawLCD.myWordData = [{},{},{}]
    cur = g.db.execute('select background, text, color, showImage from entries order by id desc')
    while i < drawLCD.dnum_max:
        row = cur.fetchone()
        if row != None:
            drawLCD.myWordData[i].update({
                    'background': str(row[0]),
                    'text': u''.join(row[1]).strip(),
                    'color': str(row[2]),
                    'showImage': str(row[3])
            })
        i = i + 1
    g.db.commit()
    insertdb = True
    print drawLCD.myWordData
    return jsonify({'data':  drawLCD.myWordData}), 201


@app.route('/api/door', methods = ['POST'])
def recieve_data():
    global insertdb
    #if not request.json:
    if not request.json:
        abort(400)
    # insert myDoorData to db
    cur = g.db.execute('select background, text, color, showImage from entries order by id asc')
    if insertdb == False:
        for data in drawLCD.myDoorData:
            g.db.execute('insert into entries (background, text, color, showImage) values (?, ?, ?, ?)', [data['background'], data['text'], data['color'], data['showImage']])
    # insert newly added data to db
    for data in request.json:
        print data
        g.db.execute('insert into entries (background, text, color, showImage) values (?, ?, ?, ?)', [data.get('background',''), data.get('text',''), data.get('color',''), data.get('showImage','')])
    # insert sent data to myDoorData
    i = 0
    drawLCD.dnum_max = 4
    drawLCD.myDoorData = [{},{},{},{}]
    cur = g.db.execute('select background, text, color, showImage from entries order by id desc')
    while i < drawLCD.dnum_max:
        row = cur.fetchone()
        if row != None:
			if i == 0:
				drawLCD.myDoorData[i].update({
					'background': 'white',
					'text': u'Packets Received: ' + str(row[1]),
					'color': 'black',
					'showImage': ''
				})
			if i == 1:
				drawLCD.myDoorData[i].update({
					'background': 'white',
					'text': u'Packets Processed: ' + str(row[1]),
					'color': 'black',
					'showImage': ''
				})
			if i == 2:
				drawLCD.myDoorData[i].update({
					'background': 'white',
					'text': u'TCP Streams Reconstructed: ' + str(row[1]),
					'color': 'black',
					'showImage': ''
				})
			if i == 3:
				drawLCD.myDoorData[i].update({
					'background': 'white',
					'text': u'String Matches: ' + str(row[1]),
					'color': 'black',
					'showImage': ''
				})
        i = i + 1
    g.db.commit()
    insertdb = True
    print drawLCD.myDoorData
    return jsonify({'data':  drawLCD.myDoorData}), 201


# main function
if __name__ == "__main__":
# create & start ledmatrix thread
    ledmatrix = LEDMatrix()
    ledmatrix.start()
# create & start server thread
    # need `use_reloader=False` to deactive reloader and run the program
    # t = threading.Thread(target = app.run(debug = True, host = '10.24.128.182', use_reloader = False))
    t = threading.Thread(target = app.run(debug = True, host = '192.168.1.2', use_reloader = False))
    t.start()

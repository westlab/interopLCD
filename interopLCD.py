# -*- coding: utf-8 -*-
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

# Flaskr & Rest
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,jsonify,make_response
from contextlib import closing

myData={
    'background':"black",
    'text':u"みっくみっくにしてあげる♪-by Hatsune Miku",
    'color':"white",
    'showImage':"miku"
}

myColor={
    'black':graphics.Color(0,0,0),
    'white':graphics.Color(255,255,255),
    'red':graphics.Color(255,0,0),
    'green':graphics.Color(0,255,0),
    'blue':graphics.Color(0,0,255)
}

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
	cur = g.db.execute('select text from entries order by id desc')
	entries = [dict(text=row[0]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
        global myData
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (text) values (?)',[request.form['text']])
        # Insert sent data to myData
        myData={
            'background':request.form['background'],
            'text':request.form['text'],
            'color':request.form['color'],
            'showImage':request.form['showImage']
        }
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

@app.route('/api/lcd',methods=['POST'])
def recieve_data():
    global myData
    if not request.json or not 'text' in request.json:
        abort(400)
    myData={
            'background':request.json['background'],
            'text':request.json['text'],
            'color':request.json['color'],
            'showImage':False
    }
    return jsonify({'data': myData}),201

#Thread for ledmatrix
class LEDMatrix(threading.Thread):
    def run(self):
        class Draw(WGFX):
            def __init__(self,*args,**kwargs):
                super(Draw,self).__init__(*args,**kwargs)

            def Run(self):
                canvas=self.matrix.CreateFrameCanvas()
                height=canvas.height
                width=canvas.width
                jafont=graphics.Font()
                enfont=graphics.Font()

                pos=width

                count=0

                try:
                    jafont.LoadFont("/usr/local/share/fonts/18x18ja.bdf")
                    #enfont.LoadFont("/usr/local/share/fonts/9x18.bdf")
                except:
                    print "No Fonts!"

                while True:
                    canvas.Clear()

                    #TODO:Create mode(?) (e.g. mode1: text flow, mode2: advertise westlab...?)

                    #1.draw background
                    if myData["background"]!="":
                       self.fillBackground(canvas,width,height,myColor[myData["background"]])

                    #2.draw and change color of text(create function)
                    leng1=graphics.DrawText(canvas,jafont,pos,14,myColor[myData["color"]],myData["text"].encode("utf-8"))
                    #leng2=graphics.DrawText(canvas,enfont,pos+leng1,12,graphics.Color(0,255,0),myEnText)

                    #3.draw miku(create function)
                    if myData["showImage"]=="miku":
                        #currentSecond=datetime.now().second
                        #if(currentSecond%2==0):
                        if(count%2==0):
                            self.drawImage(48,0,'hatsune-miku2.ppm',16,16)
                        #elif(currentSecond%2==1):
                        elif(count%2==1):
                            self.drawImage(48,0,'hatsune-miku2-2.ppm',16,16)
                        
                    #move text
                    #TODO:Changable text flow rate
                    #if(count%10==0):
                    pos-=1
                    #    count=0

                    if(pos+leng1<0):
                        pos=width

                    #Change this to time based sleep
                    time.sleep(0.10)

                    canvas=self.matrix.SwapOnVSync(canvas)

                    count+=1

        #create Draw instance
        parser=Draw()
        if(not parser.process()):
            parser.print_help()

#main function
if __name__=="__main__":
#create & start ledmatrix thread
    ledmatrix=LEDMatrix()
    ledmatrix.start()
#create & start server thread
    # need `use_reloader=False` to deactive reloader and run the program
    t=threading.Thread(target=app.run(debug=True,host='10.24.128.182',use_reloader=False))
    t.start()

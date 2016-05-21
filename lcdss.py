# -*- coding: utf-8 -*-
##################################
# LCD Control with Socket Server #
##################################

from wledmatrix import WGFX
from rgbmatrix import graphics
import time
from datetime import datetime
from PIL import Image
import threading
import time
import SocketServer
from flask import request

myText="みっくみっくにしてあげる♪-by Hatsune Miku"

#Thread for server
class Server(threading.Thread):
    def run(self):
        class MyTCPHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                global myText

                self.data=self.request.recv(1024).strip()
                print("{} wrote: ".format(self.client_address[0]))
                print(self.data)

                myText=self.data

        #create Server instance & set Host and Port
        HOST,PORT="localhost",9999
        server=SocketServer.TCPServer((HOST,PORT),MyTCPHandler)
        server.serve_forever()

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

                pos=canvas.width

                count=0

                try:
                    jafont.LoadFont("/usr/local/share/fonts/18x18ja.bdf")
                    #enfont.LoadFont("/usr/local/share/fonts/9x18.bdf")
                except:
                    print "No Fonts!"
                    
                while True:
                    canvas.Clear()

                    #draw text
                    #TODO: Fix text flow overlapping miku
                    leng1=graphics.DrawText(canvas,jafont,pos,14,graphics.Color(0,255,0),myText)
                    #leng2=graphics.DrawText(canvas,enfont,pos+leng1,12,graphics.Color(0,255,0),myEnText)

                    #draw miku
                    #currentSecond=datetime.now().second
                    #if(currentSecond%2==0):
                    if(count%2==0):
                        self.drawImage(48,0,'hatsune-miku2.ppm',16,16)
                    #elif(currentSecond%2==1):
                    elif(count%2==1):
                        self.drawImage(48,0,'hatsune-miku2-2.ppm',16,16)
                        
                    #move text
                    #if(count%10==0):
                    pos-=1
                    #    count=0

                    if(pos+leng1<0):
                        pos=canvas.width

                    time.sleep(0.10)

                    canvas=self.matrix.SwapOnVSync(canvas)

                    count+=1

        #create Draw instance
        parser=Draw()
        if(not parser.process()):
            parser.print_help()

#main function
if __name__=="__main__":
#create server&ledmatrix instance
    server=Server()
    ledmatrix=LEDMatrix()
#start server&ledmatrix thread
    server.start()
    ledmatrix.start()
#end server&ledmatrix thread when "shutdown" is sent
    if(myText=="shutdown"):
        server.end()
        ledmatrix.end()

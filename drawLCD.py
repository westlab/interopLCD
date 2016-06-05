# -*- coding:  utf-8 -*-
######################
# Draw class for LCD #
######################

# LCD control
from wledmatrix import WGFX
from rgbmatrix import graphics
import time
from datetime import datetime
from PIL import Image
import threading
import time


myDefaultData = [{
    'background': "black",
    'text': u"Interop 2016",
    'color': "white",
    'showImage': "miku"
},
{
    'background': "black",
    'text': u"慶應義塾大学西研究室",
    'color': "green",
    'showImage': ""
},
{
    'background': "black",
    'text': u"Service-oriented Router",
    'color': "red",
    'showImage': ""
},
{
    'background': "black",
    'text': u"Keio Univ. WestLab",
    'color': "blue",
    'showImage': ""
}]

myWordData = [{
    'background': "black",
    'text': u"Interop 2016",
    'color': "white",
    'showImage': "miku"
},
{
    'background': "black",
    'text': u"慶應義塾大学西研究室",
    'color': "green",
    'showImage': ""
},
{
    'background': "black",
    'text': u"Service-oriented Router",
    'color': "red",
    'showImage': ""
}]

myDoorData = [{},{},{},{}]


myColor = {
    'black': graphics.Color(0, 0, 0),
    'white': graphics.Color(255, 255, 255),
    'red': graphics.Color(255, 0, 0),
    'green': graphics.Color(0, 255, 0),
    'blue': graphics.Color(0, 0, 255)
}

dnum_max = 3


def drawWestLabData(self, canvas, width, height, enfont, pos):
	self.fillBackground(canvas, width, height, graphics.Color(0,0,0))

	# 1. draw keio pen
	lengKoPen = self.drawImage(pos, 0, 'keiopen.ppm', 16, 16)

	# 2.draw and change color of text
	leng = graphics.DrawText(canvas, enfont, pos + lengKoPen, 14, graphics.Color(255,255,255), 'Keio Univ.'.encode("utf-8"))

	# 3. draw westlab mark
	lengWestlab = self.drawImage(pos + leng + lengKoPen, 0, 'westlab.ppm', 104, 16)

	# 4. draw sor westlab
	lengSorWest = self.drawImage(pos + leng + lengKoPen + lengWestlab, 0, 'sorwestlab.ppm', 350, 16)

	# move text
	pos -= 2

	if(pos + leng + lengKoPen + lengWestlab + lengSorWest < 0):
		pos = width


def drawWordData(self, canvas, width, height, jafont, pos, dnum):
    count = 0

	# 1.draw background
    if myWordData[dnum]["background"] != "":
		self.fillBackground(canvas, width, height, myColor[myWordData[dnum]["background"]])

	# 2.draw and change color of text
    leng = graphics.DrawText(canvas, jafont, pos, 14, myColor[myWordData[dnum]["color"]], myWordData[dnum]["text"].encode("utf-8"))

	# 3.draw miku
    if myWordData[dnum]["showImage"] == "miku":
		if(count % 2 == 0):
			self.drawImage(48, 0, 'hatsune-miku2.ppm', 16, 16)
		elif(count % 2 == 1):
			self.drawImage(48, 0, 'hatsune-miku2-2.ppm', 16, 16)
		if count > 1:
			count = 0

	# move text
    pos -= 2

	# if completly scrolled text move to next text
    if(pos + leng < 0):
		dnum += 1
    if(dnum > dnum_max):
		dnum = 0

    if(pos + leng < 0):
		pos = width

    count += 1


def drawDoorData(self, canvas, width, height, enfont, pos, dnum):
    count = 0

	# 1.draw background
    if myDoorData[dnum]["background"] != "":
		self.fillBackground(canvas, width, height, myColor[myDoorData[dnum]["background"]])

	# 2.draw and change color of text
    leng = graphics.DrawText(canvas, enfont, pos, 14, myColor[myDoorData[dnum]["color"]], myDoorData[dnum]["text"].encode("utf-8"))

	# 3.draw miku
    if myDoorData[dnum]["showImage"] == "miku":
		if(count % 2 == 0):
			self.drawImage(48, 0, 'hatsune-miku2.ppm', 16, 16)
		elif(count % 2 == 1):
			self.drawImage(48, 0, 'hatsune-miku2-2.ppm', 16, 16)
		if count > 1:
			count = 0

	# move text
    pos -= 2

	# if completly scrolled text move to next text
    if(pos + leng < 0):
		dnum += 1
    if(dnum > dnum_max):
		dnum = 0

    if(pos + leng < 0):
		pos = width

    count += 1


def changeMode(preSec):
	currentSec = datetime.now().minute * 60 + datetime.now().second
	difSec = currentSec - preSec
	if difSec % (60 * 20) == 0:
		return 2
	elif difSec % (60 * 5) == 0:
		return 1
	elif difSec % 20 == 0:
		return 0


class Draw(WGFX):


    def __init__(self, *args, **kwargs):
        super(Draw, self).__init__(*args, **kwargs)


    def Run(self):
        canvas = self.matrix.CreateFrameCanvas()
        height = canvas.height
        width = canvas.width
        jafont = graphics.Font()
        enfont = graphics.Font()

        pos = width

		# an indication for data number
        dnum = 0

		# get initiate second
        preSec = datetime.now().minute * 60 + datetime.now().second
        mode = 2

        try:
            jafont.LoadFont("/usr/local/share/fonts/18x18ja.bdf")
            enfont.LoadFont("/usr/local/share/fonts/9x18.bdf")
        except:
            print "No Fonts!"

        while True:
            canvas.Clear()

            # TODO: Create mode(?) (e.g. mode1:  text flow,  mode2:  advertise westlab...?)

            if mode != changeMode(preSec) and changeMode(preSec) != None:
                mode = changeMode(preSec)
            if mode == 0:
			    drawDoorData(canvas, width, height, enfont, pos, dnum)
            elif mode == 1:
				drawWordData(canvas, width, height, jafont, pos, dnum)
            elif mode == 2:
				drawWestLabData(canvas, width, height, enfont, pos)

            time.sleep(0.10)

            canvas = self.matrix.SwapOnVSync(canvas)

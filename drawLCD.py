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


myDoorData = [{
    'background': "black",
    'text': u"Interop 2016",
    'color': "white",
    'showImage': "miku"
},
{
    'background': "black",
    'text': u"Service-oriented Router",
    'color': "blue",
    'showImage': "miku"
},
{
    'background': "black",
    'text': u"Keio Univ.",
    'color': "red",
    'showImage': "miku"
},
{
    'background': "black",
    'text': u"WESTLAB",
    'color': "green",
    'showImage': "miku"
}]

myWordData = [{
    'background': "black",
    'text': u"Interop 2016",
    'color': "white",
    'showImage': ""
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

myColor = {
    'black': graphics.Color(0, 0, 0),
    'white': graphics.Color(255, 255, 255),
    'red': graphics.Color(255, 0, 0),
    'green': graphics.Color(0, 255, 0),
    'blue': graphics.Color(0, 0, 255)
}


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

        count = 0

        # an indication for data number
        dnum = 0
        dnum_max = 2

        # Set mode
        mode = 0

        try:
            jafont.LoadFont("/usr/local/share/fonts/18x18ja.bdf")
            enfont.LoadFont("/usr/local/share/fonts/9x18.bdf")
        except:
            print "No Fonts!"

        while True:
            canvas.Clear()

            # TODO: Create mode(?) (e.g. mode1:  text flow,  mode2:  advertise westlab...?)

            # MODE1: ADVERTISE WESTLAB
            if mode == 0:
                self.fillBackground(canvas, width, height, graphics.Color(255,255,255))

                # 1. draw keio pen
                lengKoPen = self.drawImage(pos, 0, 'keiopen.ppm', 16, 16)

                # 2.draw and change color of text
                leng = graphics.DrawText(canvas, enfont, pos + lengKoPen, 14, graphics.Color(0,0,0), 'Keio Univ.'.encode("utf-8"))

                # 3. draw westlab mark
                lengWestlab = self.drawImage(pos + leng + lengKoPen, 0, 'westlab.ppm', 104, 16)

                # 4. draw sor westlab
                lengSorWest = self.drawImage(pos + leng + lengKoPen + lengWestlab, 0, 'sorwestlab.ppm', 350, 16)

                # move text
                pos -= 3

                if(pos + leng + lengKoPen + lengWestlab + lengSorWest < 0):
                    pos = width
                    mode = 1
                    dnum = 0
                    dnum_max = 2

            # MODE2: DRAW WORD DATA
            elif mode == 1:

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
                pos -= 3

                # if completly scrolled text move to next text
                if(pos + leng < 0):
                    dnum += 1
                if(dnum > dnum_max):
                    mode = 2
                    dnum = 0
                    dnum_max = 3

                if(pos + leng < 0):
                    pos = width

                count += 1

            # MODE3: DRAW DOOR DATA
            elif mode == 2:

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
                pos -= 3

                # if completly scrolled text move to next text
                if(pos + leng < 0):
                    dnum += 1
                if(dnum > dnum_max):
                    mode = 0
                    dnum = 0
                    dnum_max = 2

                if(pos + leng < 0):
                    pos = width

                count += 1

            time.sleep(0.10)

            canvas = self.matrix.SwapOnVSync(canvas)

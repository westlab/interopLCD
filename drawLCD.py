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


myData = [{
    'background': "black", 
    'text': u"NOC 乙です！", 
    'color': "white", 
    'showImage': "miku"
},
{
    'background': "black", 
    'text': u"慶應義塾大学西研究室", 
    'color': "blue", 
    'showImage': ""
},
{
    'background': "black",
    'text': u"Service-oriented Router", 
    'color': "red", 
    'showImage': ""
}
]

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

        dnum = 0

        try: 
            jafont.LoadFont("/usr/local/share/fonts/18x18ja.bdf")
            # enfont.LoadFont("/usr/local/share/fonts/9x18.bdf")
        except: 
            print "No Fonts!"

        while True: 
            canvas.Clear()

            # TODO: Create mode(?) (e.g. mode1:  text flow,  mode2:  advertise westlab...?)

            # 1.draw background
            if myData[dnum]["background"] != "": 
               self.fillBackground(canvas, width, height, myColor[myData[dnum]["background"]])

            # 2.draw and change color of text(create function)
            leng1 = graphics.DrawText(canvas, jafont, pos, 14, myColor[myData[dnum]["color"]], myData[dnum]["text"].encode("utf-8"))
            # leng2 = graphics.DrawText(canvas, enfont, pos+leng1, 12, graphics.Color(0, 255, 0), myEnText)

            # 3.draw miku(create function)
            if myData[dnum]["showImage"] == "miku": 
                # currentSecond=datetime.now().second
                # if(currentSecond%2 == 0): 
                if(count%2 == 0): 
                    self.drawImage(48, 0, 'hatsune-miku2.ppm', 16, 16)
                # elif(currentSecond%2==1): 
                elif(count%2 == 1): 
                    self.drawImage(48, 0, 'hatsune-miku2-2.ppm', 16, 16)
                if count > 1:
                    count = 0
                
            # move text
            # TODO: Changable text flow rate
            # if(count%10 == 0): 
            pos -= 2
            #    count = 0

            if(pos + leng1 < 0):
                dnum += 1
            if(dnum > 2):
                dnum = 0

            if(pos + leng1 < 0): 
                pos = width

            time.sleep(0.10)

            canvas = self.matrix.SwapOnVSync(canvas)

            count += 1

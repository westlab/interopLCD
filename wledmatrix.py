# -*- coding: utf-8 -*-
import argparse, time, sys, os
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
from PIL import Image

class WGFX(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(WGFX, self).__init__(*args, **kwargs)

        self.add_argument("-r", "--rows", action = "store", help = "Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default = 32, type = int)
        self.add_argument("-P", "--parallel", action = "store", help = "For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default = 1, type = int)
        self.add_argument("-c", "--chain", action = "store", help = "Daisy-chained boards. Default: 1.", default = 1, type = int)
        self.add_argument("-p", "--pwmbits", action = "store", help = "Bits used for PWM. Something between 1..11. Default: 11", default = 11, type = int)
        self.add_argument("-l", "--luminance", action = "store_true", help = "Don't do luminance correction (CIE1931)")
        self.add_argument("-b", "--brightness", action = "store", help = "Sets brightness level. Default: 100. Range: 1..100", default = 100, type = int)

        self.args = {}

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def Run(self):
        print("Running")

    def process(self):
        self.args = vars(self.parse_args())

        if self.args["rows"] != 16 and self.args["rows"] != 32:
            print("Rows can either be 16 or 32")
            return False

        if self.args["chain"] < 1:
            print("Chain outside usable range")
            return False

        if self.args["chain"] > 8:
            print("That is a long chain. Expect some flicker.")

        if self.args["parallel"] < 1 or self.args["parallel"] > 3:
            print("Parallel outside usable range.")
            return False

        self.matrix = RGBMatrix(self.args["rows"], self.args["chain"], self.args["parallel"])
        self.matrix.pwmBits = self.args["pwmbits"]
        self.matrix.brightness = self.args["brightness"]

        if self.args["luminance"]:
            self.matrix.luminanceCorrect = False

        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.Run()
        except KeyboardInterrupt:
            print "Exiting\n"
            sys.exit(0)

        return True

    def drawCircle(self, x0, y0, r, cr, cg, cb):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        self.matrix.SetPixel(x0  , y0+r, cr, cg, cb)
        self.matrix.SetPixel(x0  , y0-r, cr, cg, cb)
        self.matrix.SetPixel(x0+r, y0  , cr, cg, cb)
        self.matrix.SetPixel(x0-r, y0  , cr, cg, cb)
        while x<y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self.matrix.SetPixel(x0 + x, y0 + y, cr, cg, cb)
            self.matrix.SetPixel(x0 - x, y0 + y, cr, cg, cb)
            self.matrix.SetPixel(x0 + x, y0 - y, cr, cg, cb)
            self.matrix.SetPixel(x0 - x, y0 - y, cr, cg, cb)
            self.matrix.SetPixel(x0 + y, y0 + x, cr, cg, cb)
            self.matrix.SetPixel(x0 - y, y0 + x, cr, cg, cb)
            self.matrix.SetPixel(x0 + y, y0 - x, cr, cg, cb)
            self.matrix.SetPixel(x0 - y, y0 - x, cr, cg, cb)

    def drawCircleHelper(self, x0, y0, r, cornername, cr, cg, cb):
        f     = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x     = 0
        y     = r
        while x<y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f     += ddF_y
            x += 1
            ddF_x += 2
            f     += ddF_x
            if cornername & 0x4:
                self.matrix.SetPixel(x0 + x, y0 + y, cr, cg, cb)
                self.matrix.SetPixel(x0 + y, y0 + x, cr, cg, cb)
            if cornername & 0x2:
                self.matrix.SetPixel(x0 + x, y0 - y, cr, cg, cb)
                self.matrix.SetPixel(x0 + y, y0 - x, cr, cg, cb)
            if cornername & 0x8:
                self.matrix.SetPixel(x0 - y, y0 + x, cr, cg, cb)
                self.matrix.SetPixel(x0 - x, y0 + y, cr, cg, cb)
            if cornername & 0x1:
                self.matrix.SetPixel(x0 - y, y0 - x, cr, cg, cb)
                self.matrix.SetPixel(x0 - x, y0 - y, cr, cg, cb)

    def fillCircle(self, x0, y0, r, cr, cg, cb):
        self.drawFastVLine(x0, y0-r, 2*r+1, cr, cg, cb)
        self.fillCircleHelper(x0, y0, r, 3, 0, cr, cg, cb)

    def fillCircleHelper(self, x0, y0, r, cornername, delta, cr, cg, cb):
        f     = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x     = 0
        y     = r
        while x<y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f     += ddF_y
            x += 1
            ddF_x += 2
            f     += ddF_x
            if cornername & 0x1:
                self.drawFastVLine(x0+x, y0-y, 2*y+1+delta, cr, cg, cb)
                self.drawFastVLine(x0+y, y0-x, 2*x+1+delta, cr, cg, cb)
            if cornername & 0x2:
                self.drawFastVLine(x0-x, y0-y, 2*y+1+delta, cr, cg, cb)
                self.drawFastVLine(x0-y, y0-x, 2*x+1+delta, cr, cg, cb)

    def drawLine(self, x0, y0, x1, y1, cr, cg, cb):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            (x0, y0) = (y0, x0)
            (x1, y1) = (y1, x1)
        if x0 > x1:
            (x0, x1) = (x1, x0)
            (y0, y1) = (y1, y0)
        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx / 2
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        while x0<=x1:
            if steep:
                self.matrix.SetPixel(y0, x0, cr, cg, cb)
            else:
                self.matrix.SetPixel(x0, y0, cr, cg, cb)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

    def drawRect(self, x, y, w, h, cr, cg, cb):
        self.drawFastHLine(x, y, w, cr, cg, cb)
        self.drawFastHLine(x, y+h-1, w, cr, cg, cb)
        self.drawFastVLine(x, y, h, cr, cg, cb)
        self.drawFastVLine(x+w-1, y, h, cr, cg, cb)

    def drawFastVLine(self, x, y, h, cr, cg, cb):
        self.drawLine(x, y, x, y+h-1, cr, cg, cb)

    def drawFastHLine(self, x, y, w, cr, cg, cb):
        self.drawLine(x, y, x+w-1, y, cr, cg, cb)

    def fillRect(self, x, y, w, h, cr, cg, cb):
        i = x;
        while i<x+w:
            self.drawFastVLine(i, y, h, cr, cg, cb)
            i += 1

    def fillScreen(self, cr, cg, cb):
        self.fillRect(0, 0, self.matrix.width, self.matrix.height, cr, cg, cb)

    def drawRoundRect(self, x, y, w, h, r, cr, cg, cb):
        self.drawFastHLine(x+r  , y    , w-2*r, cr, cg, cb) # Top
        self.drawFastHLine(x+r  , y+h-1, w-2*r, cr, cg, cb) # Bottom
        self.drawFastVLine(x    , y+r  , h-2*r, cr, cg, cb) # Left
        self.drawFastVLine(x+w-1, y+r  , h-2*r, cr, cg, cb) # Right
        self.drawCircleHelper(x+r    , y+r    , r, 1, cr, cg, cb)
        self.drawCircleHelper(x+w-r-1, y+r    , r, 2, cr, cg, cb)
        self.drawCircleHelper(x+w-r-1, y+h-r-1, r, 4, cr, cg, cb)
        self.drawCircleHelper(x+r    , y+h-r-1, r, 8, cr, cg, cb)

    def fillRoundRect(self, x, y, w, h, r, cr, cg, cb):
        self.fillRect(x+r, y, w-2*r, h, cr, cg, cb)
        self.fillCircleHelper(x+w-r-1, y+r, r, 1, h-2*r-1, cr, cg, cb)
        self.fillCircleHelper(x+r    , y+r, r, 2, h-2*r-1, cr, cg, cb)

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, cr, cg, cb):
        self.drawLine(x0, y0, x1, y1, cr, cg, cb)
        self.drawLine(x1, y1, x2, y2, cr, cg, cb)
        self.drawLine(x2, y2, x0, y0, cr, cg, cb)

    def fillTriangle (self, x0, y0, x1, y1, x2, y2, cr, cg, cb):
        if y0 > y1:
            (y0, y1) = (y1, y0)
            (x0, x1) = (x1, x0)
        if y1 > y2:
            (y2, y1) = (y1, y2)
            (x2, x1) = (x1, x2)
        if y0 > y1:
            (y0, y1) = (y1, y0)
            (x0, x1) = (x1, x0)
        if y0 == y2:
            a = b = x0
            if x1 < a:
                a = x1
            elif x1 > b:
                b = x1
            if x2 < a:
                a = x2
            elif x2 > b:
                b = x2
            self.drawFastHLine(a, y0, b-a+1, cr, cg, cb)
            return
        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa   = 0
        sb   = 0
        if y1 == y2:
            last = y1
        else:
            last = y1-1
        y=y0
        while y<=last:
            a   = x0 + sa / dy01
            b   = x0 + sb / dy02
            sa += dx01
            sb += dx02
            if(a > b):
               (a,b) = (b,a)
            self.drawFastHLine(a, y, b-a+1, cr, cg, cb)
            y += 1
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)
        while y<=y2:
            a   = x1 + sa / dy12
            b   = x0 + sb / dy02
            sa += dx12
            sb += dx02
            if a > b:
                (a,b) = (b,a)
                self.drawFastHLine(a, y, b-a+1, cr, cg, cb)
            y += 1

    def drawBitmap(self, x, y, bitmap, w, h, cr, cg, cb):
        byteWidth = (w + 7) / 8
        j = 0
        while j<h:
            i = 0
            while i<w:
                print(bitmap[i][j])
                #if bitmap[i][j]:
                    #self.matrix.SetPixel(x+i, y+j, cr, cg, cb)
                i += 1
            j += 1

    def drawImage(self, x, y, image, w, h):
        im=Image.open(image)
        imdata=list(im.getdata())
        #print("length of imdata is: "+str(len(imdata)))
        j=0
        c=0
        while j<h:
            i=0
            while i<w:
                self.matrix.SetPixel(x+i,y+j,imdata[c][0],imdata[c][1],imdata[c][2])
                #print(type(imdata[c][0]))
                i+=1
                c+=1
            j+=1

    def drawText(self, canvas, pos, jafont, enfont, color, text):
        leng=0
#        jafont=graphics.Font()
#        enfont=graphics.Font()
#        try:
#            jafont.LoadFont("/usr/local/share/fonts/18x18ja.bdf")
#            enfont.LoadFont("/usr/local/share/fonts/9x18.bdf")
#        except:
#            print "No Fonts!"
        for char in text:
            try:
                char.decode('ascii')
            except UnicodeDecodeError:
                print char
                leng+=graphics.DrawText(canvas,jafont,pos,14,color,str(char))
                pos+=18
            else:
                print char
                leng+=graphics.DrawText(canvas,enfont,pos,12,color,str(char))
                pos+=9
        return leng


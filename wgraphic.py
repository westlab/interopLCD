#!/usr/bin/env python
#from samplebase import SampleBase
#from rgbmatrix import graphics

def drawCircle(x0, y0, r, cr, cg, cb):
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

def drawCircleHelper(x0, y0, r, cornername, color):
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

def fillCircle(x0, y0, r, cr, cg, cb):
    drawFastVLine(x0, y0-r, 2*r+1, cr, cg, cb)
    fillCircleHelper(x0, y0, r, 3, 0, cr, cg, cb)

def fillCircleHelper(x0, y0, r, cornername, delta, cr, cg, cb):
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
            drawFastVLine(x0+x, y0-y, 2*y+1+delta, cr, cg, cb)
            drawFastVLine(x0+y, y0-x, 2*x+1+delta, cr, cg, cb)
        if cornername & 0x2:
            drawFastVLine(x0-x, y0-y, 2*y+1+delta, cr, cg, cb)
            drawFastVLine(x0-y, y0-x, 2*x+1+delta, cr, cg, cb)

def drawLine(x0, y0,x1, y1, cr, cg, cb):
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
    ystep
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

def drawRect(x, y, w, h, cr, cg, cb):
    drawFastHLine(x, y, w, cr, cg, cb)
    drawFastHLine(x, y+h-1, w, cr, cg, cb)
    drawFastVLine(x, y, h, cr, cg, cb)
    drawFastVLine(x+w-1, y, h, cr, cg, cb)

def drawFastVLine(x, y, h, cr, cg, cb):
    drawLine(x, y, x, y+h-1, cr, cg, cb)

def drawFastHLine(x, y, w, cr, cg, cb):
    drawLine(x, y, x+w-1, y, cr, cg, cb)

def fillRect(x, y, w, h, cr, cg, cb):
    i = x;
    while i<x+w:
        drawFastVLine(i, y, h, cr, cg, cb)
        i += 1

def fillScreen(cr, cg, cb):
    fillRect(0, 0, _width, _height, cr, cg, cb)

def drawRoundRect(x, y, w, h, r, cr, cg, cb):
    drawFastHLine(x+r  , y    , w-2*r, cr, cg, cb) // Top
    drawFastHLine(x+r  , y+h-1, w-2*r, cr, cg, cb) // Bottom
    drawFastVLine(x    , y+r  , h-2*r, cr, cg, cb) // Left
    drawFastVLine(x+w-1, y+r  , h-2*r, cr, cg, cb) // Right
    drawCircleHelper(x+r    , y+r    , r, 1, cr, cg, cb)
    drawCircleHelper(x+w-r-1, y+r    , r, 2, cr, cg, cb)
    drawCircleHelper(x+w-r-1, y+h-r-1, r, 4, cr, cg, cb)
    drawCircleHelper(x+r    , y+h-r-1, r, 8, cr, cg, cb)

def fillRoundRect(x, y, w, h, r, cr, cg, cb):
    fillRect(x+r, y, w-2*r, h, cr, cg, cb)
    fillCircleHelper(x+w-r-1, y+r, r, 1, h-2*r-1, cr, cg, cb)
    fillCircleHelper(x+r    , y+r, r, 2, h-2*r-1, cr, cg, cb)

def drawTriangle(x0, y0, x1, y1, x2, y2, cr, cg, cb):
    drawLine(x0, y0, x1, y1, cr, cg, cb)
    drawLine(x1, y1, x2, y2, cr, cg, cb)
    drawLine(x2, y2, x0, y0, cr, cg, cb)

def fillTriangle (x0, y0, x1, y1, x2, y2, cr, cg, cb):
    if y0 > y1:
        (y0, y1) = (y1, y0)
        (x0, x1) = (x1, x0)
    if y1 > y2:
        (y2, y1) = (y1, y2)
        (x2, x1) = (xl, x2)
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
        drawFastHLine(a, y0, b-a+1, cr, cg, cb)
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
        drawFastHLine(a, y, b-a+1, cr, cg, cb)
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
            drawFastHLine(a, y, b-a+1, cr, cg, cb)
        y += 1

def drawBitmap(x, y, bitmap, w, h, cr, cg, cb):
    byteWidth = (w + 7) / 8
    j = 0
    while j<h:
        i = 0
        while i<w:
            i += 1
            if bitmap[i][j]:
                self.matrix.SetPixel(x+i, y+j, cr, cg, cb)
        j += 1

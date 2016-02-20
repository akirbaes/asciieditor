#!/usr/bin/env python
# -*- coding: utf-8 -*-
import colorama
import time
import sys
import math
ESC= '\033['
def UP(n):
	return ESC+str(n)+'A'
def DOWN(n):
	return ESC+str(n)+'B'
def RIGHT(n):
	return ESC+str(n)+'C'
def LEFT(n):
	return ESC+str(n)+'D'

def MOVX(n):
	if(n>0):
		return RIGHT(n)
	elif(n<0):
		return LEFT(-n)
	return ""

def SETXY(x,y):
	return ESC+str(y)+';'+str(x)+'H'

ERASE_ALL = ESC + '2J'
ERASE_NEXT = ESC + 'J'
ERASE_PREVIOUS = ESC + '1J'

ERASE_LINE = ESC + "2K"
CLIP_LINE = ESC + "1K"
CUT_LINE = ESC + "0K"

#SGR  = ESC + something + "m"

ENDC = ESC + '0m'
BOLD = ESC + "1m"
FAINT_ = ESC + "2m" #not supported window
ITALIC_ = ESC + "3m" #not supported everywhere, sometimes inverse
UNDERLINE = ESC + "4m" 
BLINK_S = ESC + "5m" #less than 150/60 = 5/2 seconds
BLINK_F = ESC + "6m" #BOTH doesn't seem to work
NEGATIVE = ESC + "7m"
POSITIVE = ESC + "27m"
#CONCEAL = ESC + "8m"
#CROSSED = STRIKE = ESC + "9m"
FONT_RESET = ESC + "10m"
FONT = [None]*10
FONT_0 = FONT[0] = FONT_RESET
FONT_1 = FONT[1] = ESC + "11m"
FONT_2 = FONT[2] = ESC + "12m"
FONT_3 = FONT[3] = ESC + "13m"
FONT_4 = FONT[4] = ESC + "14m"
FONT_5 = FONT[5] = ESC + "15m"
FONT_6 = FONT[6] = ESC + "16m"
FONT_7 = FONT[7] = ESC + "17m"
FONT_8 = FONT[8] = ESC + "18m"
FONT_9 = FONT[9] = ESC + "19m"
FONT_F = ESC + "20m"

SAVE_CURSE = ESC + "s"
LOAD_CURSE = ESC + "u"
HIDE_CURSOR = ESC + "?25l"
SHOW_CURSOR = ESC + "?25h"

BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7

def FG(color):
	return ESC + str(30+color) + "m"

def BG(color):
	return ESC + str(40+color) + "m"

COLORS = ["black","red","green","yellow","blue","magenta","cyan","white"]
COLDICT = dict()
for i,c in enumerate(COLORS):
	COLDICT[c]=i
	COLDICT[i]=c

"""
0x00-0x07:  standard colors (as in ESC [ 30..37 m)
0x08-0x0f:  high intensity colors (as in ESC [ 90..97 m)
0x10-0xe7:  6*6*6=216 colors: 16 + 36*r + 6*g + b (0≤r,g,b≤5)
0xe8-0xff:  grayscale from black to white in 24 steps
"""

def IND_FG(x):
	return ESC + "38;5;" + str(x) + "m"
def RGB_FG(red,green,blue):
	return ESC + "38;2;" + str(red) + ";" + str(green) + ";" + str(blue) + "m"

def IND_BG(x):
	return ESC + "48;5;" + str(x) + "m"
def RGB_BG(red,green,blue):
	return ESC + "48;2;" + str(red) + ";" + str(green) + ";" + str(blue) + "m"

FG0 = ESC + "39m" #default fore
BG0 = ESC + "49m" #default back

#FRAMED = ESC + "51m" #Don't work
#ENCIRCLED = ESC + "52m" #Don't work
#OVERLINES = ESC + "53m" #Don't work


def SET_TITLE(title):
	return '\x1b]2;'+title+'\x07'

#sys.stdout.write()
def SET_SIZE(w,h):
	sys.stdout.write('\x1b[8;{rows};{cols}t'.format(rows=h, cols=w))

WRITE = sys.stdout.write

FLUSH = lambda x: sys.stdout.flush()
Xcol = BG(RED) + FG(WHITE)
Ycol = IND_BG(BLUE+8) + FG(BLACK)
Ocol = BG(GREEN) + IND_FG(GREEN+8)

def main():
	SET_SIZE(100,40)
	FLUSH
	WRITE(SET_TITLE("COLORED DEMO")+HIDE_CURSOR+ERASE_ALL)
	for i in range(100):
		WRITE(SETXY(i,i//2)+Xcol+'X'\
+SETXY(100-i,i//2)+Ycol+'Y'\
+SETXY(50+int(math.cos(i/25.*math.pi)*50*(i/100.)),20+int(math.sin(i/25.*math.pi)*20*(i/100.)))+Ocol+"O")
		sys.stdout.flush()
		time.sleep(1.0/33)
	WRITE(SHOW_CURSOR+ENDC+SETXY(0,40)+ERASE_LINE)


""">>> for a in range(100):
...     list[i]=(list[i-1]+list[i-2])%256
...     print(list[i])
...     i=(i+1)%3
"""

if __name__=="__main__":
	colorama.init()
	while True:
		main()

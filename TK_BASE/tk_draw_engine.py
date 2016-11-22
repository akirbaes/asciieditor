# /usr/bin/env python 3
# -*- coding: utf-8 -*-

try:
	import Tkinter as Tk
	from Tkinter import font
except ImportError:
	import tkinter as Tk
	from tkinter import font
from random import choice

root = Tk.Tk()
monofonts = []

for i in sorted(font.families()):
	if "mono" in i.lower():
		print(i);
		monofonts.append(i)
		
fh = 16
monofont = font.Font(family="Ubuntu Mono",size = -fh)
fw = monofont.measure(" ")
FH=fh
FW=fw

cw = 80
CW = cw
ch = 24
CH = ch

class App:
	def __init__(self,master):
		
		#self.dupeImage = Tk.PhotoImage(file=os.path.join("Darpteam","Code","GUIELEM","duplicate.gif"))
		#self.dupeImage = Tk.PhotoImage(file=os.path.join("..","GUIELEM","duplicate.gif"))

		
		#MAINFRAME
		mainFrame = Tk.Frame(master)
		mainFrame.pack(fill=Tk.BOTH,expand=True)


		#PARAMETERS FRAME on the right    self.parametersFrame
		
		self.parametersFrame = Tk.Frame(mainFrame,bg="pink")
		self.parametersFrame.pack(side=Tk.RIGHT,anchor="e",fill=Tk.BOTH)
		
		self.charactersFrame = Tk.Frame(self.parametersFrame)
		self.charactersFrame.pack(side=Tk.TOP,anchor="n")
		

		self.displayFrame = Tk.Frame(mainFrame)
		self.displayFrame.pack(side=Tk.LEFT)
		

		
		self.canvas = Tk.Canvas(self.displayFrame, width=FW*CW, height=FH*CH)
		self.canvas.pack()
		
		self.canvas_drawing = canvasManager(self.canvas)
		self.drawing_area = drawingArea(self.canvas_drawing)
		self.canvas_drawing.addListerner(self.drawing_area)
		


class canvasManager():
	#Hides the real canvas
	def __init__(self,canvas):
		self.canvas = canvas
		self.c = canvas
		self.wv = FW
		self.hv = FH
		self.listener = None;
		hv = self.hv
		wv = self.wv
		self.bg = [[None]*CH for i in range(CW)]
		self.fg = [[None]*CH for i in range(CW)]
		self.c.create_rectangle(((0,0),(CW*FW,CH*FH)),fill="")
		for i in range(CW):
			for j in range(CH):
				p1 = (i*wv,j*hv)
				bbox = (p1,(i*wv+wv,j*hv+hv))
				self.bg[i][j] = self.c.create_rectangle(bbox,outline="",fill="black")
				self.fg[i][j] = self.c.create_text(p1,anchor="nw",font = monofont)
				
				
		def callback(event):
			self.getEvent(event.x,event.y)
		canvas.bind("<Button-1>", callback)
		
	def putchar(self,x,y,char=None,bg=None,fg=None):
		index = self.fg[x][y]
		if(fg!=None):
			self.c.itemconfig(index, fill=fg)
			
		if(char!=None):
			self.c.itemconfig(index, text=char)
			
		index = self.bg[x][y]
		if(bg!=None):
			self.c.itemconfig(index, fill=bg)
			
	def getEvent(self,x,y):
		print("received event in",x,y)
		#transforms the event in X, Y, tool
		#and sends it to drawingArea which will send it back
		if(self.listener!=None):
			if(x>0 and y>0 and x<cw*fw and y<ch*fh):
				self.listener.click(int(x/fw),int(y/fh),0)
		pass
		
	def addListerner(self,listener):
		self.listener = listener;
			
class drawingArea():
	#Just the areas, like my old ones
	def __init__(self,canvas):
		self.zones = []
		self.drawCanvas = canvas
		self.dc = canvas
		for i in range(min(CH-2,CW-2,25)):
			self.dc.putchar(i,i,chr(ord("a")+i),"red","blue")
		
	def move(self,x,y):
		self.x=x
		self.y=y
	def draw():
		pass
	def click(self,x,y,tool):
		if(tool==0):
			self.dc.putchar(x,y,choice("▀▄█░▒▓"),"black","white")
		pass

def colorConvert(string):
	#receives an \0xetc. code,
	#returns the FG and BG
	#Because I'll probably not use them if I use any engine not console-based
	pass
	
	
app = App(root)
root.mainloop()
try:
	root.destroy() #if it wasn't already
except:
	exit() #quit anyway

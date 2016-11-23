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
DRAWABLE_CHARACTERS = u"""☺☻♥♦♣♠•○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~⌂ ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿıƒ‗─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬▀▄█░▒▓■   """

cw = 80
CW = cw
ch = 24
CH = ch

#black,red,green,yellow,blue,purple,cyan,white
#light with 1

colors = ["black","red","green","gold","blue","purple","cyan","gainsboro"]
colors2 = ["dark slate gray","tomato","chartreuse","yellow","royal blue","magenta","aquamarine","snow",]


curchar = ""
curfg = "" #16
curbg = "" #8

class App:
	def __init__(self,master):
		
		#self.dupeImage = Tk.PhotoImage(file=os.path.join("Darpteam","Code","GUIELEM","duplicate.gif"))
		#self.dupeImage = Tk.PhotoImage(file=os.path.join("..","GUIELEM","duplicate.gif"))

		self.allTools = []
		#MAINFRAME
		mainFrame = Tk.Frame(master)
		mainFrame.pack(fill=Tk.BOTH,expand=True)


		#PARAMETERS FRAME on the right    self.parametersFrame
		
		self.parametersFrame = Tk.Frame(mainFrame,bg="pink")
		self.parametersFrame.pack(side=Tk.RIGHT,anchor="e",fill=Tk.BOTH)
		
		self.charactersFrame = Tk.Frame(self.parametersFrame)
		self.charactersFrame.pack(side=Tk.TOP,anchor="n")
		self.setCharacters(self.charactersFrame)
		
		self.toolsFrame = Tk.Frame(mainFrame)
		self.toolsFrame.pack(side=Tk.TOP)
		self.setTools(self.toolsFrame)

		self.displayFrame = Tk.Frame(mainFrame)
		self.displayFrame.pack(side=Tk.LEFT)
		

		
		self.canvas = Tk.Canvas(self.displayFrame, width=FW*CW, height=FH*CH)
		self.canvas.pack()
		
		self.canvas_drawing = canvasManager(self.canvas)
		self.drawing_area = drawingArea(self.canvas_drawing)
		self.canvas_drawing.addListerner(self.drawing_area)
		
	def setTools(self,toolsFrame):
		self.drawTool = Tk.Button(toolsFrame,text="Draw")
		self.drawTool.pack(side=Tk.LEFT,anchor = "w")
		self.allTools.append(self.drawTool)
		
		#Action: check if right tool otherwise unpressed
	
	def setCharacters(self,charactersFrame):
		label = Tk.Label(charactersFrame,text="Foreground")
		label.pack(side=Tk.TOP)
		fg1 = Tk.Frame(charactersFrame)
		fg1.pack(side=Tk.TOP)
		for c in colors:
			b = Tk.Button(fg1,background=c)
			b.pack(side=Tk.LEFT)
		fg2 = Tk.Frame(charactersFrame)
		fg2.pack(side=Tk.TOP)
		for c in colors2:
			b = Tk.Button(fg2,background=c)
			b.pack(side=Tk.LEFT)
		
		label = Tk.Label(charactersFrame,text="Background")
		label.pack(side=Tk.TOP)
		bg = Tk.Frame(charactersFrame)
		bg.pack(side=Tk.TOP)
		for c in colors:
			b = Tk.Button(bg,background=c)
			b.pack(side=Tk.LEFT)
			
		label = Tk.Label(charactersFrame,text="Colors")
		label.pack(side=Tk.TOP)
		col = Tk.Frame(charactersFrame)
		col.pack(side=Tk.TOP)
		for i,c in enumerate(DRAWABLE_CHARACTERS):
			l = Tk.Label(col,text=c)
			l.grid(column=int(i%16),row=int(i/16))


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

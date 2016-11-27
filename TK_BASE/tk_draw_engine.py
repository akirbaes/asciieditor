# /usr/bin/env python 3
# -*- coding: utf-8 -*-

try:
	import Tkinter as Tk
	from Tkinter import font
	from Tkinter import tkFileDialog as FileDialog
except ImportError:
	import tkinter as Tk
	from tkinter import font
	from tkinter import filedialog as FileDialog
from random import choice

root = Tk.Tk()
monofonts = []

for i in sorted(font.families()):
	if "mono" in i.lower():
		#print(i);
		monofonts.append(i)
		
fh = 20
monofont = font.Font(family="lucida console",size = -fh)
fw = monofont.measure("M")
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
curfg = "orange" #16
curbg = "tomato" #8

tool = "Point"

class App:
	def __init__(self,master):
		
		self.currentFGButton = None
		self.currentBGButton = None
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
		self.toolsFrame.pack(side=Tk.TOP,fill=Tk.BOTH,expand=True)
		self.setTools(self.toolsFrame)

		self.displayFrame = Tk.Frame(mainFrame)
		self.displayFrame.pack(side=Tk.LEFT)
			
		self.canvas = Tk.Canvas(self.displayFrame, width=FW*CW, height=FH*CH)
		self.canvas.pack()
		
		self.canvas_drawing = canvasManager(self.canvas)
		self.drawing_area = drawingArea(self.canvas_drawing)
		self.canvas_drawing.addListerner(self.drawing_area)
		
		self.setMenu(master)
		
	def setMenu(self,root):
		self.menubar = Tk.Menu(root)
		###http://tkinter.unpythonic.net/wiki/tkFileDialog
		def saveFile():
			filename = FileDialog.asksaveasfilename() #only receives the filename
		def saveAs():
			pass
			#file = FileDialog.asksaveasfile(mode='w') #already creates it
		def open():
			filename = FileDialog.askopenfilename() #plural is possible
			if(filename in self.recent_files):
				self.recent_files.remove(filename)
				self.recent_files.append("")
			self.recent_files = [filename]+self.recent_files[:-1]
			#file = FileDialog.askopenfile(mode='r')
			#filename = FileDialog.askopenfilename() #plural is possible
		self.recent_files=[""]*15
		self.menu_recent=[]
		def openRecent(number):
			def openR():
				filename = self.recent_files[number]
				#print("OpenR",number,"'"+filename+"'")
				if(filename!=""):
					if(filename in self.recent_files):
						self.recent_files.remove(filename)
						self.recent_files.append("")
					self.recent_files = [filename]+self.recent_files[:-1]

			return openR
			
		self.menubar.add_command(label="New")
		self.menubar.add_command(label="Open", command=open)
		
		def updatem():
			for i in range(15):
				self.recentmenu.entryconfigure(i, label="["+str(i).zfill(2)+"]: "+(self.recent_files[i] or "-- No entry here --"))
		
		self.recentmenu = Tk.Menu(self.menubar, tearoff=0, postcommand=updatem)
		for i in range(15):
			self.recentmenu.add_command(command=openRecent(i))
		#updatem()
		self.menubar.add_cascade(label="▼Open recent",menu=self.recentmenu)
		
		self.menubar.add_command(label="Save", command=saveFile)
		self.menubar.add_command(label="Save as", command=saveAs)
		self.menubar.add_separator()
		self.menubar.add_command(label="Quit", command=root.quit)

		# display the menu
		root.config(menu=self.menubar)
		
	def setTools(self,toolsFrame):
		def changeTool(newtool):
			def ct():
				global tool
				tool= newtool
				for button in self.allTools:
					if(button.cget("text")==tool):
						button.config(state="disabled")
						#print(tool,"is active")
					else:
						button.config(state="normal")
						
						
			return ct
		self.drawTool = Tk.Button(toolsFrame,text="Point", 
			command = changeTool("Point"),state="disabled")
		self.drawTool.pack(side=Tk.LEFT,anchor = "w")
		self.allTools.append(self.drawTool)
		#when click releasing, put selected character
		#click dragging: lines characters?
		#depending on drag direction and distance, different "hard to reach" characters
		#right click copies characters
		#right drag: selection
		#hover: can type
		
		#TOOL: pixel-mode
		self.drawTool = Tk.Button(toolsFrame,text="Pixel", 
			command = changeTool("Pixel"))
		self.drawTool.pack(side=Tk.LEFT,anchor = "w")
		self.allTools.append(self.drawTool)
		#Drag for up/down half pixels, or for tone pixels (sides)
		#Right click behaves like Point
		
		self.drawTool = Tk.Button(toolsFrame,text="Line", 
			command = changeTool("Line"))
		self.drawTool.pack(side=Tk.LEFT,anchor = "w")
		self.allTools.append(self.drawTool)
		#when dragging, draw lines diags, because they are difficult to reach normally?
		
		self.drawTool = Tk.Button(toolsFrame,text="Select", 
			command = changeTool("Select"))
		self.drawTool.pack(side=Tk.LEFT,anchor = "w")
		self.allTools.append(self.drawTool)
		#same as Point right click, but with left click and more options?
		
		#when on, advances automatically. Should be a switch instead of a tool?
		
		self.drawTool = Tk.Button(toolsFrame,text="Recolor", 
			command = changeTool("Recolor"))
		self.drawTool.pack(side=Tk.LEFT,anchor = "w")
		self.allTools.append(self.drawTool)
		#when on, typing a character only changes the character and not the color
		#and click releasing changes the color but not the character
		#and click dragging changes the color as well instead of doing lines
		
		#Action: check if right tool otherwise unpressed
		
		
		#Click Release:
		#-Point (current char)
		#-Recolor (current color)
		#-Start text?
		#Cursor mode: set cursor
		
		#Click Drag
		#-Line chars
		#-Pixel chars
		#-Left select (shapes?)
		#-Recolor (current color)
		#-Box (char mode, rectangle1, rectangle2)
		
		#Type
		#Cursor mode: type at cursor
		#Text mode: type and advance mode
		#Default: put char
		#Recolor: replace only char

		
		#Right click
		#-Select copy of char
		
		#Right drag:
		#-Instant selection
		#-Recolor: replace only char? Or instant selection as well?
		
		
		highlight = Tk.Label(toolsFrame,text="[◙]")
		highlight.pack(side=Tk.RIGHT,anchor = "e")
		def setAllColor(event):
			self.canvas_drawing.showAllColors(True)
		def unsetAllColor(event):
			self.canvas_drawing.showAllColors(False)
		highlight.bind("<Enter>", setAllColor)
		highlight.bind("<Leave>", unsetAllColor)
		
		highlight = Tk.Label(toolsFrame,text="[a]")
		highlight.pack(side=Tk.RIGHT,anchor = "e")
		def setAllChars(event):
			self.canvas_drawing.showAllChars(True)
		def unsetAllChars(event):
			self.canvas_drawing.showAllChars(False)
		highlight.bind("<Enter>", setAllChars)
		highlight.bind("<Leave>", unsetAllChars)

		self.gridset = False
		self.gridbutton = Tk.Button(toolsFrame,text="Grid")
		def showgrid():
			self.gridset = not self.gridset
			self.canvas_drawing.showOutlines(self.gridset)
			if(self.gridset):
				self.gridbutton.config(relief=Tk.SUNKEN)
			else:
				self.gridbutton.config(relief=Tk.RAISED)
		self.gridbutton.config(command = showgrid)
		self.gridbutton.pack(side=Tk.RIGHT,anchor = "w")
		
		self.textset = False
		self.textbutton = Tk.Button(toolsFrame,text="Text")
		def textMode():
			self.textset = not self.textset
			self.canvas_drawing.textmode(self.textset)
			if(self.textset):
				self.textbutton.config(relief=Tk.SUNKEN)
			else:
				self.textbutton.config(relief=Tk.RAISED)
		self.textbutton.config(command = textMode)
		self.textbutton.pack(side=Tk.RIGHT,anchor = "w")
		
		
	def setCharacters(self,charactersFrame):
		global curbg
		global curfg
		
		label = Tk.Label(charactersFrame,text="Foreground")
		label.pack(side=Tk.TOP)
		fg1 = Tk.Frame(charactersFrame)
		fg1.pack(side=Tk.TOP)
		
		def gensetfg(c,b):
			def setfg():
				global curfg; 
				curfg=c; 
				if(self.currentFGButton!=None):
					self.currentFGButton.config(state="normal",relief="raised")
				self.currentFGButton=b
				b.config(state="disabled",relief="ridge")
			return setfg
			
		def gensetbg(c,b):
			def setbg():
				global curbg; 
				curbg=c; 
				if(self.currentBGButton!=None):
					self.currentBGButton.config(state="normal",relief="raised")
				self.currentBGButton=b
				b.config(state="disabled",relief="ridge")
			return setbg
		
		for c in colors:
			#print("Curfg:",curfg,"Put c",c)
			b = Tk.Button(fg1,background=c,borderwidth=5)
			b.config(command = gensetfg(c,b))
			b.pack(side=Tk.LEFT)
			if(c=="gainsboro"):
				b.invoke()
		fg2 = Tk.Frame(charactersFrame)
		fg2.pack(side=Tk.TOP)
		for c in colors2:
			b = Tk.Button(fg2,background=c,borderwidth=5)
			b.config(command = gensetfg(c,b))
			b.pack(side=Tk.LEFT)
		
		label = Tk.Label(charactersFrame,text="Background")
		label.pack(side=Tk.TOP)
		bg = Tk.Frame(charactersFrame)
		bg.pack(side=Tk.TOP)
		for c in colors:
			b = Tk.Button(bg,background=c,borderwidth=5)
			b.config(command = gensetbg(c,b))
			b.pack(side=Tk.LEFT)
			
			if(c=="black"):
				b.invoke()
				
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
		self.canvas_mx = 0;
		self.canvas_my = 0;
		self.colorsbackup = []
		self.charsbackup = []
		self.istextmode = False
		
		self.canvas = canvas
		self.canvas.config(highlightthickness=0)
		self.c = canvas
		self.wv = FW
		self.hv = FH
		self.listener = None;
		hv = self.hv
		wv = self.wv
		self.bg = [[None]*CH for i in range(CW)]
		self.fg = [[None]*CH for i in range(CW)]
		#self.c.create_rectangle(((0,0),(CW*FW,CH*FH)),fill="red")
		for i in range(CW):
			for j in range(CH):
				p1 = (i*wv,j*hv)
				bbox = (p1,(i*wv+wv,j*hv+hv))
				self.bg[i][j] = self.c.create_rectangle(bbox,outline="dark slate gray",width=0,fill="black")
				self.fg[i][j] = self.c.create_text(p1,anchor="nw",font = monofont)
				
		self.selectx = 0;
		self.selecty = 0;
		self.selection = []
		self.selecting = False;
		self.typing = False;
		
		canvas.bind("<Enter>", lambda event: canvas.focus_set())
				
		def clickevent(event):
			self.canvas.focus_set()
			self.getEvent(event.x,event.y)
		canvas.bind("<Button-1>", clickevent)
		
		def mmovevent(x,y):
			def mmove(event):
				self.warpMouse(x,y)
			return mmove
		canvas.bind("<Left>", mmovevent(-1,0))
		canvas.bind("<Right>", mmovevent(1,0))
		canvas.bind("<Up>", mmovevent(0,-1))
		canvas.bind("<Down>", mmovevent(0,1))
		
		def updatemousepos(event):
			self.canvas_mx = event.x;
			self.canvas_my = event.y;
		canvas.bind("<Motion>", updatemousepos)
		#root.winfo_pointerxy()
		
		def typeachar(event):
			if(event.char!=""):
				#print(event.keysym)
				char = event.char;
				if(event.keysym=="BackSpace" or event.keysym=="Delete"):
					char=" "
				if(event.keysym=="Return"):
					char = None
				x=event.x
				y=event.y
				
				if(event.keysym=="BackSpace"):
					x-=fw
				if(x>0 and y>0 and x<cw*fw and y<ch*fh):
					if(event.keysym!="Return"):
						self.listener.typechar(int(x/fw),int(y/fh),char)
					if(self.istextmode):
						if(event.keysym=="BackSpace"):
							self.warpMouse(-1,0)
						elif(event.keysym=="Return"):
							self.warpMouse(-1,1)
						
						else:
							self.warpMouse(1,0)
		canvas.bind("<Key>",typeachar)
		
	def textmode(self,textset):
		self.istextmode = textset
		
	def showOutlines(self,do):
		for line in self.bg:
			for elem in line:
				self.c.itemconfig(elem, width=do)
	
	def showAllChars(self,do):
		if(do and len(self.colorsbackup)==0) or ((not do) and len(self.colorsbackup)!=0):
			for i,line in enumerate(self.fg):
				for j,fgpart in enumerate(line):
					bgpart = self.bg[i][j]
					if(do):
						col = self.c.itemcget(fgpart, "fill"), self.c.itemcget(bgpart, "fill")
						self.colorsbackup.append(col)
						self.c.itemconfig(fgpart, fill="white")
						self.c.itemconfig(bgpart, fill="black")
					else:
						col = self.colorsbackup.pop(0)
						self.c.itemconfig(fgpart, fill=col[0])
						self.c.itemconfig(bgpart, fill=col[1])
		
	def showAllColors(self,do):
		if(do and len(self.charsbackup)==0) or ((not do) and len(self.charsbackup)!=0):
			for line in self.fg:
				for elem in line:
					if(do):
						char = self.c.itemcget(elem, "text")
						self.charsbackup.append(char)
						self.c.itemconfig(elem, text="•")
					else:
						char = self.charsbackup.pop(0)
						self.c.itemconfig(elem, text=char)
						
	def putchar(self,x,y,char=None,fg=None,bg=None):
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
		
	def warpMouse(self,x,y):
		dx = x*fw
		dy = y*fh
		self.canvas.event_generate('<Motion>', warp=True, x=self.canvas_mx+dx,
			y=self.canvas_my+dy)
class drawingArea():
	#Just the areas, like my old ones
	def __init__(self,canvas):
		self.zones = []
		self.drawCanvas = canvas
		self.dc = canvas
		for i in range(min(CH-2,CW-2,25)):
			self.dc.putchar(i,i,chr(ord("a")+i),"white","red")
		
	def move(self,x,y):
		self.x=x
		self.y=y
	def draw():
		pass
	def click(self,x,y,tool):
		if(tool==0):
			#print("FG:",curfg,"BG:",curbg)
			self.dc.putchar(x,y,choice("▀▄█░▒▓"),curfg,curbg)
		pass
		
	def typechar(self,x,y,char):
		if(char!=""):
			self.dc.putchar(x,y,char,curfg,curbg)

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
	exit(1) #quit anyway

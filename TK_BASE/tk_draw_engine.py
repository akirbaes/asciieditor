# /usr/bin/env python 3
# -*- coding: utf-8 -*-

try:
	#Python 3
	import Tkinter as Tk
	from Tkinter import font
	from Tkinter import tkFileDialog as FileDialog
	from Tkinter import *
except ImportError:
	#Python 2
	import tkinter as Tk
	from tkinter import font
	from tkinter import filedialog as FileDialog
	from tkinter import *
try:
	from random import choice
	from os import name as osname
	import os

	import utilities
	from constants import *
	from interface_constants import *

	from Tooltip import CreateToolTip
	from save_system import SaveSystem
except ImportError:
	print("Could not import important files")
	raise

from drawingarea import *
	
root = Tk()

save_engine = SaveSystem()
root.title(save_engine.get_current_filename())
#Note: in the future, set the filename to the IMAGE to allow opening several

import sys
flush = sys.stdout.flush

if(osname == "nt"):
	fh = 20
	monofont = font.Font(family="lucida console",size = -fh)
else:
	fh = 25
	monofont = font.Font(family="Ubuntu Mono",size = -fh)
fw = monofont.measure("M")
FH=fh
FW=fw

#black,red,green,yellow,blue,purple,cyan,white
#light with 1

curchar = StringVar()
curchar.set("b")

curfg = StringVar()
curfg.set(LTWHITE)
curbg = StringVar()
curbg.set(BLACK)


from Tools import *

curtool = StringVar()
curtool.set("Pen")
#"Linebits"

def init_pencilcolor(masterframe):
	topFrame = Frame(masterframe)
	

class App:
	def __init__(self,master):
		self.allTools = []
		#MAINFRAME
		mainFrame = Frame(master)
		mainFrame.pack(fill=BOTH,expand=True)


		#PARAMETERS FRAME on the right    self.parametersFrame
		
		self.parametersFrame = Frame(mainFrame,bg="pink")
		self.parametersFrame.pack(side=RIGHT,anchor="e",fill=BOTH)
		
		self.charactersFrame = Frame(self.parametersFrame)
		self.charactersFrame.pack(side=TOP,anchor="n")
		self.setColorFunctions(self.charactersFrame)
		
		self.toolsFrame = Frame(mainFrame)
		self.toolsFrame.pack(side=TOP,fill=BOTH,expand=True)

		self.displayFrame = Frame(mainFrame)
		self.displayFrame.pack(side=TOP,fill=BOTH,expand=True)
			
		self.canvas = Canvas(self.displayFrame, width=FW*CW, height=FH*CH)
		self.canvas.pack(side=TOP)
		
		self.drawing = Drawing()
		self.canvas_drawing = DrawingManager(self.canvas, self.drawing)
		
		self.drawing.set_canvas(self.canvas_drawing)
		#self.canvas_drawing.set_drawing(self.drawing)
		# self.canvas_drawing.addListerner(self.drawing_area)
		
		self.setTools(self.toolsFrame)
		self.setMenu(master)
		
	def setMenu(self,root):
		#Menu with several options
		self.menubar = Menu(root)
		###http://tkinter.unpythonic.net/wiki/tkFileDialog
		
		def new():
			savename = "newfile_"+utilities.gen_time()+".ansi"
			root.title(savename)
			save_engine.set_current_filename(savename)
			#pushName(savename) #no because not saved yet
			#self.canvas_drawing.empty()
		def open():
			filename = FileDialog.askopenfilename(defaultextension="txt",filetypes=(("ANSI text",".ansi"),("Plain text",".txt"))) #plural is possible
			if(filename):
				self.loadDrawing(filename)
				save_engine.pushName(filename)
				save_engine.set_current_filename(filename)
				root.title(filename)
			#file = FileDialog.askopenfile(mode='r')
			#filename = FileDialog.askopenfilename() #plural is possible
		self.menu_recent=[]
		def openRecent(number):
			def openR():
				filename = save_engine.get_recent_filename(number)
				#print("OpenR",number,"'"+filename+"'")
				if(filename!=""):
					self.loadDrawing(filename)
					save_engine.pushName(filename)
					save_engine.set_current_filename(filename)
					root.title(filename)
			return openR
		def saveFile():
			self.saveDrawing(save_engine.get_current_filename())
			save_engine.pushName()
		def saveAs():
			filename = FileDialog.asksaveasfilename(defaultextension=".ansi",
				filetypes=(("ANSI text",".ansi"),("Plain text",".txt")),
				initialfile=save_engine.get_current_filename()) #only receives the filename
			print(filename)
			if(filename):
				save_engine.set_current_filename(filename)
				root.title(filename)
				saveFile()
			#file = FileDialog.asksaveasfile(mode='w') #already creates it
			
		def updatem():
			for i in range(15):
				self.recentmenu.entryconfigure(i, label="["+str(i).zfill(2)+"]: "+(save_engine.get_recent_filename(i) or "-- No entry here --"))
		
		self.recentmenu = Menu(self.menubar, tearoff=0, postcommand=updatem)
		for i in range(15):
			self.recentmenu.add_command(command=openRecent(i))
		#updatem()
		
		
		self.menubar.add_command(label="New", command=new)
		self.menubar.add_command(label="Open", command=open)
		self.menubar.add_cascade(label="▼Open recent",menu=self.recentmenu)
		self.menubar.add_command(label="Save", command=saveFile)
		self.menubar.add_command(label="Save as", command=saveAs)
		self.menubar.add_separator()
		self.menubar.add_command(label="Quit", command=root.quit)

		# display the menu
		root.config(menu=self.menubar)
		
		
	def saveDrawing(self,savename):
		#savename
		#mode color or not
		if(savename[-4:]==".txt"):
			data = self.canvas_drawing.repr_data_bw()
			print("Note: saving as plain .txt will not save color informations.")
		else:
			data = self.canvas_drawing.repr_data()
		saveplace = open(savename,"w",encoding="utf-8")
		saveplace.write(data)
		saveplace.close()
	
	
	
	def loadDrawing(self,filename):
		file = open(filename,"r",encoding="utf-8")
		string = file.read()
		file.close()
		data = utilities.ansistring_to_charcolorindextriplet(string)
		self.canvas_drawing.load_data(data)
		
	def setTools(self,toolsFrame):
		# # self.button_oldcolor = None
		# # def changeTool(newtool):
			# # def ct():
				# # global tool
				# # tool= newtool
				# # for button in self.allTools:
					# # if(self.button_oldcolor==None):
						# # self.button_oldcolor = button.cget("bg")
						
					# # if(button.cget("text")==tool):
						# # button.config(state="disabled")
						# # button.config(bg="blue")
						# # #print(tool,"is active")
					# # else:
						# # button.config(state="normal")
						# # button.config(bg=self.button_oldcolor)
						
						
			# # return ct
		# # self.drawTool = Button(toolsFrame,text="Linebits", 
		# # command = changeTool("Linebits")) #,state="disabled"
		# # self.drawTool.pack(side=LEFT,anchor = "w")
		# # self.allTools.append(self.drawTool)
		#when click releasing, put selected character
		#click dragging: lines characters?
		#depending on drag direction and distance, different "hard to reach" characters
		#right click copies characters
		#right drag: selection
		#hover: can type
		#when dragging, draw lines diags, because they are difficult to reach normally?
		# # self.drawTool.invoke()
		
		# # self.drawTool = Button(toolsFrame,text="SelectBy", 
		# # command = changeTool("SelectBy"))
		# # self.drawTool.pack(side=LEFT,anchor = "w")
		# # self.allTools.append(self.drawTool)
		#same as Point right click, but with left click and more options?
		
		#TOOL: pixel-mode
		# # self.drawTool = Button(toolsFrame,text="Pixels", 
		# # command = changeTool("Pixels"))
		# # self.drawTool.pack(side=LEFT,anchor = "w")
		# # self.allTools.append(self.drawTool)
		#Drag for up/down half pixels, or for tone pixels (sides)
		#Right click behaves like Point
		
		# self.drawTool = Button(toolsFrame,text="Rectangle", 
		# command = changeTool("Rectangle"))
		# self.drawTool.pack(side=LEFT,anchor = "w")
		# self.allTools.append(self.drawTool)
		#Draw a rectangle of given char
		
		#when on, advances automatically. Should be a switch instead of a tool?
		
		# # self.drawTool = Button(toolsFrame,text="Box", 
		# # command = changeTool("Box"))
		# # self.drawTool.pack(side=LEFT,anchor = "w")
		# # self.allTools.append(self.drawTool)
		
		
		# # self.drawTool = Button(toolsFrame,text="Box2", 
		# # command = changeTool("Box2"))
		# # self.drawTool.pack(side=LEFT,anchor = "w")
		# # self.allTools.append(self.drawTool)
		
		
		#when on, typing a character only changes the character and not the color
		#and click releasing changes the color but not the character
		#and click dragging changes the color as well instead of doing lines
		
		#Action: check if right tool otherwise unpressed
		
		
		# # self.drawTool = Button(toolsFrame,text="Paint", 
		# # command = changeTool("Paint"))
		# # self.drawTool.pack(side=LEFT,anchor = "w")
		# # self.allTools.append(self.drawTool)
		
		
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
		
		highlight = Label(toolsFrame,text="[◙]")
		highlight.pack(side=RIGHT,anchor = "e")
		def setAllColor(event):
			self.canvas_drawing.showAllColors(True)
		def unsetAllColor(event):
			self.canvas_drawing.showAllColors(False)
		highlight.bind("<Enter>", setAllColor)
		highlight.bind("<Leave>", unsetAllColor)
		
		
		CreateToolTip(highlight,"Show colors")
		
		highlight = Label(toolsFrame,text="[a]")
		highlight.pack(side=RIGHT,anchor = "e")
		def setAllChars(event):
			self.canvas_drawing.showAllChars(True)
		def unsetAllChars(event):
			self.canvas_drawing.showAllChars(False)
		highlight.bind("<Enter>", setAllChars)
		highlight.bind("<Leave>", unsetAllChars)
		
		CreateToolTip(highlight,"Show chars")

		goptionsFrame = Frame(toolsFrame)
		goptionsFrame.pack(side=RIGHT,anchor = "w")

		self.gridset = False
		self.gridbutton = Button(goptionsFrame,text="Grid")
		def showgrid():
			self.gridset = not self.gridset
			self.canvas_drawing.showOutlines(self.gridset)
			if(self.gridset):
				self.gridbutton.config(relief=SUNKEN)
			else:
				self.gridbutton.config(relief=RAISED)
		self.gridbutton.config(command = showgrid)
		self.gridbutton.pack(side=BOTTOM,anchor = "w")
		
		
		self.textset = False
		self.textbutton = Button(goptionsFrame,text="Ins.")
		def textMode():
			self.textset = not self.textset
			self.canvas_drawing.textmode(self.textset)
			if(self.textset):
				self.textbutton.config(relief=SUNKEN)
			else:
				self.textbutton.config(relief=RAISED)
		self.textbutton.config(command = textMode)
		self.textbutton.pack(side=BOTTOM,anchor = "w")
		self.textbutton.invoke()
		CreateToolTip(self.textbutton,"Insert mode on/off")
		
		#Modification modes
		modeFrame = Frame(toolsFrame)
		global dochar,dofg,dobg
		dochar = IntVar()
		dofg = IntVar()
		dobg = IntVar()
		dochar.set(1)
		dofg.set(1)
		dobg.set(1)
		fgm = Checkbutton(modeFrame,text="[FG]",var=dofg)
		CreateToolTip(fgm,"Modify Foreground color when drawing")
		bgm = Checkbutton(modeFrame,text="[BG]",var=dobg)
		CreateToolTip(bgm,"Modify Background color when drawing")
		chm = Checkbutton(modeFrame,text="[Ch]",var=dochar)
		CreateToolTip(chm,"Modify Characters when drawing")
		fgm.select()
		bgm.select()
		chm.select()
		
		fgm.pack(side=TOP)
		bgm.pack(side=TOP)
		chm.pack(side=TOP)
		modeFrame.pack(side=RIGHT)
		
		
		
	def setColorFunctions(self,charactersFrame):
		
		topFrame = Frame(charactersFrame)
		topFrame.pack(side=TOP)
		
		def validchar(char, type):
			#Replace goes trough: delete (0) then fill (1)
			#print(type, repr(char))
			#flush()
			return len(char) < 2 and char in DRAWABLE_CHARACTERS
		#https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter/35554720#35554720
		#topFrame.validchar = validchar
		#vcmd = topFrame.register(topFrame.validchar,'%P')
		charEntry = Entry(topFrame,textvariable = curchar, width = 1, validate = "all", font = monofont)
		charEntry['validatecommand'] = (charEntry.register(validchar), '%P', '%d')
		charEntry.pack(side=LEFT)
		
		def reverse_color(color):
			#https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
			return "#%06x"%(int("FFFFFF",16)-int(color[1:],16))
		
		fgButton = Button(topFrame,text=" ",background=curfg.get(),borderwidth=2, width = 1, height = 1)
		fgButton.selector = None
		def createFGSelector():
			parent = fgButton
			if(parent.selector == None or not parent.selector.winfo_exists()):
				selector = Toplevel(parent, borderwidth=2, relief="groove")
				selector.focus_set()
				parent.selector = selector
				selector.wm_overrideredirect(True)
				def delete(*args):
					selector.destroy()
				selector.bind("<FocusOut>",delete)
				
				label = Label(selector,text="Foreground [x]")
				label.pack(side=TOP,fill="x")
				fg1 = Frame(selector)
				fg1.pack(side=TOP)
				label.bind("<1>",delete)
			
				selector.currentFGButton = None
				def gensetfg(c,b):
					def setfg():
						curfg.set(c); 
						if(selector.currentFGButton!=None):
							selector.currentFGButton.config(state="normal",relief="raised",text=" ") #unselect
						selector.currentFGButton=b
						b.config(state="disabled",relief="ridge",text="X") #select
					return setfg
					
				
				for c in colors:
					#print("Curfg:",curfg,"Put c",c)
					b = Button(fg1,background=c,disabledforeground=reverse_color(c),borderwidth=2,text=" ", font = monofont) #creation 1
					b.config(command = gensetfg(c,b))
					b.pack(side=LEFT)
					if(c==curfg.get()):
						b.invoke()
						
				fg2 = Frame(selector)
				fg2.pack(side=TOP)
				for c in colors2:
					b = Button(fg2,background=c,disabledforeground=reverse_color(c),borderwidth=2,text=" ",font = monofont) #creation 2
					b.config(command = gensetfg(c,b))
					b.pack(side=LEFT)
					if(c==curfg.get()):
						b.invoke()
				selector.update()
				xx = min(root.winfo_rootx()+root.winfo_width()-selector.winfo_width(),
						parent.winfo_rootx()-parent.winfo_width()/2-selector.winfo_width()/2)
				selector.geometry(("+%d+%d")%(xx,parent.winfo_rooty()))
			else:
				selector = parent.selector
				selector.update()
				xx = min(root.winfo_rootx()+root.winfo_width()-selector.winfo_width(),
						parent.winfo_rootx()-parent.winfo_width()/2-selector.winfo_width()/2)
				selector.geometry(("+%d+%d")%(xx,parent.winfo_rooty()))
				
		def updateFGButton(*args):
			fgButton.config(background=curfg.get())
		curfg.trace_add("write",updateFGButton)
		fgButton.config(command=createFGSelector)
		fgButton.pack(side=LEFT)
		
			
			
		bgButton = Button(topFrame,background=curbg.get(),borderwidth=2, width = 1, height = 1)
		bgButton.selector = None
		def createBGSelector():
			parent = bgButton
			if(parent.selector == None or not parent.selector.winfo_exists()):
				selector = Toplevel(parent, borderwidth=2, relief="groove")
				selector.focus_set()
				parent.selector = selector
				selector.wm_overrideredirect(True)
				def delete(*args):
					selector.destroy()
				selector.bind("<FocusOut>",delete)
				
				selector.currentBGButton = None
				def gensetbg(c,b):
					def setbg():
						curbg.set(c); 
						if(selector.currentBGButton!=None):
							selector.currentBGButton.config(state="normal",relief="raised",text=" ") #unselect
						selector.currentBGButton=b
						b.config(state="disabled",relief="ridge",text="X") #select
					return setbg
				label = Label(selector,text="Background [x]")
				label.pack(side=TOP,fill="x")
				label.bind("<1>",delete)
				bg = Frame(selector)
				bg.pack(side=TOP)
				for c in colors:
					b = Button(bg,background=c,disabledforeground=reverse_color(c),borderwidth=2,text=" ",font = monofont) #creation
					b.config(command = gensetbg(c,b))
					b.pack(side=LEFT)
					
					if(c==curbg.get()):
						b.invoke()
				
				selector.update()
				xx = min(root.winfo_rootx()+root.winfo_width()-selector.winfo_width(),
						parent.winfo_rootx()-parent.winfo_width()/2-selector.winfo_width()/2)
				selector.geometry(("+%d+%d")%(xx,parent.winfo_rooty()))
			else:
				selector = parent.selector
				selector.update()
				xx = min(root.winfo_rootx()+root.winfo_width()-selector.winfo_width(),
						parent.winfo_rootx()-parent.winfo_width()/2-selector.winfo_width()/2)
				selector.geometry(("+%d+%d")%(xx,parent.winfo_rooty()))
		def updateBGButton(*args):
			bgButton.config(background=curbg.get())
		curbg.trace_add("write",updateBGButton)
		bgButton.config(command=createBGSelector)
		bgButton.pack(side=LEFT)
		
		
		def select_all(event):
			charEntry.selection_range(0, END)
		def focus(event):
			charEntry.focus()
		charEntry.bind("<FocusIn>", select_all)
		charEntry.bind("<Enter>", focus)
		charEntry.bind("<Key>", select_all)
		
		exampleLabel = Label(charactersFrame,textvariable=curchar,background=curbg.get(),foreground=curfg.get(),font=monofont,borderwidth=0)
		exampleLabel.pack(side=TOP)
		def updateExampleBG(*args):
			exampleLabel.config(background=curbg.get())
		def updateExampleFG(*args):
			exampleLabel.config(foreground=curfg.get())
		curfg.trace_add("write",updateExampleFG)
		curbg.trace_add("write",updateExampleBG)
		charEntry.update()
		cew = exampleLabel.winfo_width()
		ceh = exampleLabel.winfo_height()
		
		paletteButton = Button(charactersFrame,text="↓")
		paletteButton.pack(side=TOP)
		paletteFrame = Frame(charactersFrame,width=cew*8+4+8*4,height=ceh*8+4+8*4,relief="ridge",borderwidth=2)
		paletteFrame.pack(side=TOP)
		paletteFrame.pack_propagate(0)
		paletteFrame.grid_propagate(0)
		
		def paletteColor(parent,f,b,c):
			# f,b,c = fgvar.get(), bgvar.get(), charvar.get()
			#actually, use my own, made of a label, that can be selected without having focus, and switched 
			color_button = Label(parent,relief="solid",
				bg=b,fg=f,text=c,borderwidth=0,font=monofont,activebackground=reverse_color(b),activeforeground=reverse_color(f),
				highlightthickness=2,highlightcolor="red")
				
			number = len(parent.winfo_children())-1
			#color_button.pack(side=LEFT)
			color_button.grid(column=number%8, row=number//8)
			# print(number%8,number//8)
			flush()
			
			def delete(*args):
				color_button.destroy()
			color_button.bind("<Delete>", delete)
			def setColor(*args):
				curfg.set(f)
				curbg.set(b)
				curchar.set(c)
				color_button.focus_set()
				color_button.config(state=ACTIVE)
				#color_button.config(relief="sunken",borderwidth=2)
			color_button.bind("<1>",setColor)
			def leave(*args):
				color_button.config(state=NORMAL)
				#color_button.config(relief="sunken",borderwidth=0)
				pass
			color_button.bind("<Leave>",leave)
				
				
			
			
		def putIntoPalette():
			paletteColor(paletteFrame,curfg.get(),curbg.get(),curchar.get())
		paletteButton.config(command=putIntoPalette)
		
		
		"""
		label = Label(charactersFrame,text="Colors")
		label.pack(side=TOP)
		col = Frame(charactersFrame)
		col.pack(side=TOP)
		for i,c in enumerate(DRAWABLE_CHARACTERS):
			l = Label(col,text=c)
			l.grid(column=int(i%16),row=int(i/16))
		"""
class DrawingManager():
	#Hides the real canvas
	#For now it also holds the chars and colors data, but I have to separate view from data later on...
	def set_drawing(drawing):
		self.drawing = drawing
		#And redo the _init_ parts that require the drawing
	
	def __init__(self,canvas, drawing):
		self.showbox = None #later on I will need to "showbox" several characters instead of one
		self.canvas_mx = 0;
		self.canvas_my = 0;
		self.colorsbackup = []
		self.charsbackup = []
		self.istextmode = False
		
		self.current_tool = Pen(canvas,self)
		self.current_character_variables = (curfg, curbg, curchar)
		self.drawing = drawing
		self.canvas = canvas
		self.canvas.config(highlightthickness=0)
		self.c = canvas
		self.wv = FW
		self.hv = FH
		self.listener = None;
		self.bg = [[None]*CH for i in range(CW)]
		self.fg = [[None]*CH for i in range(CW)]
		
		self.clicktool = None
		self.clickx = -1
		self.clicky = -1
		self.c.create_rectangle(((0,0),(CW*FW,CH*FH)),fill="red")
		for i in range(CW):
			for j in range(CH):
				p1 = (i*FW,j*FH)
				bbox = (p1,(i*FW+FW,j*FH+FH))
				self.bg[i][j] = self.c.create_rectangle(bbox,outline="dark slate gray",width=0,fill=BLACK)
				self.fg[i][j] = self.c.create_text(p1,anchor="nw",font = monofont,fill=BLACK)
				
		self.selectx = 0;
		self.selecty = 0;
		self.selection = []
		self.selecting = False;
		self.typing = False;
		
		canvas.bind("<Enter>", lambda event: canvas.focus_set())
		
		def send_event(eventType):
			def act(event):
				layer = self.drawing.get_current_layer()
				self.current_tool.send_event(eventType, event, layer, self.wv, self.hv, (curfg, curbg, curchar))
			return act
		canvas.bind("<Button-1>", send_event("<Button-1>"))
		canvas.bind("<B1-Motion>", send_event("<B1-Motion>"))
		canvas.bind("<ButtonRelease-1>", send_event("<ButtonRelease-1>"))
		
		canvas.bind("<Button-3>", send_event("<Button-3>"))
		canvas.bind("<B3-Motion>", send_event("<B3-Motion>"))
		canvas.bind("<ButtonRelease-3>", send_event("<ButtonRelease-3>"))
		
		canvas.bind("<Key>", send_event("<Key>"))
		
		canvas.current_after = None
		# # def clickevent(event):
			# # self.canvas.focus_set()
			# # self.getEvent(event.x,event.y,"click")
		# # canvas.bind("<Button-1>", clickevent)
		# # def unclickevent(event):
			# # self.canvas.focus_set()
			# # self.getEvent(event.x,event.y,"unclick")
		# # canvas.bind("<ButtonRelease-1>", unclickevent)
		
		# # def rclickevent(event):
			# # self.getEvent(event.x,event.y,"rclick")
		# # canvas.bind("<Button-3>", rclickevent)
		# # def unrclickevent(event):
			# # self.getEvent(event.x,event.y,"unrclick")
		# # canvas.bind("<ButtonRelease-3>", unrclickevent)
		
		def mmovevent(x,y):
			def mmove(event):
				self.warpMouse(x,y)
			return mmove
		canvas.bind("<Left>", mmovevent(-1,0))
		canvas.bind("<Right>", mmovevent(1,0))
		canvas.bind("<Up>", mmovevent(0,-1))
		canvas.bind("<Down>", mmovevent(0,1))
		
		# # def updatemousepos(event):
			# # self.canvas_mx = event.x;
			# # self.canvas_my = event.y;
		# # canvas.bind("<Motion>", updatemousepos)
		#root.winfo_pointerxy()
		
		# # def typeachar(event):
			# # if(event.char!=""):
				# # #print(event.keysym)
				# # char = event.char;
				# # if(event.keysym=="BackSpace" or event.keysym=="Delete"):
					# # char=" "
				# # if(event.keysym=="Return"):
					# # char = None
				# # x=event.x
				# # y=event.y
				
				# # if(event.keysym=="BackSpace"):
					# # x-=fw
				# # if(x>0 and y>0 and x<cw*fw and y<ch*fh):
					# # if(event.keysym!="Return"):
						# # self.listener.typechar(int(x/fw),int(y/fh),char)
					# # if(self.istextmode):
						# # if(event.keysym=="BackSpace"):
							# # self.warpMouse(-1,0)
						# # elif(event.keysym=="Return"):
							# # self.warpMouse(-1,1)
						
						# # else:
							# # self.warpMouse(1,0)
		# # canvas.bind("<Key>",typeachar)
		
	def textmode(self,textset):
		self.istextmode = textset
		
	def showOutlines(self,do):
		for line in self.bg:
			for elem in line:
				self.c.itemconfig(elem, width=do)
				
	def empty(self):
		self.drawing.get_current_layer().remove_rect(0,0,80,20)
		# for i,line in enumerate(self.fg):
				# for j,fgpart in enumerate(line):
					# bgpart = self.bg[i][j]
					# self.c.itemconfig(fgpart, text=" ")
					# self.c.itemconfig(fgpart, fill=WHITE)
					# self.c.itemconfig(bgpart, fill=BLACK)
					

	def load_data(self,data):
		for i,line in enumerate(data):
			for j,elem in enumerate(line):
				if(elem!=None):
					fgc, bgc, nchar = elem
					if(i>=cw or j>=ch):
						break
					fgpart = self.fg[i][j]
					bgpart = self.bg[i][j]
					self.drawing.get_current_layer().put(i,j,(fgc,bgc,nchar))
					#self.c.itemconfig(fgpart, text=nchar)
					#self.c.itemconfig(fgpart, fill=fgc)
					#self.c.itemconfig(bgpart, fill=bgc)
						
	def load_positional_data(self,data):
		for draw in data:
			x,y, chardata = draw
			if(chardata!=None):
				fgc, bgc, nchar = chardata
			
			fgpart = self.fg[x][y]
			bgpart = self.bg[x][y]
			self.c.itemconfig(fgpart, text=nchar)
			self.c.itemconfig(fgpart, fill=fgc)
			self.c.itemconfig(bgpart, fill=bgc)
					
	def showAllChars(self,do):
		if(do and len(self.colorsbackup)==0) or ((not do) and len(self.colorsbackup)!=0):
			for i,line in enumerate(self.fg):
				for j,fgpart in enumerate(line):
					bgpart = self.bg[i][j]
					if(do):
						col = self.c.itemcget(fgpart, "fill"), self.c.itemcget(bgpart, "fill")
						self.colorsbackup.append(col)
						self.c.itemconfig(fgpart, fill=WHITE)
						self.c.itemconfig(bgpart, fill=BLACK)
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
						
	# def condputchar(self,x,y,char=None,fg=None,bg=None):
		# self.putchar(x,y,
				# (dochar.get() and char) or None,
				# (dofg.get() and fg) or None,
				# (dobg.get() and bg) or None)
	# def putchar(self,x,y,char=None,fg=None,bg=None):
		# print(char,fg,bg)
		# index = self.fg[x][y]
		# if(fg!=None):
			# self.c.itemconfig(index, fill=fg)
			
		# if(char!=None):
			# self.c.itemconfig(index, text=char[0])
			
		# index = self.bg[x][y]
		# if(bg!=None):
			# self.c.itemconfig(index, fill=bg)
	
	def getEvent(self,x,y,e):
		print("getEvent called - should not be")
		return
		#print("received event in",x,y)
		#transforms the event in X, Y, tool
		#and sends it to drawingArea which will send it back
		
		# # if(self.listener!=None):
			# # if e=="click":
				# # #Start showing a char even if not moved
				# # self.clicktool = tool
				# # self.clickx = x
				# # self.clicky = y
			# # elif e=="unclick":
				# # cc=0
				# # if(self.clicktool=="Linebits"):
					# # cc = ("`'´","-"+"+"+"-","_//|\\\\_")
				# # elif(self.clicktool=="Pixels"):
					# # cc = (" ▀▀▀▀▀▀▀▀▀█"," ░░░▒▓▓▓█"," ▄▄▄▄▄▄▄▄▄█")
				# # elif(self.clicktool=="Box2"):
					# # cc = ("║","═╝╝╝║╚╚╚═","═╝╝╝╩╚╚╚═","═╣╣╬╠╠═","═╗╗╗╦╔╔╔═","═╗╗╗║╔╔╔═","║")
				# # elif(self.clicktool=="Box"):
					# # cc = ("│","┘┴└","┘┴└","─┤┤┼├├─","┐┬┌","┐┬┌","│")
				# # if(cc):
					# # dx = int(x/fw)-int(self.clickx/fw)
					# # dy = int(y/fh)-int(self.clicky/fh)
					# # #c = ═║╚╝╠╣╦╩╬■►◄↕↨↑↓→←∟↔▲▼
					# # h = int(len(cc)/2)
					# # choosey = min(len(cc)-1,max(0,h+dy))
					# # w = int(len(cc[choosey])/2)
					# # choosex = min(len(cc[choosey])-1,max(0,w+dx))
					
					# # print(dx,"->",choosex,"\n",dy,"->",choosey,"\n",cc[choosey][choosex])
					# # x=self.clickx
					# # y=self.clicky
					# # if(x>0 and y>0 and x<cw*fw and y<ch*fh):
						# # self.putchar(int(x/fw),int(y/fh),
							# # (dochar.get() and cc[choosey][choosex]) or None,
							# # (dofg.get() and curfg.get()) or None,
							# # (dobg.get() and curbg.get()) or None)
				# # else:
					# # if(x>0 and y>0 and x<cw*fw and y<ch*fh):
						# # self.listener.click(int(x/fw),int(y/fh),0)
			# # elif e=="rclick":
				# # if(x>0 and y>0 and x<cw*fw and y<ch*fh):
					# # fg,bg,c = self.getAt(int(x/fw),int(y/fh))
					# # curchar.set(c or " ")
					# # curbg.set(bg)
					# # curfg.set(fg)
				
	# # def getAt(self,x,y):
		# # return (self.c.itemcget(self.fg[x][y],"fill"),
				# # self.c.itemcget(self.bg[x][y],"fill"),
				# # self.c.itemcget(self.fg[x][y],"text"))
		
	# def addListerner(self,listener):
		# self.listener = listener;
		
	def warpMouse(self,x,y):
		dx = x*fw
		dy = y*fh
		self.canvas.event_generate('<Motion>', warp=True, x=self.canvas_mx+dx,
			y=self.canvas_my+dy)
				
	def repr_data(self):
		#to remade for drawingArea instead next [TODO]
		datatext = ""
		fg = None
		bg = None
		brightness = 0
		
		for j in range(CH):
			for i in range(CW):
				fgelem = self.fg[i][j]
				char = self.c.itemcget(fgelem, "text") or " "
				nfg = self.c.itemcget(fgelem, "fill") 
				bgelem = self.bg[i][j]
				nbg = self.c.itemcget(bgelem, "fill")
				
				nb = ""
				fgid = ""
				bgid = ""
				if(nfg!=fg and nfg!=None):
					fgid = str(utilities.FGCODE(nfg))
					fg=nfg
					if(nfg in colors2):
						if(brightness == 0):
							nb = "1"
							brightness = 1
					else:
						if(brightness == 1):
							nb = "22"
							brightness = 0
				if(nbg!=bg and nbg!=None):
					bgid = str(utilities.BGCODE(nbg))
					bg=nbg
				if(fgid or bgid or nb):
					datatext += ESC + "[" + (";".join((x for x in (nb,fgid,bgid) if x!=""))) + "m"
				datatext+=char[0]
			datatext+="\n"
		datatext+=ESC+"[0m"
		return datatext
		
	def repr_data_bw(self):
		#to remade for drawingArea instead next [TODO]
		#to add ansi color codes [TODO]
		datatext = ""
		
		for j in range(CH):
			for i in range(CW):
				elem = self.fg[i][j]
				char = self.c.itemcget(elem, "text") or " "
				datatext+=char[0]
			datatext+="\n"
		return datatext
	
	def redraw(self, positions = None):
		if(positions==None):
			self.load_data(self.drawing.get_current_stack().combine_layers())
		else:
			for position in positions:
				x,y = position
				chardata = self.drawing.get_current_stack().layers[0].get(x,y)
				
				self.load_positional_data([(x,y,chardata)])

app = App(root)
root.mainloop()
try:
	root.destroy() #if it wasn't already
except:
	exit(1) #quit anyway

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#asciieditorv2 : Save, Export, multi-draw
import pygcurse, pygame, sys
from pygame.locals import *
from time import sleep
import random, math
from colortext import *

DRAWABLE_CHARACTERS = u"""☺☻♥♦♣♠•○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~⌂ ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿıƒ‗─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬▀▄█░▒▓■   """

ZERO = 0 #normally in ascii the top corner has coordinates (1,1), 0 doesn't exist
#but pygcurse follows pygame
pygame.font.init()
MAIN_FONT = pygame.font.Font("unifont-7.0.03.ttf" ,16)  
#http://unifoundry.com/unifont.html 
#GNU General Public License


BLACK = (0,0,0)
LTBLACK = (128,128,128)
RED = (128,0,0)
LTRED = (255,0,0)
GREEN = (0,128,0)
LTGREEN = (0,255,0)
YELLOW = (128,128,0)
LTYELLOW = (255,255,0)
BLUE = (0,0,128)
LTBLUE = (0,0,255)
MAGENTA = (128,0,128)
LTMAGENTA = (255,0,255)
CYAN = (0,128,128)
LTCYAN = (0,255,255)
WHITE = (192,192,192)
LTWHITE = (224,224,224)

BACKGROUND_COLORS = (BLACK,RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE)
FOREGROUND_COLORS = (BLACK,RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE,\
					LTBLACK,LTRED,LTGREEN,LTYELLOW,LTBLUE,LTMAGENTA,LTCYAN,LTWHITE)

def BGCODE(color):
	index = BACKGROUND_COLORS.index(color)
	return str(index+40)
	
def FGCODE(color):
	index = FOREGROUND_COLORS.index(color)
	return str(index%8+30)

IW = IMAGE_WIDTH = 80
IH = IMAGE_HEIGHT = 24
DW = DRAWING_WIDTH = 80 #drawing area's width
DH = DRAWING_HEIGHT = 24 #drawing area's height
DX = DRAWING_X = 10
DY = DRAWING_Y = 10

MENU_X = ZERO
MENU_Y = ZERO
TOOLS_X = ZERO
TOOLS_Y = 3
TOOLS_HEIGHT = 30 #arbitrary ?
TOOLS_WIDTH = DRAWING_X -1 #drawing_x

IMAGE_TITLE_Y = MENU_Y+1 # and color to differenciate?
IMAGE_TITLE_X = DRAWING_X
ANIM_STRIP_X = DRAWING_X
ANIM_STRIP_Y = IMAGE_TITLE_Y +1
ANIM_STRIP_HEIGHT = DRAWING_Y - ANIM_STRIP_Y

MENU_WIDTH = DRAWING_WIDTH + DRAWING_X - MENU_X

COLORS_X = MENU_X + MENU_WIDTH +1
COLORS_Y = 1
COLORS_HEIGHT = 5 #? arbitrary

CHARA_X = COLORS_X
CHARA_Y = COLORS_Y + COLORS_HEIGHT

CHARA_WIDTH = 16
CHARA_HEIGHT = 3

PALETTE_X = COLORS_X
PALETTE_Y = CHARA_Y + CHARA_HEIGHT + 2

PALETTE_WIDTH = 16 #nothing to add?
PALETTE_HEIGHT = 16 #arrow, menu, msg

COLORS_WIDTH = PALETTE_WIDTH

VIEW_X = PALETTE_X
VIEW_Y = PALETTE_Y + PALETTE_HEIGHT +1 +3

VIEW_WIDTH = PALETTE_WIDTH
VIEW_HEIGHT = DRAWING_Y + DRAWING_HEIGHT - VIEW_Y 

INFOS_X = ZERO
INFOS_Y = DRAWING_Y + DRAWING_HEIGHT +1

WINDOW_HEIGHT = INFOS_Y +1
WINDOW_WIDTH = PALETTE_X + PALETTE_WIDTH +1


win = pygcurse.PygcurseWindow(WINDOW_WIDTH,WINDOW_HEIGHT)

TOOLSLIST = "PEN","SELECT","FILL","SELECOL","LINE"

cellx = 0
celly = 0

win.autoupdate = False
win.font = MAIN_FONT
cellw, cellh = win.cellwidth, win.cellheight
CW, CH = cellw, cellh


def pos_in_rect(px,py,x,y,w,h):
	return x<=px<x+w and y<=py<y+h

def xx(cellx):
	return cellx*CW

def yy(celly):
	return celly*CH

class CharaMatrix():
	def __init__(self,width,height,x=0,y=0):
		self.changed=False
		self.matrix = [[None]*height for p in range(width)]
		self.width=width
		self.height=height
		self.x=x
		self.y=y
		self.dirty = list()
		self.focus = False
		
	def put(self,data, x,y):
		if(pos_in_rect(x,y,0,0,self.width,self.height)):
			if(self.matrix[x][y]!=data):
				self.matrix[x][y]=data
				self.dirty.append((x,y))
		else:
			print("Put outside of rect",x,y,self.x,self.y,self.width,self.height)
			return False
		return True
		
	def select(self,x,y,w,h):
		ans=CharaMatrix(w,h)
		for i in range(w):
			for j in range(h):
				if(pos_in_rect(i,j,0,0,self.width,self.height)):
					ans.put(i,j,self.matrix[x+i][y+j])
				else:
					pass
					#outside, None by default
		return ans
		
	def rectangle(self,x1,y1,x2,y2,data,relative=True):
		x1,x2 = min(x1,x2),max(x1,x2)
		y1,y2 = min(y1,y2),max(y1,y2)
		
		for i in range(x1,x2,1):
			for j in range(y1,y2,1):
				self.put(i-(not relative)*self.x,j-(not relative)*self.y, data)
				
	def canvas(self,x1,y1,x2,y2,data):
		"""Empty rectangle"""
		x1,x2 = min(x1,x2),max(x1,x2)
		y1,y2 = min(y1,y2),max(y1,y2)
		
		for i in range(x1,x2,1):
			self.put(i,y1,data)
			self.put(i,y2,data)
			
		for j in range(y1,y2,1):
			self.put(x1,j, data)
			self.put(x2,j, data)
	
	def merge_show(self, other, x, y, transparent=None):
		for i,column in enumerate(other.get_matrix()):
			for j,char in enumerate(column):
				if(char!=transparent):
					self.put(x+i,y+j,char)
		
	def get_matrix(self):
		return self.matrix
		
	def get(self,x,y):
		if(pos_in_rect(x,y,0,0,self.width,self.height)):
			return self.matrix[x][y]
		else:
			return None
	
	def set_fg(self,x,y,color):
		a=get(x,y)
		if(a!=None):
			self.put(x,y,(color,a[1],a[2]))

	
	def set_bg(self,x,y,color):
		a=get(x,y)
		if(a!=None):
			self.put(x,y,(a[0],color,a[2]))
				
	def set_char(self,x,y,char):
		a=get(x,y)
		if(a!=None):
			self.put(x,y,(a[0],a[1],char))
				
	def line(self,x1,y1,x2,y2):
		pass
	def rotated(self,angle):
		pass
		#return a rotated one with nones. only for show, doesn't modify the original
	def update(self):
		self.changed=True
		
	def draw(self,win):
		x,y = self.x, self.y
		for i, line in enumerate(self.matrix):
			for j, char in enumerate(line):

				if(0<=x+i<WINDOW_WIDTH and 0<=y+j<WINDOW_HEIGHT): #if in window only
					if(char!=None and char[1]!=None):
						fg,bg,char=char
						win.putchar(char,x+i,y+j,fgcolor=fg,bgcolor=bg)
					else:
						win.putchar(None,x+i,y+j) #erase outside (if the square moved)
						#WRITE(SETXY(i+1,j+1)+" ")

	def refresh(self,win):
		x,y = self.x, self.y
		while self.dirty:
			i,j = self.dirty.pop()
			if(0<=x+i<WINDOW_WIDTH and 0<=y+j<WINDOW_HEIGHT): #if in window only
				data = self.get(i,j)
				if(data!=None and data[1]!=None): #if in this area only
					fg,bg,char = data
					win.putchar(char,x+i,y+j,fgcolor=fg,bgcolor=bg)
				else:
					win.putchar(None,x+i,y+j) #erase outside (if the square moved)

	
	def move(self,dx,dy):
		self.x+=dx
		self.y+=dy
		for i, line in enumerate(self.matrix):
			for j, elem in enumerate(line):
				if(self.get(i,j)!=self.get(i+dx,j+dy)):
					self.dirty.append((i-dx,j-dy))
					self.dirty.append((i,j))
		
		
	def export_ainsi(self):
		text_data=""
		for j in range(len(self.matrix[0])):
			for i in range(len(self.matrix)):
				char = self.matrix[i][j]
				if(char==None or None in char):
					data="\x1b[0m\x1b[1C" #reset color and jump one forward
				else:
					fg,bg,char = char
					if fg in BACKGROUND_COLORS: #dim version
						data="\x1b[22" #normal : dimmer on win32
					else:
						data="\x1b[1" #bold : bright
					data += ";" + FGCODE(fg) + ";" + BGCODE(bg) + "m" + char 
				text_data+=data
			if(j<len(self.matrix[0])-1):
				text_data+="\n"
		text_data+="\x1b[0m" #reset
		#print(text_data)
		return text_data
		
	def inside(self,px,py):
		return self.x <= px < self.x+self.width  and  self.y <= py < self.y+self.height
		
	def write(self,word,x,y,fgcolor=WHITE,bgcolor=BLACK):
		try:
			for i,l in enumerate(word):
				olddata = self.get(x+i,y)
				if(fgcolor == None):
					fgcolor = olddata[0]
				if(bgcolor == None):
					bgcolor = olddata[1]
				self.put((fgcolor,bgcolor,l),x+i,y)
		except Exception as e:
			print(e)
			
	def release_focus(self,x=0,y=0):
		self.focus=False
	def set_focus(self,x=0,y=0):
		self.focus=True
	def focus_update(self,x=0,y=0):
		pass
	def hover(self,x=0,y=0):
		pass
	def unhover(self,x=0,y=0):
		pass

	def set_rfocus(self,x=0,y=0):
		pass
	def release_rfocus(self,x=0,y=0):
		pass
	def rfocus_update(self,x=0,y=0):
		pass
	
	def set_mfocus(self,x=0,y=0):
		pass
	def release_mfocus(self,x=0,y=0):
		pass
	def mfocus_update(self,x=0,y=0):
		pass
		
	def update_ink(self):
		pass

class DrawingArea(CharaMatrix):
	
	def __init__(self,width=DW,height=DH,x=DX,y=DY):
		VISIBLE_WIDTH = VW = 80
		VISIBLE_HEIGHT = VH = 25
		
		CharaMatrix.__init__(self, width, height, x, y)
		self.drawing_mode = None
		self.previous_position = (-1,-1)
		self.drawing_position = (-1,-1) #position where pencil is
		self.overlay_character = None #character used by pencil
		self.is_visible=False
		

		self.view_x = 0
		self.view_y = 0
		if(width<VISIBLE_WIDTH):
			self.view_x = VISIBLE_WIDTH//2 - width//2
		if(height<VISIBLE_HEIGHT):
			self.view_y = VISIBLE_HEIGHT//2 - height//2 
			
			
	def draw_line(self,x,y,char):
		if(self.previous_position==(-1,-1)):
			self.previous_position = (x,y)
		x1,y1 = self.previous_position
		dx=x-x1
		dy=y-y1
		steps = max(abs(x-x1),abs(y-y1))+1
		
		for s in range(steps):
			i = x1 + float(dx)*s/steps
			j = y1 + float(dy)*s/steps
			self.put(char,int(round(i)), int(round(j)))
		"""
		for i in range(x1,x2,1):
			
			#for j in range(y1,y2,1):
				#self.put(char,i,j)
			j=round(float(i-x1)/(x2-x1)*(y2-y1))+y1
			#print(j)
			self.put(char,i,int(j))"""
		self.previous_position = (x,y)
				
	def set_focus(self,x,y):
		self.draw_line(x-self.x,y-self.x,ink1.get())
		self.refresh(win)
		#drawing.put((draw_fg, draw_bg, draw_char),cellx-DX,celly-DY)
		#drawing.refresh(win)

		
	def focus_update(self,x,y):
		self.draw_line(x-self.x,y-self.x,(ink1.get()))
		self.refresh(win)
		
	def release_focus(self,x,y):
		self.previous_position=(-1,-1)
			
class ToolsArea(CharaMatrix):
	def __init__(self,width = TOOLS_WIDTH, height = TOOLS_HEIGHT, x=TOOLS_X, y=TOOLS_Y):
		CharaMatrix.__init__(self,width,height,x,y)
		self.tools = TOOLSLIST
		for i,tool in enumerate(self.tools):
			self.write(tool,0,i*2,LTWHITE,LTBLACK)
		
class TintControlArea(CharaMatrix):
	def __init__(self):
		width=16
		height=4
		x=COLORS_X
		y=COLORS_Y
		CharaMatrix.__init__(self,width,height,x,y)
		self.write("Foreground",0,0,WHITE,BLACK)
		self.write("Background",0,2,WHITE,BLACK)
		
		self.update()
		self.current_focus=None
		
	def update_ink(self):
		self.update()
	
	def update(self,refresh=True):
		#print("updating",draw_fg, draw_bg, draw_char)
		
		for i,col in enumerate(FOREGROUND_COLORS):
			if(col==BLACK):
				self.put((WHITE,BLACK,"_"),0,1)
			else:
				self.put((col,BLACK,u"■"),i,1)
			if (ink1.get_fg() == col):
				self.put((LTWHITE,col,u"⌂"),i,1)
			#	self.put((col,WHITE,u"■"),i,1)
		
		for i,col in enumerate(BACKGROUND_COLORS):
			if(col==BLACK):
				self.put((WHITE,BLACK,"_"),0,3)
			else:
				self.put((col,BLACK,u"■"),i,3)
			if (ink1.get_bg() == col and draw_char!=None):
				self.put((LTWHITE,col,u"⌂"),i,3)
			"""	if(col==BLACK):
					self.put((LTWHITE,col,u"⌂"),i,4)
				else:
					self.put((BLACK,col,u"⌂"),i,4)"""
		self.put((LTBLACK,BLACK,u"×"),8,3)
		if(ink1.get_char()==None or ink1.get_bg() == None):
			self.put((BLACK,WHITE,u"×"),8,3)
		
		if(refresh):
			self.refresh(win)
			
					
	def set_focus(self,x,y):
		if(y-self.y==1):
			self.current_focus = 1
		elif(y-self.y>=3):
			self.current_focus = 2
		self.focus_update(x,y)
		
		
	def focus_update(self,x,y):
		x=x-self.x
		y=y-self.y
		if(self.current_focus==1):

			x=min(max(0,x),15)
			ink1.set_fg( FOREGROUND_COLORS[x] )
		elif(self.current_focus==2):
			
			x=min(max(0,x),8)
			if(x<8):
				ink1.set_bg( BACKGROUND_COLORS[x] )
			else:
				ink1.set_bg( None )
			
	def release_focus(self,x,y):
		self.current_focus = None
			
class MenuArea(CharaMatrix):
	def __init__(self):
		width = MENU_WIDTH
		height = 1
		x=MENU_X
		y=MENU_Y
		CharaMatrix.__init__(self,width,height,x,y)
		self.menu_things = "File","Edit","Effect","Options"
		self.areas=[]
		count=0
		for name in self.menu_things:
			self.write(name,count,0,fgcolor=(0,0,0),bgcolor=(128,128,128))
			count+=len(name)+1
			self.areas.append(count)
		#print(self.matrix)
			
class PaletteArea(CharaMatrix):
	def __init__(self,string=""):
		x=PALETTE_X
		y=PALETTE_Y
		width=PALETTE_WIDTH
		height=PALETTE_HEIGHT
		CharaMatrix.__init__(self,width,height,x,y)
		string=string.ljust(16*16)
		self.string=string
		self.select = None
		
		for i in range(16):
			for j in range(16):
				data = (WHITE,BLACK,string[i+j*16])
				self.put(data,i,j)
		self.modifiable=True
		self.color_only = False
		self.character_only = False
		self.cx = -1
		self.cy = -1
				
	def set_colorful(self):
		for i in range(16):
			for j in range(16):
				data = (FOREGROUND_COLORS[(7+i)%16],BACKGROUND_COLORS[(j)%8],self.string[i+j*16])
				self.put(data,i,j)
	
	def set_focus(self,x,y):
		ink1.set( self.get(x-self.x,y-self.y) or [None,None,None] )
		if(self.inside(x,y)):
			self.select = (x-self.x,y-self.y)
		
	def focus_update(self,x,y):
		pass
		
	def release_focus(self,x,y):
		print("release",x-self.x,y-self.y,self.inside(x,y), (self.select and self.get(*self.select)) or self.select, self.get(x-self.x,y-self.y))
		if(self.select and self.inside(x,y)):
			if (x-self.x,y-self.y) != self.select:
				data = self.get(*self.select)
				self.put(self.get(x-self.x,y-self.y),*self.select)
				self.put(data,x-self.x,y-self.y)
			self.select=None
			self.update_ink()
			self.refresh(win)
			
	def update_ink(self):
		for i,column in enumerate(self.matrix):
			for j,data in enumerate(column):
				if(data == ink1.get()):
					self.cx, self.cy = i, j
					return True
		self.cx,self.cy=-1,-1
		return False
		
	def show_cursor(self,screen):
		if(self.cx!=-1):
			screen.blit(tiny, (self.x*CW+self.cx*CW,self.y*CH+self.cy*CH) )
		
class Ink():
	def __init__(self,bgcolor=BLACK,fgcolor=WHITE,char=u"☺"):
		self.bgcolor=bgcolor
		self.fgcolor=fgcolor
		self.char=char
		self.notify_list= list()
		
	def update(self):
		for elem in self.notify_list:
			elem.update_ink()
			
	def set(self,data):
		if(type(data)==tuple):
			if(data!=(self.fgcolor,self.bgcolor,self.char)):
				self.fgcolor,self.bgcolor,self.char = data
				self.update()
		elif type(data)==unicode:
			if(self.char!=data):
				self.char=data
				self.update()
					
	def set_bg(self,bgdata):
		if(self.bgcolor!=bgdata):
			self.bgcolor=bgdata
			self.update()
	
	def set_fg(self,fgdata):
		if(self.fgcolor!=fgdata):
			self.fgcolor=fgdata
			self.update()
			
	def set_char(self,charadata):
		if(self.char!=chardata):
			self.char=chardata
			self.update()
			
	def get(self):
		if(self.char==None or self.bgcolor==None):
			return (None,None,None)
		else:
			return (self.fgcolor,self.bgcolor,self.char)
			
	def get_char(self):
		return self.char
		
	def get_bg(self):
		return self.bgcolor
		
	def get_fg(self):
		return self.fgcolor
		
	def notify(self,other):
		if not(other in self.notify_list):
			self.notify_list.append(other)
	
	def unnotify(self,other):
		if other in self.notify_list:
			self.notify_list.remove(other)
			
class CharacterSwitch(CharaMatrix):
	def __init__(self):
		x,y,width,height = CHARA_X, CHARA_Y, CHARA_WIDTH, CHARA_HEIGHT
		CharaMatrix.__init__(self,width,height,x,y)
		#should be
		#CHARA_WIDTH = 16
		#CHARA_HEIGHT = 5
		self.write(u"╔═╗",0,0)
		self.write(u"╚═╝",0,2)
		self.write(u"║",0,1)
		self.write(u"║",2,1)
		
		self.update()
		self.focus = 0
		self.palette = None
	def set_palette(self,palette):
		self.palette = palette
		
	def update(self,refresh=True):
		self.put(ink1.get(),1,1)
		self.put(ink2.get(),5,1)
		self.put(ink3.get(),9,1)
		
		if(refresh):
			self.refresh(win)
		
	def update_ink(self):
		self.update()
		
	def set_focus(self,x,y):
		x,y = x-self.x, y-self.y
		if(0<=x<3 and 0<=y<3):
			self.focus = 1
		elif(x==5 and y == 1):
			self.focus = 2
		elif(x==9 and y== 1):
			self.focus = 3
			
	def release_focus(self,x,y):
		if(self.focus):
			if(self.palette):
				if(self.palette.inside(x,y)):
					data= self.palette.get(x-PALETTE_X,y-PALETTE_Y)
					inks = (None,ink1,ink2,ink3)
					self.palette.put(inks[self.focus].get(),x-PALETTE_X,y-PALETTE_Y)
					inks[self.focus].set(data)
					self.palette.update_ink()
					self.palette.refresh(win)
			self.focus=0
		self.update()
		
ink1 = Ink()
ink2 = Ink()
ink3 = Ink()

tiny=pygame.image.load("tinier.png")
import codecs

def export_drawing(draw):
	data = draw.export_ainsi()
	print(data)
	drawing=codecs.open("Mydrawing.txt","w","utf-8")
	drawing.write(data)
	drawing.close()
	
def save_drawing(draw):
	matrix = draw.get_matrix()
	data = u"" + chr(len(matrix)) + chr(len(matrix[0]))
	for column in matrix:
		for character in column:
			if(character==None or None in character):
				data += u"00­" #thie third character is "­" or ord 173
			else:
				fg,bg,char = character
				if(fg in FOREGROUND_COLORS):
					data += hex(FOREGROUND_COLORS.index(fg))[-1]
				else:
					data += "0"
					print("EXPORT ERROR : ",fg, "not in",FOREGROUND_COLORS)
					
					
				if(bg in BACKGROUND_COLORS):
					data += hex(BACKGROUND_COLORS.index(bg))[-1]
				else:
					data += "0"
					print("EXPORT ERROR : ",bg, "not in",BACKGROUND_COLORS)
					
				data += char
	print(data)
	save=codecs.open("Mysave.txt","w","utf-8")
	save.write(data)
	save.close()

def load_drawing(draw):
	save=codecs.open("Mysave.txt","r","utf-8")
	mydata = list(save.read())
	save.close()
	w,h = int(mydata.pop(),16), int(mydata.pop(),16)
	matrix = [[(BLACK,BLACK," ")]*j for i in range(w)] #character is invincible space (ord(160))
	for i in range(w*h):
		fg,bg,char = int(mydata.pop(),16), int(mydata.pop(),16), mydata.pop()
		if(char == u"­"): #character is ord(173) caret
			char = None
		fg, bg = FOREGROUND_COLORS[fg], BACKGROUND_COLORS[bg]
		matrix[i%w][i//w] = (fg,bg,char)
	return matrix



def main():
	win._autodisplayupdate = False
	clock =  pygame.time.Clock()
	start=True
	mousex,mousey = -128, -128
	counter=0
	
	palette = PaletteArea(DRAWABLE_CHARACTERS)
	#palette.set_colorful()

	win.setscreencolors(None, "black", clear=True)
	#win.putchars(" "*MENU_WIDTH,MENU_X,MENU_Y,bgcolor=(128,128,128))
	menu=MenuArea()
	tools = ToolsArea()
	win.putchars("MY_DRAWING.txt | OTHER_DRAWING.txt | ",IMAGE_TITLE_X,IMAGE_TITLE_Y)

	drawing = DrawingArea()
	for j in range(DRAWING_HEIGHT):
		for i in range(DRAWING_WIDTH):
			data = (RED,BLACK, random.choice(("#","X","8","%","$",None)))
			drawing.put(data,i,j)
			
	win.putchars(u"◄ PALETTE 0    ►",PALETTE_X,PALETTE_Y-1)
	
	charaswitch = CharacterSwitch()
	charaswitch.set_palette( palette )
	tint = TintControlArea() #must be created AFTER palette
	
	ink1.notify(tint)
	ink1.notify(charaswitch)
	ink2.notify(charaswitch)
	ink3.notify(charaswitch)
	ink1.notify(palette)
	
	#draw_fg, draw_bg, draw_char = palette.get(0,0)
	#draw_fg2, draw_bg2, draw_char2 = palette.get(15,15)
	
	
	charaswitch.draw(win)
	menu.draw(win)
	tools.draw(win)
	palette.draw(win)
	drawing.draw(win)
	tint.draw(win)
	
	start=False
	
	areas = [menu,tools,palette,drawing,tint,charaswitch]
	focus = None
	
	win.putchar(ink1.get_char(),COLORS_X,COLORS_Y-2,fgcolor = ink1.get_fg(), bgcolor=ink1.get_bg())
	

	SCREEN=pygame.display.get_surface()
	
	while True:
		win.putchars(" "*WINDOW_WIDTH,INFOS_X,INFOS_Y)
			
		counter+=1
		clock.get_fps()
		if(counter>160):
			win.putchars(str(cellx-DX)+" ; "+str(celly-DY) + " - fps : " + 
			str(clock.get_fps()) + "                   " ,INFOS_X+1,INFOS_Y)
			
		#SCREEN.fill((0,0,0))
		pygame.draw.rect(SCREEN, (64,64,64) , (( xx(DX),yy(DY) ),( xx(DW),yy(DH) )) )
		win.update()
		
		pygame.draw.lines(SCREEN,BLUE, True, ( (DX*CW-1,DY*CH-1),(DX*CW+DW*CW,DY*CH-1),(DX*CW+DW*CW,DY*CH+DH*CH),(DX*CW-1,DY*CH+DH*CH) ))
		pygame.draw.ellipse(SCREEN, BLUE, (mousex,mousey,10,10))
		#SCREEN.blit(tiny,(16,16))
		palette.show_cursor(SCREEN)
		
		pygame.display.flip()
		clock.tick(60)
		

		
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif(event.type == MOUSEMOTION):
				cellx, celly = win.getcoordinatesatpixel(event.pos)
				mousex,mousey = event.pos
				if(focus):
					focus.focus_update(cellx,celly)
			elif(event.type == KEYDOWN and event.key == K_e):
				export_drawing(drawing)
			elif(event.type == KEYDOWN and event.key == K_s):
				save_drawing(drawing)
			elif(event.type == MOUSEBUTTONDOWN and event.button == 1): #1 is left, 2 is middle, 3 is right, 4 and 5 are wheel up and down
				#print("Pressed!")
				for area in areas:
					if area.inside(cellx,celly):
						if(focus):
							focus.release_focus(cellx,celly)
						area.set_focus(cellx,celly)
						focus=area
						break;
				
				if(palette.inside(cellx,celly)):
					#a, b, draw_char = palette.get(cellx-PALETTE_X,celly-PALETTE_Y)  or [None,None,None]
					
					#win.putchar(draw_char,COLORS_X,COLORS_Y-2, fgcolor=draw_fg, bgcolor=draw_bg)
					tint.update()
					tint.refresh(win)
					
					#print(palette.matrix[cellx-PALETTE_X][celly-PALETTE_Y])
				if(pos_in_rect(cellx,celly, PALETTE_X, PALETTE_Y-1, PALETTE_WIDTH, 1)):
					print(u"En-tête palette")

			elif(event.type == MOUSEBUTTONUP and event.button==1):
				if(focus):
					focus.release_focus(cellx,celly)
					focus=None
			elif(event.type == MOUSEBUTTONUP and event.button == 3):
				if(drawing.inside(cellx,celly)):
					#global draw_fg, draw_bg, draw_char
					ink1.set( drawing.get(cellx-DX,celly-DY) or [None,None,None] )
					print("Got color!",drawing.get(cellx-DX,celly-DY))

if __name__=="__main__":
	draw_fg, draw_bg, draw_char = WHITE, WHITE, " "
	draw_fg2, draw_bg2, draw_char2 = BLACK, BLACK, None
	main()
		
		
	

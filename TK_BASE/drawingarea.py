from utilities import repr_data
from utilities import repr_data_bw
#In construction, untested yet
MODIFICATION_COUNTER = 1
W = 80
H = 20
	
"""
This whole system is flawed when you have to update it.
Why did I chose this system over a Commands-based one? http://blog.wolfire.com/2009/02/how-we-implement-undo/
Because I wanted to include it in the Cases directly
REDO FROM ZERO. Kind of.
Commands are not possible since some actions are irreversible (lost info)
So might need to remember modified pixels before/after
The before could leech from the after of the previous action?
Some commands could have optimised before/after based on what is done
(Like moving a bunch of pixels or drawing a line)
But at the end of the day it should be able to be converted to pixels
Because we might want to combine several actions into one for optimisation reasons


"""

class Case():
	"""Contains the data for the cases
	A case is sort of a FG,BG,CHAR tuple
	Shows the last version corresponding to given MODIFICATION_COUNTER
	Meaning: contains versionned undos
	"""
	#dirty management is not up to level
	def default():
		return Case()
	def __init__(self,parent,fg="#000000",bg="#000000",char=" "):
		self.parent = parent
		self.fg_list = [(0,fg)]
		self.bg_list = [(0,bg)]
		self.char_list = [(0,char)]
		self.dirty = True
	def __iter__(self):
		return (i for i in (self.fg(),self.bg(),self.char()))
	def get(self):
		return self.fg(-1), self.bg(-1), self.char(-1)
	def fg(self, modif = None):
		if(modif==None):
			modif = MODIFICATION_COUNTER
		if(modif==-1):
			return self.fg_list[-1][1]
		else:
			for i in range(len(self.fg_list)-1,0,-1):
				if(self.fg_list[i][0]<MODIFICATION_COUNTER):
					return self.fg_list[i][1]
		return self.fg_list[0][1]
		
	def char(self, modif = None):
		if(modif==None):
			modif = MODIFICATION_COUNTER
		if(modif==-1):
			return self.char_list[-1][1]
		else:
			for i in range(len(self.char_list)-1,0,-1):
				if(self.char_list[i][0]<MODIFICATION_COUNTER):
					return self.char_list[i][1]
		return self.char_list[0][1]
		
	def bg(self, modif = None):
		if(modif==None):
			modif = MODIFICATION_COUNTER
		if(modif==-1):
			return self.bg_list[-1][1]
		else:
			for i in range(len(self.bg_list)-1,0,-1):
				if(self.bg_list[i][0]<MODIFICATION_COUNTER):
					return self.bg_list[i][1]
		return self.bg_list[0][1]
		
	def set_fg(self,fg):
		while(self.fg_list[-1][0] >= MODIFICATION_COUNTER):
			self.fg_list.pop()
		if(self.fg() == fg):
			return
		self.fg_list.append((MODIFICATION_COUNTER,fg))
		
	def set_bg(self,bg):
		while(self.bg_list[-1][0] >= MODIFICATION_COUNTER):
			self.bg_list.pop()
		if(self.bg() == bg):
			return
		self.bg_list.append((MODIFICATION_COUNTER,bg))
		
	def set_char(self,char):
		while(self.char_list[-1][0] >= MODIFICATION_COUNTER):
			self.char_list.pop()
		if(self.char() == char):
			return
		self.char_list.append((MODIFICATION_COUNTER,char))
		
	def visit(self):
		self.dirty = False
		self.pfg = self.fg()
		self.pbg = self.bg()
		self.pchar = self.char()
	def change(self):
		if(not self.dirty and (self.pfg!=self.fg() or self.pbg!=self.bg() or self.pchar!=self.char())):
			self.dirty = True
	def unchange(self):
		self.dirty = False
	def set(self,data):
		if(isinstance(data,Case)):
			data = tuple(data)
		if(isinstance(data,tuple) or isinstance(data,list)):
			self.set_fg(data[0])
			self.set_bg(data[1])
			self.set_char(data[2])
		else:
			raise TypeError("Give a Case or a tuple or a list")
			
		
	def empty(self):
		return self.fg(),self.bg(),self.char()==0,0," "
	def __eq__(self,other):
		if(isinstance(other,Case)):
			return self.fg() == other.fg() and self.bg() == other.bg() and self.char() == other.char()
		elif(isinstance(other,tuple)):
			return self.fg(),self.bg(),self.char() == other
	def __repr__(self):
		return str(self.get())


class Layer():
	"""A layer contains W*H Cases
	it has a transparency color
	it is contained in a stack
	"""
	MODE_NORMAL = 0
	MODE_FGCOLOR = 1
	MODE_BGCOLOR = 2
	MODE_CHAR = 3
	MODE_COLOR = 4
	MODE_ADD = 5 		#Add color ID value
	MODE_SUBTRACT = 6 	#Add color ID value
	MODE_WARMER = 7 	#Follow roulette
	MODE_COLDER = 8 	#Follow roulette
	def notify_parent(self, data):
		self.parent.notify_parent(data)
		#TODO idea: notify the higher layers instead, until the top layer notifies the parent
		#Unless the place is occupied, in this case stop the propagation
		#Or when you notify the parent, the parent checks
	
	def _is_inside_(self,x,y):
		return self.x<=x<self.x+self.w and self.y<=y<self.y+self.h
	def _is_outside_(self,x,y):
		return not self._is_inside_(x,y)
	
	def __init__(self, parent):
		self.parent = parent
		self.empty = True
		self.pixels = 0
		self.cases = [[Case(self) for y in range(H)] for x in range(W)]
		self.x = 0
		self.y = 0
		self.w = W
		self.h = H
		self._transparency_color_ = 0 #Pixels with double this color AND " " character are transparent
		#see transparent_case()
		self.allow_transparency = True
		self.mode = Layer.MODE_NORMAL #only one implemented so far)
		self.visible = True
		#
		self.set = self.put
		self.set_bg = self.putbg
		self.set_char = self.putchar
		self.set_fg = self.putfg
	def set_transparency(self, color, id = None):
		self._transparency_color_ = color
		self.notify_parent(("setalpha",color,id))
	def transparency(self):
		return (self._transparency_color_,self._transparency_color_," ")
	def put(self,x,y,data, id = None):
		#print("Old:",self.cases[x][y].get())
		self.cases[x][y].set(data)
		#print("New:",self.cases[x][y].get())
		self.notify_parent(("put",x,y, id))
	def putchar(self,x,y,char, id = None):
		self.cases[x][y].set_char(char)
		self.notify_parent(("put",x,y, id))
	def putfg(self,x,y,fg, id = None):
		self.cases[x][y].set_fg(fg)
		self.notify_parent(("put",x,y, id))
	def putbg(self,x,y,bg, id = None):
		self.cases[x][y].set_bg(bg)
		self.notify_parent(("put",x,y, id))
	def get_bg(self,x,y):
		return self.cases[x][y].bg()
	def get_fg(self,x,y):
		return self.cases[x][y].fg()
	def get_char(self,x,y):
		return self.cases[x][y].char()
	def get(self,x,y):
		return self.cases[x][y].get()
	def get_nontransparent(self,x,y):
		if(self.is_transparent(x,y) or self._is_outside_(x,y)):
			return None
		else:
			return self.get(x,y)
		
	def is_transparent(self,x,y):
		return self.allow_transparency and (self.get(x,y) == self.transparency())
	def is_layer_empty(self):
		for x in range(self.w):
			for y in range(self.h):
				if(not self.is_transparent(x,y)):
					return False
		return True
	def allow_transparency_toggle(self,value=None):
		if(value==None):
			self.allow_transparency = not self.allow_transparency
		else:
			self.allow_transparency = value
	def select_rect(self,x,y,w,h):
		#create a rectangular selection from a rectangle
		result = []
		for px in range(x,x+w):
			column = []
			for py in range(y,y+h):
				if(self._is_inside_(px,py) and not self.is_transparent(px,py)):
					column.append(self.cases[px][py])
				else:
					column.append(None)
			result.append(column)
		return result, x,y #optimise: cut the borders outside instead of filling with None
	def select(self,points):
		#create a rectangular selection from an iterable of points
		leftmost = min(points)
		leftmostx = leftmost[0]
		upmosty = leftmost[1]
		upmost = leftmost
		rightmost = max(points) #could do in same loop but same
		rightmostx = rightmost[0]
		downmosty = rightmost[1]
		downmost = rightmost
		for point in points:
			if(point[1]<upmosty):
				upmost = point
				upmosty = point[1]
			if(point[1]>downmosty):
				downmost = point
				downmosty = point[1]
		results = [[None for x in range(leftmostx,rightmostx+1)] for y in range(upmosty,downmosty+1)]
		for px,py in points:
			if(self._is_inside_(px,py) and not is_transparent(px,py)):
				results[px-leftmostx][py-upmosty] = self.get(px,py)
			else:
				results[px-leftmostx][py-upmosty] = None
		return results, leftmostx,upmosty 
		#optimise: cut the borders outside instead of filling with None (count only isinside points)
			
	def remove_rect(self,x,y,w,h):
		for px in range(x,x+w):
			for py in range(y,y+h):
				self.put(px,py,self.transparency)
		
		self.notify_parent(("rect",x,y,w,h, id))
	def shift_zone(self,dx,dy):
		#[TODO] test boundaries
		selection = self.select_rect(self.x,self.y,self.w,self.h)
		self.remove_rect(self.x,self.y,self.w,self.h)
		
		self.x-=dx
		self.y-=dy
		for x in range(self.x,self.x+self.w):
			for y in range(self.y,self.y+self.h):
				self.put(x,y,selection[x-self.x][y-self.y])
		
class Stack():
	canvas = None
	current_layer_id = 0
	
	def get_current_layer(self):
		return self.layers[self.current_layer_id]
	
	def notify_parent(self, data):
		if(self.parent != None):
			self.parent.notify_update(data)
		
	def __init__(self, parent = None):
		self.layers = [Layer(self)]
		self.parent = parent
		self.image_speed = 100
	
	def add_layer(self):
		self.layers.append(Layer(self))
		
	def set_image_speed(self, msec):
		self.image_speec = msec
		
	def combine_layers(self):
		result = []
		
		for x in range(W):
			column = []
			for y in range(H):
				color = None
				for layer in self.layers:
					color = layer.get(x,y)
					# if(color[0]!="#000000"):
						# print(color)
					# if layer.mode == Layer.MODE_NORMAL:
						# color = layer.get_nontransparent(x,y)
						# if(color!=None):
							# break
				column.append(color)
			result.append(column)
		#print(str(self.layers[0].cases))
		return result
		
# # def test():
	# # global MODIFICATION_COUNTER
	# # from random import randint
	# # p = Stack()
	# # for i,layer in enumerate(p.layers):
		# # for j in range(20):
			# # x=randint(0,W-1)
			# # y=randint(0,H-1)
			# # layer.put(x,y ,(5,0,chr(ord("A")+i)))
			# # # print(x,y,layer.get(x,y))
		# # MODIFICATION_COUNTER +=1
			
	# # for i in range(8):
		# # result = p.combine_layers()
		# # # print(result)
		# # str_result = repr_data(result)
		# # print(str_result)
		# # MODIFICATION_COUNTER -= 1
		
	# # for i in range(4):
		# # result = p.combine_layers()
		# # # print(result)
		# # str_result = repr_data(result)
		# # print(str_result)
		# # MODIFICATION_COUNTER += 1
	# # MODIFICATION_COUNTER = 1
	# # # Need something different to break the future modifs
	# # # Harder to update
	# # result = p.combine_layers()
	# # # print(result)
	# # str_result = repr_data(result)
	# # print(str_result)
	# # input()
	
	# # for i,layer in enumerate(p.layers):
		# # x=randint(0,W-1)
		# # y=randint(0,H-1)
		# # layer.put(x,y ,(5,0,chr(ord("a")+i)))
	# # MODIFICATION_COUNTER +=1
	# # for i in range(8):
		# # result = p.combine_layers()
		# # # print(result)
		# # str_result = repr_data(result)
		# # print(str_result)
		# # MODIFICATION_COUNTER += 1
		
		
		
# # test()	
class Drawing():
	def get_current_layer(self):
		return self.stacks[self.image_index].get_current_layer()
	def get_current_stack(self):
		return self.stacks[self.image_index]
	def notify_update(self,data):
		if(data[0]=="put"):
			self.canvas.redraw(positions = [(data[1],data[2])])
		else:
			self.canvas.redraw()
		#print("Redrawing")
	"""
		what needed:
			self.image_index = 0
			self.anim = [] #for each animation image, there are layers
			self.last_layer = 0 
			#nitpick: if the number of the layer is different, this number will not change until we really click
			#Do we do by name? or by limiting the number of layers and doing "layer depths"
			#I say we have 4~8 layers that can be empty, swapped
			#Colors should be CHAR, COLOR_INDEX, COLOR_INDEX
			Am currently using: FG, BG, CHAR instead...
			#Transparency for each layer should be definable
			self.sizes = [] #contains the sizes of each image and layer, and offsets
			#those will appear as little boxes
			self.image = None #must have an "update" function with X,Y or more
			self.update_image(x,y)
			self.image_dirty = [] #this contains 80*25 instead (screen size)
			A selection, that can go all the layers deep if alt is pressed
			"""
			
	#Just the areas, like my old ones
	def set_canvas(self,drawingmanager):
		self.canvas = drawingmanager
		
	def __init__(self):
		self.image_index = 0
		self.stacks = [Stack(self)]
		
		# for i in range(min(CH-2,CW-2,25)):
			# self.canvas.putchar(i,i,chr(ord("a")+i),WHITE,RED)
	
	# # def move(self,x,y):
		# # self.x=x
		# # self.y=y
	# # def draw():
		# # pass
	# # def click(self,x,y,tool):
		# # if(tool==0):
			# # #print("FG:",curfg,"BG:",curbg)
			# # self.dc.condputchar(x,y,choice("▀▄█░▒▓"),None,None)
			# # """self.dc.putchar(x,y,
							# # dobg and choice("▀▄█░▒▓") or None,
							# # dofg and curfg or None,
							# # dochar and curchar or None)"""
		# # pass
		
	# # def typechar(self,x,y,char):
		# # if(char!=""):
			# # self.dc.condputchar(x,y,char,curfg,curbg)
	
				
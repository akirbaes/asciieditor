import time
from interface_constants import *

def gen_time():
	l = time.localtime(time.time())
	return (str(l.tm_year)+"_"+\
		(str(l.tm_yday).zfill(3))+"_"+\
		(str(l.tm_hour).zfill(2))+\
		(str(l.tm_min).zfill(2))+\
		(str(l.tm_sec).zfill(2)))
		

def BGCODE(color):
	index = BACKGROUND_COLORS.index(color)
	return str(index+40)
	
def FGCODE(color):
	index = FOREGROUND_COLORS.index(color)
	return str(index%8+30)
	

def ansicolorcode_to_colorindexnumber(ansi_string):
	#receives an \0xetc. code,
	#returns the FG and BG
	#Because I'll probably not use them if I use any engine not console-based
	#\x1b[0;56;89m
	#len("\x1b[")==2
	data = ansi_string.replace("\x1b[","").replace("m","").split(";")
	
	if "1" in data:
		brightness = 1 #"bold"
	elif "22" in data:
		brightness = 0 #"normal"
	else:
		brightness = None
	
	bgi = None
	fgi = None
	for n in data:
		if("40"<=n and n<"48"):
			bgi = int(n)-40
		elif("30"<=n and n<"38"):
			fgi = int(n)-30
	if "0" in data:
		brightness = 0
		fgi = -1
		bgi = -1
	return brightness, fgi, bgi
	
def ansistring_to_charcolorindextriplet(ansistring,fgstart = WHITE, bgstart = BLACK):
	escs, esce = nextEscape(ansistring,0)
	brightness = 0 #normal
	fg = fgstart
	bg = bgstart
	alldata = []
	currentline = []
	i=0
	while i<len(ansistring):
		if(i==escs and esce > escs):
			nbright,nfg,nbg = utilities.ansicolorcode_to_colorindexnumber(ansistring[escs:esce+1])
			#print(escs,esce,'"'+ansistring[escs:esce+1]+'"',"->",nbright,nfg,nbg)
			i=esce #position of the m
			escs, esce = nextEscape(ansistring,i)
			#print(escs,esce,'"'+ansistring[escs:esce+1]+'"',"->","new")
			if(nbright!=None):
				brightness = nbright
			if(nfg!=None):
				if(nfg==-1):
					fg = fgstart
				else:
					fg = FOREGROUND_COLORS[brightness*8+nfg]
			if(nbg!=None):
				if(nbg==-1):
					bg = bgstart
				else:
					bg = BACKGROUND_COLORS[nbg]
		else:
			if(ansistring[i] in DRAWABLE_CHARACTERS):
				currentline.append((ansistring[i],fg,bg))
			elif(ansistring[i]=="\n"):
				alldata.append(currentline)
				currentline = []
			else:
				currentline.append(("?",fg,bg))
		i+=1
	return alldata
	

def nextEscape(string,startpos):
	index = string.find("\x1b[",startpos)
	#print("Found at",index)
	index2 = string.find("m",index)
	#print("Found second at",index2)
	return index,index2
	
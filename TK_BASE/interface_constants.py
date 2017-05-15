def tocolor(r,g,b):
	"""RGB to hex string"""
	return "#"+(hex(256*256*r+256*g+b)[2:].zfill(6))
	
BLACK = tocolor(0,0,0)
LTBLACK = tocolor(128,128,128)
RED = tocolor(128,0,0)
LTRED = tocolor(255,0,0)
GREEN = tocolor(0,128,0)
LTGREEN = tocolor(0,255,0)
YELLOW = tocolor(128,128,0)
LTYELLOW = tocolor(255,255,0)
BLUE = tocolor(0,0,128)
LTBLUE = tocolor(0,0,255)
MAGENTA = tocolor(128,0,128)
LTMAGENTA = tocolor(255,0,255)
CYAN = tocolor(0,128,128)
LTCYAN = tocolor(0,255,255)
WHITE = tocolor(192,192,192)
LTWHITE = tocolor(224,224,224)


colors = [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]
colors2 = [LTBLACK, LTRED, LTGREEN, LTYELLOW, LTBLUE, LTMAGENTA, LTCYAN, LTWHITE]


BACKGROUND_COLORS = colors
FOREGROUND_COLORS = colors+colors2
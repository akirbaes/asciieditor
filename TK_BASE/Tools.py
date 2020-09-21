import interface_constants as IC
import sys
flush = sys.stdout.flush
from numpy import sign

class Tool():
    name = "Unnamed"
    click_x = None
    click_y = None
    current_x = None
    current_y = None
    cursorstyle = "pencil"
    widget = None
    has_selector = False
    #Common
    def select_tool_init(self):
        self.click_x = None
        self.click_y = None
        self.current_x = None
        self.current_y = None
        self.widget.config(cursor=cursorstyle)
        
    def __init__(self, concerned_widget):
        self.widget = concerned_widget
    
    def has_click(self):
        return self.click_x != None and self.click_y != None
    #Custom
    
    def send_event(self, eventType, event, layer=None):
        pass
        
    def keyboard(self, character, layer):
        pass
        
    def left_click(self, x, y, layer):
        self.click_x, self.click_y = x, y
        
    def right_click(self, x, y, layer):
        self.click_x, self.click_y = x, y
        
    def left_release(self, x, y, layer):
        if(has_click(self)):
            pass
        self.click_x, self.click_y = None, None
        
    def right_release(self, x, y, layer):
        if(self.has_click(self)):
            pass
        self.click_x, self.click_y = None, None
        
    def mouse_move(self, x, y):
        return
        #Update visuals
        
    def right_mouse_drag(self, x, y):
        return
        #Update visuals and data
    def left_mouse_drag(self, x, y):
        return
        #Update visuals and data
        
    def mouse_enter(self, x, y):
        return
        #Update visuals
    def mouse_leave(self,x, y):
        #Update visuals
        return
    
class Pen(Tool):
    name = "Pen"
    cursorstyle = "pencil"
    line_number = 0
    def __init__(self, canvas, handler):
        # print("New Pen")
        # flush()
        self.widget = canvas
        self.widget.config(cursor="pencil")
        self.handler = handler #when having to change of tool on the fly?
    def send_event(self,eventType, event,layer=None, char_width = IC.CW, char_height = IC.CH, current_char = None):
        #if(event.widget == concerned_widget):
        # print("Got event:",event)
        # for thing in dir(event):
            # print(thing,repr(event.__getattribute__(thing)), event.__getattribute__(thing))
        # print(dir(event))
        
        ########LEFT CLICK: drawing
        if(eventType=="<Button-1>"):
            # print("Got click")
            x,y = event.x//char_width, event.y//char_height
            self.click_x, self.click_y = x, y
            Pen.line_number += 1
            self.trace(x,y,x,y,layer,(current_char))
            self.current_x,self.current_y = x,y
        elif(eventType=="<B1-Motion>"):
            x,y = event.x//char_width, event.y//char_height
            #print(self.click_x, self.click_y,",", x,y)
            #sys.stdout.flush()
            if(self.has_click()):
                self.trace(x, y, self.click_x, self.click_y, layer, (current_char))
                self.click_x, self.click_y = x, y
            self.current_x,self.current_y = x,y
        elif(eventType=="<ButtonRelease-1>"):
            self.click_x, self.click_y = None, None
            self.current_x,self.current_y = None, None
            
            
        #######RIGHT CLICK: colir pick or switch to special selector
        elif(eventType=="<Button-3>"):
            x,y = event.x//char_width, event.y//char_height
            self.click_x, self.click_y = x, y
            self.current_x,self.current_y = x,y
        elif(eventType=="<B3-Motion>"):
            x,y = event.x//char_width, event.y//char_height
            
            if(self.has_click()):
                if(x == self.click_x or y==self.click_y):
                    self.widget.config(cursor="pencil")
                    self.has_selector = False
                    self.current_x,self.current_y = None, None
                else:
                    self.widget.config(cursor="crosshair")
                    self.has_selector = True
                    self.current_x,self.current_y = x,y
                pass
            #set the cursor lines on the canvas
        elif(eventType=="<ButtonRelease-3>"):
            x,y = event.x//char_width, event.y//char_height
            #Copy Graphicsgale's approach
            sys.stdout.flush()
            if(self.has_click()):
                if(x == self.click_x or y==self.click_y):
                    fg,bg,c = layer.get(self.click_x, self.click_y)
                    curfg, curbg, curchar = self.handler.current_character_variables
                    curfg.set(fg)
                    curbg.set(bg)
                    curchar.set(c)
                    self.widget.config(cursor="pencil")
                else:
                    x0, x1 = min(self.click_x, x), max(self.click_x,x)
                    y0, y1 = min(self.click_y, y), max(self.click_y,y)
                    rect = layer.select_rect(x0, y0, x1-x0, y1-y0)
                    # print("Received selection:",rect)
                    layer.remove_rect(x0, y0, x1-x0, y1-y0)
                    # print("Changing toool")
                    # sys.stdout.flush()
                    self.handler.change_tool(Mover)
                    self.handler.get_current_tool().initial_layer=layer
                    self.handler.set_selection(rect, x0, y0)
                self.click_x, self.click_y = None, None
                self.has_selector = False
                self.current_x,self.current_y = None, None
            
            
            
    def trace(self, x,y, xprev, yprev, layer, char_data):
        if(x==xprev and y==yprev):
            layer.put(x,y,char_data, id = (Pen.name,Pen.line_number))
        elif(abs(xprev-x)>abs(yprev-y)):
            s = sign(x-xprev)
            for X in range(xprev, x+s, s):
                delta = abs((X-xprev) / (x-xprev))
                Y = int(yprev + (y-yprev)*delta)
                layer.put(X,Y,char_data, id = (Pen.name,Pen.line_number))
        else: #if(abs(xprev-x)<=abs(yprev-y)):
            s = sign(y-yprev)
            for Y in range(yprev, y+s, s):
                if(y==yprev):
                    X = x
                else:
                    delta = abs((Y-yprev) / (y-yprev))
                    X = int(xprev + (x-xprev)*delta)
                layer.put(X,Y,char_data, id = (Pen.name,Pen.line_number))
    
#penselector:
#either double duty (two variables in pen)
#or right click will send to a different tool
class Mover(Tool):
    name = "Mover"
    flush()
    """When moving around, moves the selection"""
    """When right click, undo the selection"""
    cursorstyle = "diamond_cross"
    nocursorstyle = "X_cursor"
    def __init__(self, canvas, handler):
        # print("New Mover")
        self.widget = canvas
        self.widget.config(cursor="X_cursor")
        self.handler = handler
        self.previous_tool = Pen
    def send_event(self,eventType, event,layer=None, char_width = IC.CW, char_height = IC.CH, current_char = None):
    
        #if(event.widget == concerned_widget):
        # print("Got event:",event)
        # for thing in dir(event):
            # print(thing,repr(event.__getattribute__(thing)), event.__getattribute__(thing))
        # print(dir(event))
        
        if(eventType=="<Button-1>"):
            # print("Got click")
            if(self.handler.is_in_selection(event.x,event.y)):
                x,y = event.x//char_width, event.y//char_height
                self.click_x, self.click_y = x, y
                self.current_x,self.current_y = x,y
            else:
                pass
        elif(eventType=="<B1-Motion>"):
            x,y = event.x//char_width, event.y//char_height
            #print(self.click_x, self.click_y,",", x,y)
            #sys.stdout.flush()
            self.current_x, self.current_y = x, y
            #self.left_click(x,y,self.initial_layer)
            if(self.has_click()):
                dx, dy = self.current_x - self.click_x, self.current_y - self.click_y
                self.handler.move_selection_relative(dx,dy)
                self.click_x, self.click_y = x, y
        elif(eventType=="<ButtonRelease-1>"):
            self.click_x, self.click_y = None, None
            self.current_x,self.current_y = None, None
        elif(eventType=="<Motion>"):
            if(self.handler.is_in_selection(event.x,event.y)):
                self.widget.config(cursor=self.cursorstyle)
            else:
                self.widget.config(cursor=self.nocursorstyle)
            
            
        #######RIGHT CLICK: stop it
        elif(eventType=="<Button-3>"):
            self.handler.change_tool(self.previous_tool)
            self.handler.merge_selection(layer)
            self.handler.remove_selection()
            self.initial_layer=None
            
    def __del__(self):
        #self.handler.change_tool(self.previous_tool) #No: if deleted, probably because changed tool
        if(self.initial_layer!=None):
            self.handler.merge_selection(self.initial_layer) #Update when Layer are implemented [TODO]
            self.handler.remove_selection()
        
class Text(Tool):
    name = "Text"
    click_number = 0
    def __init__(self,canvas,handler):
        # print("New Mover")
        self.widget = canvas
        self.widget.config(cursor="xterm")
        self.handler = handler
        self.click_x=None
        self.click_y=None
        
    def send_event(self,eventType, event,layer=None, char_width = IC.CW, char_height = IC.CH, current_char = None):
        if(eventType=="<Button-1>"):
            x,y = event.x//char_width, event.y//char_height
            self.left_click(x,y,layer)
            Text.click_number+=1
        elif(eventType=="<Key>"):
            c=event.char
            if(len(c)==1 and self.has_click()):
                layer.put(self.click_x,self.click_y,current_char[0:2]+(c,), id = (Text.name,Text.click_number))
                self.click_x+=1
                
                

ALLTOOLS=[Pen,Text]

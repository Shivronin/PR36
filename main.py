from kivy.config import Config
Config.set("graphics", "resizable", 0)
from random import uniform
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.properties import ListProperty



Window.size = (360, 800)


sline = False
clr=[1,1,0.5,1]
pre_clr=clr
xs=0
ys=0
xboun=0
yboun=0
rect=False
press=0
wide=5
def reset():
    global rect, ell, sline
    rect=ell=sline=False
def retclr():
    return clr

def incanvasxy(self,x,y):
    if x > -0.5* self.width and y >0.2 *self.height and x < self.width*1 and y < self.height*1:
        return True


class Painter(Widget):
    
    col = ListProperty(clr)
     

    def on_touch_down(self, touch):
        #print "down"
        global xs,ys,xboun,yboun,press,wide
        press = 1
        if incanvasxy(self,touch.x,touch.y):   
            
            self.col= retclr()
            if Widget.on_touch_down(self, touch):
                xs=touch.x
                ys=touch.y    
                return True

            with self.canvas:
                Color(*self.col)
                touch.ud['line'] = Line(points=(touch.x, touch.y),width=wide)
                xs=touch.x
                ys=touch.y
        else:
            xs=touch.x
            ys=touch.y    
    def on_touch_move(self, touch):
        #print "move"
        global xs,ys,xboun,yboun,wide
        if incanvasxy(self,touch.x,touch.y) :
            self.col= retclr()
            if sline:
                if Widget.on_touch_move(self, touch):
                    return True
                with self.canvas.after:
                    self.canvas.after.clear()

                    Color(*self.col)
                    Line(points=(touch.x,touch.y),width=wide)
                xboun=touch.x
                yboun=touch.y
        
                    
            else:
                if incanvasxy(self,xs,ys):
                    touch.ud["line"].points += [touch.x, touch.y]
    def on_touch_up(self, touch):
        #print "up"
        global xs,ys,press,wide
        
        if incanvasxy(self,xs,ys):
            if incanvasxy(self,touch.x,touch.y) :    
                
                if sline:
                    
                    self.col= retclr()
                    
                    if Widget.on_touch_down(self, touch):
                        return True
                    with self.canvas:
                        Color(*self.col)
                        Line(points=(touch.x,touch.y,xs,ys),width=wide) 
                if rect:
                    
                    self.col= retclr()
                    
                    if Widget.on_touch_down(self, touch):
                        return True
                    with self.canvas:
                        Color(*self.col)
                        Line(rectangle=(xs, ys, touch.x-xs, touch.y-ys),width=wide)         
            else:
                if press:
                    if sline :
                        with self.canvas:
                                if xboun:
                                    Color(*self.col)
                                    Line(points=(xboun,yboun,xs,ys),width=wide)
                        self.canvas.after.clear()
                    if rect :
                        with self.canvas:
                                if xboun:
                                    Color(*self.col)
                                    Line(rectangle=(xs, ys, xboun-xs, yboun-ys),width=wide)
                        self.canvas.after.clear() 
        self.canvas.after.clear()                  
        press=0                     
class Cpicker(ColorPicker):
    pass

class popup(Popup):
    def hello (self, y):
        global clr,pre_clr
        pre_clr=clr    
        clr=y 


class MainScreen(Screen):
    
    def open_it1(self):
        popup().open()

    
    def eraser(self):
        global clr,pre_clr,sline
        reset()
        pre_clr = clr
        clr= [0,0,0,1]
    
    def thick(self,*args):
        global wide
        wide = args[1]
        self.lab.text = "Толщина : " + str(args[1])
        
class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class painApp(App):
    def build(self):
        return presentation

if __name__== "__main__":
    painApp().run()
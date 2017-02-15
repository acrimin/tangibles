import math

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.properties     import *
from kivy.garden.tei_knob import  Knob


from renderer import Renderer

class MyKnob(Knob):
    # Object property that receives the image
    obj = ObjectProperty()

    # on_knob is called if value, token_id or token_placed chage
    #def on_knob(self, value, pattern_id):
        #angle = value
        #self.obj.rotation = angle

    def on_token_placed(self, instance, value):
        print "token Placed: " + str(value)

class Application(App):
    def build(self):
        root = Widget()
        root.add_widget(Renderer())

        print (root.width)

        knob = MyKnob(
                        pos = (root.width, 0),
                        size = (300, 300),
                        min = 0, max = 360,
                        step = 1,
                        show_marker = True,
                        knobimg_source = "img/knob_metal.png",
                        marker_img = "img/bline.png",
                        markeroff_color = (0.3, 0.3, .3, 1),
                        pattern_id= 99, #(ids 1 to 8, or 99 for no id)
                        debug = False,
                        obj = None) # Passes the object to the knob

        root.add_widget(knob)
        return root


if __name__ == "__main__":
    Application().run()

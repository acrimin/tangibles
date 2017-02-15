from kivy.properties     import *
from kivy.garden.tei_knob import  Knob

class MyKnob(Knob):
    # Object property that receives the image
    obj = ObjectProperty()

    # on_knob is called if value, token_id or token_placed chage
    def on_knob(self, value, pattern_id):
        angle = value
        self.obj.rotation = angle

    def on_token_placed(self, instance, value):
        print "token Placed: " + str(value)
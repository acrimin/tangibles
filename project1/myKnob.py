from kivy.properties     import *
from kivy.garden.tei_knob import  Knob

class MyKnob(Knob):
    def __init__(self, **kwargs):
        super(MyKnob, self).__init__(**kwargs)
        print "init"
        self.controller = kwargs['controller']

    # on_knob is called if value, token_id or token_placed chage
    def on_knob(self, value, pattern_id):
        print "knob:", value
        self.controller.setRotation(value, 0)


    def on_token_placed(self, instance, value):
        print "token Placed: " + str(value)
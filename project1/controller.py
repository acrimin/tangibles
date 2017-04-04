from kivy.core.window import Window
import sys

from ui import UI

from kivy.lib.osc import oscAPI
from kivy.clock import Clock

class Controller():
    def __init__(self, **kwargs):
        # self.sendip = sys.argv[1]
        # self.sendPort = 5001
        # self.recvPort = 5002

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.renderer = kwargs['renderer']

        self._prevKnob = [0.,0.,0.]
        self._touches = []

        oscAPI.init()  
        oscid = oscAPI.listen(ipAddr="127.0.0.1", port= 5000) 
        Clock.schedule_interval(lambda *x: oscAPI.readQueue(oscid), 0)
        oscAPI.bind(oscid, self.dialListener, '/tuios/tok')

        # oscid2 = oscAPI.listen(ipAddr=self.sendip, port= self.recvPort) 
        # Clock.schedule_interval(lambda *x: oscAPI.readQueue(oscid2), 0)
        # oscAPI.bind(oscid2, self.receive, '/tuios/tok')

    def setUI(self, ui):
        self.ui = ui

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.rotate(0,-5)
        elif keycode[1] == 'right':
            self.rotate(0,5)
        if keycode[1] == 'up':
            self.rotate(-5,0)
        elif keycode[1] == 'down':
            self.rotate(5,0)
        elif keycode[1] == 'r':
            self.reset()
        elif keycode[1] == 'escape':
            sys.exit()
        elif keycode[1] == '.':
            self.zoom(0.1)
        elif keycode[1] == ',':
            self.zoom(-0.1)
        elif keycode[1] == 'a':
            self.setRotation(35,-270)
            self.ui.popup(0)
        elif keycode[1] == 's':
            self.setRotation(-20,-90)
            self.ui.popup(1)
        elif keycode[1] == 'd':
            self.setRotation(-30,-185)
            self.ui.popup(2)
        elif keycode[1] == 'f':
            self.setRotation(55,-90)
            self.ui.popup(3)
        return True     

    def send(self):
        x = self.renderer.rotx.angle
        y = self.renderer.roty.angle
        z = self.renderer.scale.xyz[0]
        print "sending:", x, y, z

        # oscAPI.sendMsg('/tuios/tok', [x,y,z], 
        #                             ipAddr= self.sendip, 
        #                             port= self.sendPort) 

    def receive(self, value, instance):
        x = value[2]
        y = value[3]
        z = value[4]

        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y
        self.renderer.scale.xyz = (z,z,z)

    def rotate(self, rotX, rotY):
        self.renderer.rotx.angle += rotX
        self.renderer.roty.angle += rotY
        self.send()

    def setRotation(self, x, y):
        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y
        self.send()

    def zoom(self, scale):
        xyz = self.renderer.scale.xyz
        if (xyz[0] + scale > 0):
            self.renderer.scale.xyz = tuple(p + scale for p in xyz)
            self.send()

    def reset(self):
        self.renderer.rotx.angle = 0
        self.renderer.roty.angle = 0
        self.renderer.scale.xyz = (1,1,1)
        self.send()

    def dialListener(self, value, instance):
        # print ("value", value, "instance:", instance)
        knob = value[2] - 1
        angle = float(value[7])

        if (value[8] == 1):
            self._prevKnob[knob] = -1.
        elif (self._prevKnob[knob] == -1.):
            self._prevKnob[knob] = angle
        else:
            delta = angle - self._prevKnob[knob]
            self._prevKnob[knob] = angle
            if (abs(delta) > 100):
                delta = 0
            if (knob == 0):
                self.rotate(0,delta)
            elif (knob == 1):
                self.rotate(delta,0)
            elif (knob == 2):
                self.zoom(delta*.01)

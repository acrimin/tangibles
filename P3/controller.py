from kivy.core.window import Window
import sys

from ui import UI

from kivy.lib.osc import oscAPI
from kivy.clock import Clock

class Controller():
    def __init__(self, **kwargs):
        self.sendip = sys.argv[len(sys.argv)-1]

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.renderer = kwargs['renderer']

        self._prevKnob = [0.,0.,0.]
        self._touches = []

        oscAPI.init()  
        oscid = oscAPI.listen(ipAddr="0.0.0.0", port= 5000) 
        Clock.schedule_interval(lambda *x: oscAPI.readQueue(oscid), 0)
        oscAPI.bind(oscid, self.dialListener, '/tuios/tok')
        oscAPI.bind(oscid, self.receive, '/tuios/intra')
        oscAPI.bind(oscid, self.receiveVid, '/tuios/video')

    def receiveVid(self, value, instance):
        print value[2]
        print value[3]

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
            self.popup(35,-270,0)
        elif keycode[1] == 's':
            self.popup(-20,-90,1)
        elif keycode[1] == 'd':
            self.popup(-30,-185,2)
        elif keycode[1] == 'f':
            self.popup(55,-90,3)
        return True     

    def send(self, popup=-1):
        x = self.renderer.rotx.angle
        y = self.renderer.roty.angle
        z = self.renderer.scale.xyz[0]
        print "sending:", x, y, z, popup

        oscAPI.sendMsg('/tuios/intra', [x,y,z,popup], 
                                    ipAddr= self.sendip, 
                                    port= 5000) 

    def receive(self, value, instance):
        x = value[2]
        y = value[3]
        z = value[4]
        p = value[5]

        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y
        self.renderer.scale.xyz = (z,z,z)

        if (p != -1):
            self.popupRecv(p)

    def rotate(self, rotX, rotY):
        self.renderer.rotx.angle += rotX
        self.renderer.roty.angle += rotY
        self.send()

    def popup(self, x, y, pageNum):
        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y
        self.ui.popup(pageNum)
        self.send(pageNum)

    def popupRecv(self,pageNum):
        self.ui.popup(pageNum)

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
        print "dialListener"
        print ("value", value, "instance:", instance)

        knob = value[2] - 1
        angle = float(value[7])

        print "angle: " + str(angle)

        if (value[8] == 1):
            self._prevKnob[knob] = -1.
        elif (self._prevKnob[knob] == -1.):
            self._prevKnob[knob] = angle
        else:
            delta = angle - self._prevKnob[knob]
            print "delta"
            print delta
            if delta == 999:
                self.reset()
            else:
                self._prevKnob[knob] = angle
                if (abs(delta) > 100):
                    delta = 0
                if (knob == 0):
                    self.rotate(0,delta)
                elif (knob == 1):
                    self.rotate(delta,0)
                elif (knob == 2):
                    self.zoom(delta*.01)

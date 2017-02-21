from kivy.core.window import Window
import sys

from ui import UI

from kivy.lib.osc import oscAPI
from kivy.clock import Clock

class Controller():
    def __init__(self, **kwargs):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.renderer = kwargs['renderer']

        self._touches = []

        oscAPI.init()  
        oscid = oscAPI.listen(ipAddr="127.0.0.1", port= 5000) 
        Clock.schedule_interval(lambda *x: oscAPI.readQueue(oscid), 0)
        oscAPI.bind(oscid, self.listener, '/tuios/tok')

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.rotate(-5,0)
        elif keycode[1] == 'right':
            self.rotate(5,0)
        if keycode[1] == 'up':
            self.rotate(0,-5)
        elif keycode[1] == 'down':
            self.rotate(0,5)
        elif keycode[1] == 'n':
            self.setRotation(0,0)
        elif keycode[1] == 'escape':
            sys.exit()
        elif keycode[1] == '.':
            self.zoom(-0.1)
        elif keycode[1] == ',':
            self.zoom(0.1)

        return True     

    def rotate(self, rotX, rotY):
        self.renderer.rotx.angle += rotX
        self.renderer.roty.angle += rotY

    def setRotationX(self, x):
        self.renderer.rotx.angle = x

    def setRotationY(self, y):
        self.renderer.roty.angle = y

    def setRotation(self, x, y):
        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y

    def zoom(self, zoom):
        print self.renderer.camera_translate
        self.renderer.camera_translate[2] += zoom

    def setZoom(self, zoom):
        self.renderer.camera_translate[2] = zoom

    def listener(self, value, instance):
        print ("value", value, "instance:", instance)
        knob = value[2]
        angle = int(value[7])
        if (knob == 1):
            self.setRotationX(angle)
        elif (knob == 2):
            self.setRotationY(angle)
        elif (knob == 3):
            self.setZoom(angle)
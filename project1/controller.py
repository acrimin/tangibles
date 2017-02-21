from kivy.core.window import Window
import sys

from ui import UI
from internet import Internet

class Controller():
    def __init__(self, **kwargs):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.renderer = kwargs['renderer']

        self._touches = []

        Internet(function = self.listener)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print keycode
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
        elif keycode[1] == 'q':
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

    def listener(self, data):
        if (data[0] == 'setRotationX'):
            self.setRotationX(data[1])
        elif (data[0] == 'setRotationY'):
            self.setRotationY(data[1])
        elif (data[0] == 'rotate'):
            self.rotate(data[1], data[2])
        elif (data[0] == 'setZoom'):
            self.setZoom(data[1])
        elif (data[0] == 'zoom'):
            self.zoom(data[1])
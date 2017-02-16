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

        return True     

    def rotate(self, rotX, rotY):
        self.renderer.rotx.angle += rotX
        self.renderer.roty.angle += rotY

    def setRotation(self, x, y):
        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y


    def listener(self, data):
        if (data[0] == 's'):
            self.setRotation(data[1], data[2])


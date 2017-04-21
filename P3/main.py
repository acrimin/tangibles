import sys

if (sys.argv[1] == "vertical"):
	dial = 0
else:
	from subprocess import Popen
	Popen(["python", "tray.py"])
	dial = 300

from kivy.config import Config
from win32api import GetSystemMetrics
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)
Config.set('graphics', 'height', height-dial)
Config.set('graphics', 'width', width)

from kivy.app import App

from ui import UI
from controller import Controller
from renderer import Renderer
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *


class Application(App):

    def build(self):  
        displayType = sys.argv[1]
        renderer = Renderer()
        controller = Controller(renderer = renderer)
        ui = UI(renderer = renderer, controller = controller, screenType = displayType)
        controller.setUI(ui)

        return ui

if __name__ == "__main__":
    Application().run()

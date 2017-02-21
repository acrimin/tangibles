# from kivy.config import Config
# from win32api import GetSystemMetrics
# width = GetSystemMetrics(0)
# height = GetSystemMetrics(1)
# dial = 300
# Config.set('graphics', 'borderless', 1)
# Config.set('graphics', 'resizable', 0)
# Config.set('graphics', 'position', 'custom')
# Config.set('graphics', 'left', 0)
# Config.set('graphics', 'top', 0)
# Config.set('graphics', 'height', height-dial)
# Config.set('graphics', 'width', width)

from kivy.app import App

from ui import UI
from controller import Controller
from renderer import Renderer

class Application(App):
    def build(self):  
        renderer = Renderer()

        controller = Controller(renderer = renderer)

        ui = UI(renderer = renderer, 
                controller = controller)        

        return ui

if __name__ == "__main__":
    Application().run()

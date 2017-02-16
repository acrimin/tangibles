from kivy.config import Config
Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)
Config.set('graphics', 'height', 1500-300)
Config.set('graphics', 'width', 2250)

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

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

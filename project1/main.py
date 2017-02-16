from kivy.app import App

from ui import UI
from controller import Controller
from renderer import Renderer
from myKnob import MyKnob
        
class Application(App):
    def build(self):  
        # controller = None     
        knob = MyKnob(
            size = (300, 300),
            min = 0, max = 360,
            step = 1,
            show_marker = True,
            knobimg_source = "img/knob_metal.png",
            marker_img = "img/bline.png",
            markeroff_color = (0.3, 0.3, .3, 1),
            pattern_id= 99, #(ids 1 to 8, or 99 for no id)
            debug = False,
            obj = None) #controller) # Passes the object to the knob

        renderer = Renderer()

        controller = Controller(
            knob = knob, 
            renderer = renderer)
    
        ui = UI(
            knob = knob, 
            renderer = renderer, 
            controller = controller)        

        return ui       

if __name__ == "__main__":
    Application().run()

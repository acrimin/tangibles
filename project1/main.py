from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from renderer import Renderer
from myKnob import MyKnob

from kivy.config import Config

    
class UI(AnchorLayout):
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.controller = kwargs['controller']

        anchor_top = AnchorLayout(anchor_x = 'center',
                                  anchor_y = 'top')        
        anchor_top.add_widget(kwargs['renderer'])
        self.add_widget(anchor_top)

        anchor_bot = AnchorLayout(anchor_x = 'right',
                                  anchor_y = 'bottom')
        anchor_bot.add_widget(kwargs['knob'])
        self.add_widget(anchor_bot)

        self._touches = []

    def define_rotate_angle(self, touch):
        x_angle = (touch.dx/self.width)*360
        y_angle = -1*(touch.dy/self.height)*360
        return x_angle, y_angle  

    def on_touch_down(self, touch):
        self._touch = touch
        touch.grab(self)
        self._touches.append(touch)
        
    def on_touch_up(self, touch): 
        touch.ungrab(self)
        self._touches.remove(touch)
        
    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                ax, ay = self.define_rotate_angle(touch)
                self.controller.rotate(ax, ay)

        

class Controller():
    def __init__(self, **kwargs):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.renderer = kwargs['renderer']
        self.knob = kwargs['knob']

        self._touches = []

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

        return True     

    def rotate(self, rotX, rotY):
        self.renderer.rotx.angle += rotX
        self.renderer.roty.angle += rotY

    def setRotation(self, x, y):
        self.renderer.rotx.angle = x
        self.renderer.roty.angle = y

class Application(App):
    def build(self):       
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
            obj = None) # Passes the object to the knob

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

from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scatter import Scatter

from myKnob import MyKnob

class UI(AnchorLayout):
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.controller = kwargs['controller']

        top = RenderPart(anchor_x = 'center',
                         anchor_y = 'top',
                         renderer = kwargs['renderer'],
                         controller = self.controller)
        self.add_widget(top)

        bot = DialPart(anchor_x = 'right',
                       anchor_y = 'bottom',
                       controller = self.controller)
        self.add_widget(bot)

class DialPart(AnchorLayout):
    def __init__(self, **kwargs):
        super(DialPart, self).__init__(**kwargs)

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
            obj = Scatter(),
            controller = kwargs['controller'])

        self.add_widget(knob)
   

class RenderPart(AnchorLayout):
    def __init__(self, **kwargs):
        super(RenderPart, self).__init__(**kwargs)
        self.controller = kwargs['controller']
        self.renderer = kwargs['renderer']
        self.add_widget(self.renderer)
        self._touches = []

    def define_rotate_angle(self, touch):
        x_angle = (touch.dx/self.width)*360
        y_angle = -1*(touch.dy/self.height)*360
        return x_angle, y_angle  

    def on_touch_down(self, touch):
        if touch.y > 310:
            self._touch = touch
            touch.grab(self)
            self._touches.append(touch)
        
    def on_touch_up(self, touch): 
        if touch in self._touches:
            touch.ungrab(self)
            self._touches.remove(touch)
        
    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                ax, ay = self.define_rotate_angle(touch)
                self.controller.rotate(ax, ay)
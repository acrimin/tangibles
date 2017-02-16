from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout

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
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button

class UI(FloatLayout):
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.controller = kwargs['controller']

        self.controller = kwargs['controller']
        self.renderer = kwargs['renderer']
        self.add_widget(self.renderer)
        self._touches = []

        self.scatterHeight = 500
        self.scatterWidth = 300
        self.scatter = None

    def closePopup(self, press):
        self.remove_widget(self.scatter)
        self.scatter = None

    def popup(self, pageNum):
        if (self.scatter):
            self.remove_widget(self.scatter)
        
        self.scatter = Scatter(do_rotation=False, do_scale=False)

        grid = BoxLayout(orientation='vertical',
            size_hint=(None,None),
            height=self.scatterHeight,
            width=self.scatterWidth)

        if (pageNum == 0):
            label = Label(text="Frontal Lobe",font_size='20sp')
            grid.add_widget(label)
            image = Image(source="img/frontal_lobe.jpg")
            grid.add_widget(image)
            label1 = Label(size_hint_y=None, 
                text_size=(self.scatterWidth,None), 
                text="The frontal lobe plays a large role in voluntary movement. It houses the primary motor cortex which regulates activities like walking.")
            grid.add_widget(label1)
        elif (pageNum == 1):
            label = Label(text="Occipital Lobe",font_size='20sp')
            grid.add_widget(label)
            image = Image(source="img/occipital_lobe.jpg")
            grid.add_widget(image)
            label1 = Label(size_hint_y=None, 
                text_size=(self.scatterWidth,None), 
                text="The occipital lobe is divided into several functional visual areas. Each visual area contains a full map of the visual world. Although there are no anatomical markers distinguishing these areas (except for the prominent striations in the striate cortex), physiologists have used electrode recordings to divide the cortex into different functional regions.")
            grid.add_widget(label1)
        elif (pageNum == 2):
            label = Label(text="Temporal Lobe",font_size='20sp')
            grid.add_widget(label)
            image = Image(source="img/temporal_lobe.jpg")
            grid.add_widget(image)
            label1 = Label(size_hint_y=None, 
                text_size=(self.scatterWidth,None), 
                text="The temporal lobe is involved in processing sensory input into derived meanings for the appropriate retention of visual memory, language comprehension, and emotion association.")
            grid.add_widget(label1)
        elif (pageNum == 3):
            label = Label(text="Parietal Lobe",font_size='20sp')
            grid.add_widget(label)
            image = Image(source="img/parietal_lobe.jpg")
            grid.add_widget(image)
            label1 = Label(size_hint_y=None, 
                text_size=(self.scatterWidth,None), 
                text="The parietal lobe integrates sensory information among various modalities, including spatial sense and navigation (proprioception), the main sensory receptive area for the sense of touch (mechanoreception) in the somatosensory cortex which is just posterior to the central sulcus in the postcentral gyrus,[1] and the dorsal stream of the visual system.")
            grid.add_widget(label1)
        
        space = Label(size_hint=(None,None),size=(self.scatterWidth,30))
        grid.add_widget(space)

        btn = Button(text="Close",size_hint=(None,None),size=(self.scatterWidth,50), on_press=self.closePopup)
        grid.add_widget(btn)

        self.scatter.add_widget(grid)
        self.add_widget(self.scatter)

    def define_rotate_angle(self, touch):
        x_angle = (touch.dx/self.width)*360
        y_angle = -1*(touch.dy/self.height)*360
        return x_angle, y_angle  

    def _within(self,touch):
        if (self.scatter != None and len(self._touches) == 0):
            if (touch.x > self.scatter.x and 
                    touch.x < self.scatter.x + self.scatterWidth and
                    touch.y > self.scatter.y and
                    touch.y < self.scatter.y + self.scatterHeight):
                return True
        return False



    def on_touch_down(self, touch):
        if (self._within(touch)):
            super(UI, self).on_touch_down(touch)
        else:
            self._touch = touch
            touch.grab(self)
            self._touches.append(touch)
        
    def on_touch_up(self, touch):
        if (self._within(touch)):
            super(UI, self).on_touch_up(touch)
        elif touch in self._touches:
            touch.ungrab(self)
            self._touches.remove(touch)
        
    def on_touch_move(self, touch):
        if (self._within(touch)):
            super(UI, self).on_touch_move(touch)
        elif touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                ax, ay = self.define_rotate_angle(touch)
                self.controller.rotate(ay, ax)


            elif len(self._touches) == 2: # scaling here
                #use two touches to determine do we need scal
                touch1, touch2 = self._touches 
                old_pos1 = (touch1.x - touch1.dx, touch1.y - touch1.dy)
                old_pos2 = (touch2.x - touch2.dx, touch2.y - touch2.dy)
                
                old_dx = old_pos1[0] - old_pos2[0]
                old_dy = old_pos1[1] - old_pos2[1]
                
                old_distance = (old_dx*old_dx + old_dy*old_dy)
                
                new_dx = touch1.x - touch2.x
                new_dy = touch1.y - touch2.y
                
                new_distance = (new_dx*new_dx + new_dy*new_dy)
                
                SCALE_FACTOR = 0.01
                
                if new_distance > old_distance: 
                    scale = SCALE_FACTOR
                elif new_distance == old_distance:
                    scale = 0
                else:
                    scale = -1*SCALE_FACTOR
                
                if scale:
                    self.controller.zoom(scale)

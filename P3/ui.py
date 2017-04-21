
import kivy
from kivy.app import App
from kivy.properties     import *
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.animation     import * 
from kivy.uix.videoplayer import Video
from kivy.uix.button     import Button
from functools import partial

# Import kivy osc library
from kivy.lib.osc         import oscAPI 
# Import clock (required by osc listener)
from kivy.clock           import Clock

class UI(FloatLayout):
    vid_state = 0
    vidLength = 141.0 # in seconds
    start = 0
    stop = 0
    vid_pos = (720,200)

    self.controller = kwargs['controller']

    def sendVid(self, start, stop, value):
        oscAPI.sendMsg('/tuios/video', [start, stop, value], 
                    ipAddr= self.controller.sendip, 
                    port= 5000) 

    def playVideo(self, start, stop, value):
        self.start = start
        self.stop = stop
        try:
            if self.vid_state == 0:
                self.renderer.opacity = 0

                #play video
                self.vid1_scatter.pos = self.vid_pos
                self.video.opacity = 1
                self.video.play = True
                self.video.seek(float(self.start/self.vidLength))
                self.vid_state = 1

            else:
                #stop video
                self.video.opacity = 0
                self.video.play = False
                self.vid_state = 0
                self.renderer.opacity = 1
        except:
            if self.vid_state == 0:

                #play video
                self.vid1_scatter.pos = self.vid_pos
                self.video.opacity = 1
                self.video.play = True
                self.video.seek(float(self.start/self.vidLength))
                self.vid_state = 1

            else:
                #stop video
                self.video.opacity = 0
                self.video.play = False
                self.vid_state = 0

    def cb_seek(self, instance, value):
        if value > self.stop:
            #stop video
            self.video.opacity = 0
            self.video.play = False
            self.vid_state = 0
            try:
                self.renderer.opacity = 1
            except:
                pass

    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.screenType = kwargs['screenType']
        self.controller = kwargs['controller']

        self.background = Image(source='img/Blue-Background.jpg', 
            size_hint = (1, 1), 
            allow_stretch = True,
            keep_ratio = False)
        self.add_widget(self.background)

        self.controller = kwargs['controller']
        self.renderer = kwargs['renderer']
        #self.renderer.pos = (1500, 1500)

        # Defining colors
        # use a (r, g, b, a) tuple (a = alpha channel = tranparency)
        self.grey = (0.5, 0.5, 0.5, 1)
        self.black = (0, 0, 0, 1)

        # instantiate the labels
        self.label1 =  Label(text="3-D Brain Model", font_size=250, color=self.black, font_name='fonts/Living Hell.ttf')
        self.label1Wid = Widget(pos = (0,0), size=(self.label1.size))
        if self.screenType == "horizontal":
            self.label1.pos=(self.width+1000, self.height+850)
        else:
            self.label1.pos=(self.width+1000, self.height+1150)
            self.label1.font_size=300
        self.label1Wid.add_widget(self.label1)

        self.label2 =  Label(text="Rotate X", font_size=50, bold = True, color=self.grey, pos=(self.width+1320, 0))
        self.label2Wid = Widget(pos = (0, 0), size=(self.label2.size))
        if self.screenType == "horizontal":
            self.label2.opacity = 1
        else:
            self.label2.opacity = 0
        self.label2Wid.add_widget(self.label2)

        self.label3 =  Label(text="Rotate Y", font_size=50, bold = True, color=self.grey, pos=(self.width+1640, 0))
        if self.screenType == "horizontal":
            self.label3.opacity = 1
        else:
            self.label3.opacity = 0
        self.label3Wid = Widget(pos = (0, 0), size=(self.label3.size))
        self.label3Wid.add_widget(self.label3)

        self.label4 =  Label(text="Zoom", font_size=50, bold = True, color=self.grey, pos=(self.width+1940, 0))
        if self.screenType == "horizontal":
            self.label4.opacity = 1
        else:
            self.label4.opacity = 0
        self.label4Wid = Widget(pos = (0, 0), size=(self.label4.size))
        self.label4Wid.add_widget(self.label4)

        # Basic facts about the brain
        self.widget1 = Widget(pos = (0, 0), size=(300, 300))
        button1 = Button(background_normal='Tile1/Vid-2.png', size=self.widget1.size, pos = self.widget1.pos)
        button1.bind(on_press=partial(self.sendVid, 0, 12))
        self.widget1.add_widget(button1)

        # weight of brain
        self.widget2 = Widget(pos = (0, 300), size=(300, 300))
        button2 = Button(background_normal='Tile1/Vid-3.png', size=self.widget2.size, pos = self.widget2.pos)
        button2.bind(on_press=partial(self.playVideo, 13, 21))
        self.widget2.add_widget(button2)
        
        # Brain is protected by bones, meninges, and spinal fluid
        self.widget3 = Widget(pos = (0, 0), size=(300, 300))
        button3 = Button(background_normal='Tile1/Vid-4.png', size=self.widget3.size, pos = (0, 300))
        button3.bind(on_press=partial(self.playVideo, 22, 33))
        self.widget3.add_widget(button3)
        
        # brain has 3 parts: fore brain, mid brain, and hind brain
        self.widget4 = Widget(pos = (0, 0), size=(300, 300))
        button4 = Button(background_normal='Tile1/Vid-5.png', size=self.widget4.size, pos = (0, 300))
        button4.bind(on_press=partial(self.playVideo, 34, 41))
        self.widget4.add_widget(button4)

        ########################### 6 6 6
        # Fore brain
        self.widget5 = Widget(pos = (0, 0), size=(300, 300))
        button5 = Button(background_normal='Tile1/Vid-6.png', size=self.widget5.size, pos = (0, 300))
        button5.bind(on_press=partial(self.playVideo, 41, 61))
        self.widget5.add_widget(button5)
        
        # The Cerebrum...
        self.widget6 = Widget(pos = (0, 0), size=(300, 300))
        button6 = Button(background_normal='Tile1/Vid-7.png', size=self.widget6.size, pos = (0, 300))
        button6.bind(on_press=partial(self.playVideo, 61, 78))
        self.widget6.add_widget(button6)
        
        ########################### 8 8 8
        # Mid brain
        self.widget7 = Widget(pos = (0, 0), size=(300, 300))
        button7 = Button(background_normal='Tile1/Vid-8.png', size=self.widget7.size, pos = (0, 300))
        button7.bind(on_press=partial(self.playVideo, 78, 89))
        self.widget7.add_widget(button7)

        ########################### 9 9 9
        # Hind brain
        self.widget8 = Widget(pos = (0, 0), size=(300, 300))
        button8 = Button(background_normal='Tile1/Vid-9.png', size=self.widget8.size, pos = (0, 300))
        button8.bind(on_press=partial(self.playVideo, 89, 89))
        self.widget8.add_widget(button8)
        
        # Cerebellum... balance, movements, coordination
        self.widget9 = Widget(pos = (0, 0), size=(300, 300))
        button9 = Button(background_normal='Tile1/Vid-10.png', size=self.widget9.size, pos = (0, 300))
        button9.bind(on_press=partial(self.playVideo, 96, 106))
        self.widget9.add_widget(button9)
        
        # Pons and Medulla / midbrain .. breathing, heart rate, blood pressure, swallowing, digestion, and blinking
        self.widget10 = Widget(pos = (0, 0), size=(300, 300))
        button10 = Button(background_normal='Tile1/Vid-11.png', size=self.widget10.size, pos = (0, 300))
        button10.bind(on_press=partial(self.playVideo, 106, 126))
        self.widget10.add_widget(button10)

        ########################### 12 12 12 
        # Different centres of our brain -- video summary
        widget11 = Widget(pos = (0, 0), size=(300, 300))
        button11 = Button(ackground_normal='Tile1/Vid-12.png', size=widget11.size, pos = (0, 300))
        button11.bind(on_press=partial(self.playVideo, 126, 126))
        widget11.add_widget(button11)

        self.video = Video(size = (800,800), pos=(0,0), volume=1.0, 
                         options={'eos': 'loop'}, allow_stretch = True,
            keep_ratio = True, opacity =0)
        self.video.source = 'Tile1/Tile1-Vid.mp4' 
        self.video.play = False
        self.video.bind(position=self.cb_seek)

        #Creates a widget to add the vid_scatter to
        self.vid1_wid = Widget()
        # Creates a scatter widget
        self.vid1_scatter = Scatter(size=(800, 800), pos=self.vid_pos)
        # Adds image to the scatter, and the scatter to the widget
        self.vid1_scatter.add_widget(self.video)
        self.vid1_wid.add_widget(self.vid1_scatter)

        if self.screenType == "vertical":
            self.add_widget(self.vid1_wid)
            self.add_widget(self.renderer)
        else:
            self.video.volume = 0
            # Button widgets
            self.add_widget(self.widget1)
            self.add_widget(self.widget2)

        # add label widgets to the main layout 
        self.add_widget(self.label1Wid)
        self.add_widget(self.label2Wid)
        self.add_widget(self.label3Wid)
        self.add_widget(self.label4Wid)

        self._touches = []

        self.scatterHeight = 500
        self.scatterWidth = 300
        self.scatter = None

    def closePopup(self, press):
        self.remove_widget(self.scatter)
        self.scatter = None
    '''
    def popup(self, pageNum):
        if (self.scatter):
            self.remove_widget(self.scatter)
        
        self.scatter = Scatter(do_rotation=False, do_scale=False)

        grid = BoxLayout(orientation='vertical',
            size_hint=(None,None),
            height=self.scatterHeight,
            width=self.scatterWidth)

        if (pageNum == 0):
            label5 = Label(text="Frontal Lobe",font_size='35sp', font_name='fonts/Voces-Regular.ttf', pos=(0, 300))
            label5Wid = Widget()
            label5Wid.add_widget(label5)
            grid.add_widget(label5Wid)

            image = Image(source="img/frontal_lobe.jpg")
            grid.add_widget(image)
            label6 = Label(size_hint_y=None, 
                text_size=(self.scatterWidth,None), 
                font_size='22sp',
                pos=(100, 100),
                font_name='fonts/Voces-Regular.ttf',
                text="The frontal lobe plays a large role in voluntary movement. It houses the primary motor cortex which regulates activities like walking.")
            label6Wid = Widget()
            label6Wid.add_widget(label6)
            grid.add_widget(label6Wid)

        elif (pageNum == 1):
            label5 = Label(text="Occipital Lobe",font_size='35sp', font_name='fonts/Voces-Regular.ttf', pos=(0, 300))
            grid.add_widget(label5)
            label5Wid = Widget()
            label5Wid.add_widget(label5)
            grid.add_widget(label5Wid)

            image = Image(source="img/occipital_lobe.jpg")
            grid.add_widget(image)
            label6 = Label(size_hint_y=None, 
                text_size=(self.scatterWidth,None), 
                font_size='22sp',
                pos=(100, 100),
                font_name='fonts/Voces-Regular.ttf',
                text="The occipital lobe is divided into several functional visual areas. Each visual area contains a full map of the visual world. Although there are no anatomical markers distinguishing these areas (except for the prominent striations in the striate cortex), physiologists have used electrode recordings to divide the cortex into different functional regions.")
            label6Wid = Widget()
            label6Wid.add_widget(label6)
            grid.add_widget(label6Wid)

        elif (pageNum == 2):
            label5 = Label(text="Temporal Lobe",font_size='35sp', font_name='fonts/Voces-Regular.ttf', pos=(0, 300))
            grid.add_widget(label5)
            label5Wid = Widget()
            label5Wid.add_widget(label5)
            grid.add_widget(label5Wid)

            image = Image(source="img/temporal_lobe.jpg")
            grid.add_widget(image)
            label6 = Label(size_hint_y=None, 
                text_size=(self.scatterWidth,None), 
                font_size='22sp',
                pos=(100, 100),
                font_name='fonts/Voces-Regular.ttf',
                text="The temporal lobe is involved in processing sensory input into derived meanings for the appropriate retention of visual memory, language comprehension, and emotion association.")
            label6Wid = Widget()
            label6Wid.add_widget(label6)
            grid.add_widget(label6Wid)

        elif (pageNum == 3):
            label5 = Label(text="Parietal Lobe",font_size='35sp', font_name='fonts/Voces-Regular.ttf', pos=(0, 300))
            grid.add_widget(label5)
            label5Wid = Widget()
            label5Wid.add_widget(label5)
            grid.add_widget(label5Wid)

            image = Image(source="img/parietal_lobe.jpg")
            grid.add_widget(image)
            label6 = Label(size_hint_y=None, 
                text_size=(self.scatterWidth,None), 
                font_size='22sp',
                pos=(100, 100),
                font_name='fonts/Voces-Regular.ttf',
                text="The parietal lobe integrates sensory information among various modalities, including spatial sense and navigation (proprioception), the main sensory receptive area for the sense of touch (mechanoreception) in the somatosensory cortex which is just posterior to the central sulcus in the postcentral gyrus,[1] and the dorsal stream of the visual system.")
            label6Wid = Widget()
            label6Wid.add_widget(label6)
            grid.add_widget(label6Wid)
        
        space = Label(size_hint=(None,None),size=(self.scatterWidth,30))
        grid.add_widget(space)

        btn = Button(text="Close",size_hint=(None,None),size=(self.scatterWidth,50), on_press=self.closePopup)
        grid.add_widget(btn)

        self.scatter.add_widget(grid)
        self.add_widget(self.scatter)
        '''

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
            print "first elif"
            super(UI, self).on_touch_down(touch)
        else:
            print "else statement"
            self._touch = touch
            touch.grab(self)
            self._touches.append(touch)
            super(UI, self).on_touch_down(touch)
        
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

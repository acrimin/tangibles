###Sample Kivy program (kivy.org)
### Alexandre Siqueira, Clemson
### February, 2017
#########################################
#04 - knob_API
#tangible knob API - object rotation
#########################################

import kivy
from kivy.app import App
from kivy.properties     import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter    import Scatter
from kivy.uix.image      import Image

# Import kivy osc library
from kivy.lib.osc         import oscAPI 
# Import clock (required by osc listener)
from kivy.clock           import Clock

class ReceiverApp(App):
    # Set ip and port to listen to
    ip = '0.0.0.0' # listens to any sender IP
    port = 5000    # listens only to this port

    def build(self):
        # Starts OSC
        oscAPI.init()  
        # Instanciates OSC listener
        oscid = oscAPI.listen(ipAddr=self.ip, port= self.port) 
        # listens for osc messages every screen refresh
        Clock.schedule_interval(lambda *x: oscAPI.readQueue(oscid), 0)

        # binds messages - this listens to messages if prefix /1/tok
        oscAPI.bind(oscid, self.cb_tok, '/tuios/tok')

        # creates a grid layout with two columns
    	root = GridLayout(cols = 3, spacing = 50, padding = 30)

        # Creates an image widget
        image1 = Image(source='img/bunny.jpg', size = (300,300))
        image2 = Image(source='img/bunny.jpg', size = (300,300))
        image3 = Image(source='img/bunny.jpg', size = (300,300))

        # Creates a scatter widget
        self.scatter1 = Scatter()
        # Adds image widget to the scatter
        self.scatter1.add_widget(image1)

        self.scatter2 = Scatter()
        self.scatter2.add_widget(image2)
        self.scatter3 = Scatter()
        self.scatter3.add_widget(image3)

        # Adds scatter to the root
        root.add_widget(self.scatter1)
        root.add_widget(self.scatter2)
        root.add_widget(self.scatter3)
        return root

    #OSC callback function
    def cb_tok(self, value, instance): 
        # print message received to console
        print "Message received: " + str(value)

        if value[2] == 1:
            self.scatter1.rotation = value[7]
        elif value[2] == 2:
            try:
                self.scatter2.opacity = float(value[7])/360
            except:
                self.scatter2.opacity = 1

        elif value[2] == 3: 
            try:
                self.scatter3.scale = (float(value[7]) /180) + 0.01
            except:
                self.scatter3.scale = 1



ReceiverApp().run()
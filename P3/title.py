from kivy.config import Config

width = 300
height = 150
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'height', height)
Config.set('graphics', 'width', width)


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image      import Image
from subprocess import Popen


class StartMenu(App):
    def build(self): 
        box = BoxLayout(orientation="vertical")
        box.add_widget(Label(text_size=(width,None),
            text="Enter IP Address and Select Display Type"))

        spaceBox = BoxLayout(orientation="horizontal")
        spaceBox.add_widget(Widget(size_hint=(None,None),size=(5,5)))
        self.text = TextInput(multiline=False,font_size="20sp",size_hint_y=None,size=(10,40))
        spaceBox.add_widget(self.text)
        spaceBox.add_widget(Widget(size_hint=(None,None),size=(5,5)))
        box.add_widget(spaceBox)

        box.add_widget(Widget(size_hint=(None,None),size=(10,10)))
        buttonBox = BoxLayout(orientation="horizontal",spacing=5)

        btn1 = Button(text="Vertical", on_press=self.btn1)
        btn2 = Button(text="Horizontal", on_press=self.btn2)
        buttonBox.add_widget(btn1)
        buttonBox.add_widget(btn2)
        box.add_widget(buttonBox)

        return box
    #----------------------------
    # modified by Sarah:
    def btn1(self, touch):
        global displayType
        global ipAddress
        if (self.text.text != ""):
            displayType = "vertical"
            ipAddress = self.text.text
            print self.text.text
            App.get_running_app().stop()
        # if the user does not specify IP Address, assume the local IP Address
        else:
            displayType = "vertical"
            ipAddress = "127.0.0.1"
            print "127.0.0.1"
            App.get_running_app().stop()

    def btn2(self, touch):
        global displayType
        global ipAddress
        if (self.text.text != ""):
            displayType = "horizontal"
            ipAddress = self.text.text
            App.get_running_app().stop()
        # if the user does not specify IP Address, assume the local IP Address
        else:
            displayType = "horizontal"
            ipAddress = "127.0.0.1"
            print "127.0.0.1"
            App.get_running_app().stop()
    #----------------------------

if __name__ == "__main__":
    StartMenu().run()
    Popen(["python", "main.py", displayType, ipAddress])


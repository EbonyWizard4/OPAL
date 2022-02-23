

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from iqoptionapi.stable_api import IQ_Option
from kivy.properties import NumericProperty


class Manager(ScreenManager):
    pass

class Trade(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for a in a:
            self.ids.box.add_widget(Texto())


class Texto(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.Texto.text='Mudei o Texto'
    

class MyApp(App):

    def build(self):
        return Manager()


if __name__ == '__main__':
    MyApp().run()


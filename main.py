
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty

class Manager(ScreenManager):
    pass

class TelaBotao(Screen):
    def pop_up(self):
        popup = Popup(title = 'meu pop up', content = Label(text = 'Aee!'))
        popup.open()
        
class MyTxt(TextInput):
    max_characters = NumericProperty(1)

    def insert_text(self, substring, from_undo=False):

        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ''
        TextInput.insert_text(self, substring, from_undo)
        if int(self.text) > 23:
            self.parent.parent.pop_up()
class MyAPP(App):
    def build(self):
        return Manager()

MyAPP().run()
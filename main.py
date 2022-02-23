
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class Manager(ScreenManager):
    pass

class TelaBotao(Screen):
    def pop_up(self):
        popup = Popup(title = 'meu pop up', content = Label(text = 'Aee!'))
        popup.open()
        
class MyTxt(TextInput):
    def insert_text(self, substring, from_undo=False):
        txt = int(self.text)
        print(txt)
        if txt > 2:
            substring = self.parent.parent.pop_up()
        TextInput.insert_text(self, substring, from_undo)

class MyAPP(App):
    def build(self):
        return Manager()

MyAPP().run()
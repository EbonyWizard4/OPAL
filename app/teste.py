from distutils.command.build import build
import imp
import kivy
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from functools import partial
from datetime import datetime

class Tela(App):
    def build(self):
        return Gerenciador()

class Gerenciador(ScreenManager):
    pass

class Tela1(Screen):
    def achei(self):
        print('achei Tla 1')
    pass

class Tela2(Screen):
    def achei(self):
        print('achei Tla 2')
    pass

class Tela3(Screen):
    def achei(self):
        print('achei Tla 3')
    pass

Tela().run()

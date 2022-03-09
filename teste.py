from distutils.command.build import build
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

class Tela(BoxLayout):
    pass

class MeuTeste(App):
    def build(self):
        return Tela()

MeuTeste().run()
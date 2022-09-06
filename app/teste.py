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

class Gerenciador(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.sinal=[]
        self.chave = 1

    
    def contar(self, chave = 0):

        chave += 1
        return chave

    def agendar(self):
        self.agendado = []
        print(self.chave)
        self.sinal.append(Clock.schedule_once(self.imprimir, 10))
        print('agendar está funcionando!')
        for item in enumerate(self.sinal):
            self.agendado.append(datetime.now())
        print('foi agendado: \n',self.agendado)
        self.chave = self.contar(self.chave)

    def excluir(self, chave=0):
        Clock.unschedule(self.sinal[1])

    def imprimir(self,*args):
        print("imprimir está funcionando",datetime.now())

Tela().run()

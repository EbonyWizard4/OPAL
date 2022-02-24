
import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

from botSinais import Robo

import json

class Gerenciador(ScreenManager):
    pass

class TelaApp(Screen):
    def on_pre_enter(self):
        self.nome, self.banca = OPAL().perfil()
        self.ids.Usuario.text = self.nome
        self.ids.Banca.text = self.banca

class TelaLogin(Screen):
    def login(self):
        self.parent.current = 'TelaApp'
        # self.email = str(self.ids.Login.text)
        # self.senha = str(self.ids.Senha.text)
        # self.login = OPAL().login(self.email, self.senha)
        # if self.login == True:
        #     self.parent.current = 'TelaApp'
        # else:
        #     print('Errou chama o Pop-Up')       
        
class TelaMenu(Screen):
    def sinais(self):
        self.parent.current = 'TelaSinais'
    
    def trade(self):
        self.parent.current = 'TelaTrade'
    
class TelaSinais(Screen):
    def pop_up(self):
        box = BoxLayout(orientation = 'vertical', padding = 20, spacing = 10)
        popup = Popup(title = 'Horário Invalido!', content = box, size_hint = (None, None), size = (400,200))
        box.add_widget(Label(text = 'Por favor insira um horário que seja valido!'))
        box.add_widget(Button(text = 'OK', on_release = popup.dismiss))
        popup.open()
        

    def insere_sinal(self):
        self.sinal = []
        OPAL().insere_sinal(self.sinal)
    
    def menu(self):
        self.parent.current = 'TelaMenu'
    
    def trade(self):
        self.parent.current = 'TelaTrade'

class TelaTrade(Screen):
    def sinais(self):
        self.parent.current = 'TelaSinais'
        
    def menu(self):
        self.parent.current = 'TelaMenu'

class SinalTrade(BoxLayout):
    pass

class MyTextInput_Hora(TextInput):
    max_characters = NumericProperty(1)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ''
        TextInput.insert_text(self, substring, from_undo)
        if int(self.text) > 23:
            TelaSinais().pop_up()
            self.text = ''

class MyTextInput_Minuto(TextInput):
    max_characters = NumericProperty(1)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ''
        TextInput.insert_text(self, substring, from_undo)
        if int(self.text) > 59:
            TelaSinais().pop_up()
            self.text = ''

class MyTextInput(TextInput):
    pass


class OPAL(App):
    API = Robo()
    def build(self):
        return Gerenciador()
    
    def login(self, email, senha):
        self.login = self.API.singin(self.email, self.senha)
        return True if self.login else False
    
    def perfil(self):
        self.nome, self.banca = self.API.perfil()
        return self.nome, self.banca
    
    def insere_sinal(self, sinal):
        self.pronto = self.API.insereSinal(sinal)
        return True if self.pronto == True else False

if __name__ == '__main__':
    OPAL().run()

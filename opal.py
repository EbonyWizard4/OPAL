

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
from datetime import datetime, timedelta

class Gerenciador(ScreenManager):
    pass

class TelaApp(Screen):
    def on_pre_enter(self):
        self.nome, self.banca = OPAL().perfil()
        self.ids.Usuario.text = self.nome
        self.ids.Banca.text = self.banca

class TelaLogin(Screen):
    def login(self):
        #
        self.email = str(self.ids.Login.text)
        self.senha = str(self.ids.Senha.text)
        if '@' in self.email:
            self.parent.current = 'TelaApp'
            #self.login = OPAL().login(self.email, self.senha)
        else:
            Pop_up().pop_up(
                'Erro ao efetuar o Login',
                'O e-mail informado não é valido,\nCorrija suas credenciais e tente novamente!'
            )
            
        if self.login == True:
            self.parent.current = 'TelaApp'
        else:
            Pop_up().pop_up(
                'Erro ao efetuar o Login',
                'Verifique sua conexão e tente novamente'
            )
        
        self.ids.Login.text = ''
        self.ids.Senha.text = ''
        
class TelaMenu(Screen):
    def sinais(self):
        self.parent.current = 'TelaSinais'
    
    def trade(self):
        self.parent.current = 'TelaTrade'
    
class TelaSinais(Screen):
    def salva_sinal(self):
        self.banca ='Treino'
        self.sinal =[
            self.ids.Hora.text + ':' + self.ids.Minuto.text,
            self.ids.Paridade.text,
            self.ids.Direcao.text,
            self.ids.Time_Frame.text,
            self.ids.Valor.text,
            self.banca
            ]
        
        if '' in self.sinal:
            Pop_up().pop_up(
                'Falha Ao inserir o Sinal',
                'Verifique se todos os campos foram \npreenchidos e tente novamente',
            )
        elif OPAL().insere_sinal(self.sinal) == True:
            Pop_up().pop_up(
                'Sucesso!',
                'Seu sinal foi inserido com sucesso!',
            )
        else:
            Pop_up().pop_up(
                'Falha Ao inserir o Sinal',
                'Verifique se todos os campos foram \npreenchidos e tente novamente',
            )
            
        
        
    pass
        

    def insere_sinal(self):
        self.sinal = []
        OPAL().insere_sinal(self.sinal)
    
    def menu(self):
        self.parent.current = 'TelaMenu'
    
    def trade(self):
        self.parent.current = 'TelaTrade'

class TelaTrade(Screen):
    def on_pre_enter(self, *args):
        self.sinais = OPAL().le_sinais()
        self.sinais = sorted(self.sinais)
        for self.sinal in self.sinais:
            self.ids.Lista.add_widget(SinalTrade(self.sinal))
        
    def sinais(self):
        self.parent.current = 'TelaSinais'

    def start(self):
        self.lista = OPAL().le_sinais()
        self.lista = sorted(self.lista)
        # self.now = datetime.now()
        self.now = datetime.strftime(datetime.now(), '%H:%M:%S')
        for sinal in self.lista:
            tempo = datetime.strptime(sinal[0] + ':00', '%H:%M:%S') - datetime.strptime(self.now, '%H:%M:%S')
            tempo = timedelta.total_seconds(tempo)
            if tempo <= 0:
                self.ids.Lista.remove_widget(self.ids.Lista.children[0])
            else:
                ordem = Clock.schedule_once(self.trade, tempo)
            # print(ordem)


    
    def trade(self,*args):
        OPAL().trade()
        self.ids.Lista.remove_widget(self.ids.Lista.children[0])
        
        
            
    def menu(self,**args):
        self.parent.current = 'TelaMenu'
    
    def on_pre_leave(self, *args):
        for widget in range(len(self.ids.Lista.children)):
            self.ids.Lista.remove_widget(self.ids.Lista.children[0])

class SinalTrade(BoxLayout):
    def __init__(self,sinal=[], **kwargs):
        super().__init__(**kwargs)
        for self.elemento in sinal:
            self.ids.box_sinal.add_widget(Label(text = str(self.elemento)))
            

    
    def exclui_sinal(self,sinal=[]):
        sinal.clear()
        for widget in range(len(self.ids.box_sinal.children)):
            sinal.append(self.ids.box_sinal.children[0].text)
            self.ids.box_sinal.remove_widget(self.ids.box_sinal.children[0])
        sinal = sinal[::-1]
        OPAL().exclui_sinal(sinal)
        self.parent.remove_widget(self)

class Pop_up(Popup):
    def pop_up(self, titulo, texto):
        box = BoxLayout(orientation = 'vertical', padding = 20, spacing = 10)
        popup = Popup(title = titulo, content = box, size_hint = (None, None), size = (400,200))
        box.add_widget(Label(text = texto))
        box.add_widget(Button(text = 'OK', on_release = popup.dismiss))
        popup.open()
    
class MyTextInput_Hora(TextInput):
    max_characters = NumericProperty(1)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ''
        TextInput.insert_text(self, substring, from_undo)
        if int(self.text) > 23:
            Pop_up().pop_up('Horario Invalido!', 'Corrija o capo horário e tente novamente!')
            self.text = ''

class MyTextInput_Minuto(TextInput):
    max_characters = NumericProperty(1)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ''
        TextInput.insert_text(self, substring, from_undo)
        if int(self.text) > 59:
            Pop_up().pop_up('Horario Invalido!', 'Corrija o capo minutos e tente novamente!')
            self.text = ''

class MyTextInput(TextInput):
    pass

class OPAL(App):
    API = Robo()
    def build(self):
        return Gerenciador()
    
    def login(self, email, senha):
        self.login = True #self.API.singin(email, senha)
        return True if self.login else False
    
    def perfil(self):
        self.nome, self.banca = 'Jhone Antonio', '10.000'#self.API.perfil()
        return self.nome, self.banca
    
    def insere_sinal(self, sinal):
        self.sinal = self.API.insere_sinal(sinal)
        return self.sinal
    
    def le_sinais(self):
        self.sinais = self.API.le_sinais()
        return self.sinais
    
    def exclui_sinal(self, sinal):
        self.API.exclui_sinal(sinal)

    def trade(self):
        self.API.trade()

if __name__ == '__main__':
    OPAL().run()

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
from functools import partial

#Gerencia a troca entre a tela login e a tela do app
class Gerenciador(ScreenManager):
    pass

#Recebe as credenciais e chama a rotina de login (7/7 funcionando)
class TelaLogin(Screen):
    #-> faz login
    def login(self):
        self.email = str(self.ids.Login.text)
        self.senha = str(self.ids.Senha.text)
        if '@' in self.email:
            self.API = OPAL().login(self.email, self.senha)
        else:
            Pop_up().pop_up(
                'Erro ao efetuar o Login',
                'O e-mail informado não é valido,\nCorrija suas credenciais e tente novamente!'
            )
            
        if self.API:
            self.parent.current = 'TelaApp'
        else:
            Pop_up().pop_up(
                'Erro ao efetuar o Login',
                'Verifique sua conexão e tente novamente'
            )
        
        self.ids.Login.text = ''
        self.ids.Senha.text = ''

#Exibe dados do usuári e as telas do app
class TelaApp(Screen):
    #-> carrega informações ao abrir a tela
    def on_pre_enter(self):
        self.nome, self.banca = OPAL().perfil()
        self.ids.Usuario.text = self.nome
        self.ids.Banca.text = self.banca    
        self.ordens = [] #-> cria uma lista     

# Contem botões de acesso as telas do app
class TelaMenu(Screen):
    #-> muda para tela sinais
    def sinais(self):
        self.parent.current = 'TelaSinais'
    
    #-> muda para tela de trade
    def trade(self):
        self.parent.current = 'TelaTrade'

#Recebe os dados do sinal e chama a rotina de salvamento
class TelaSinais(Screen):
    #-> define o número de gales
    def switch_gale(self):
        if self.ids.Gale1.active == True:
            self.ids.Gale2.disabled = False
            if self.ids.Gale2.active == True:
                self.gale = '2'
            else: 
                self.gale = '1'
        else:
            self.ids.Gale2.disabled = True
            self.gale = '0'
    
    #-> valida sinais antes de salvar
    def salva_sinal(self):
        sinais = OPAL().le_sinais()
        self.banca ='Treino'
        self.hora =  str(self.ids.Hora.text + ':' + self.ids.Minuto.text)
           
        self.sinal =[
            self.hora,
            self.ids.Paridade.text,
            self.ids.Direcao.text,
            self.ids.Time_Frame.text,
            self.ids.Valor.text,
            self.banca,
            self.gale
            ]
        
        if '' in self.sinal:
            Pop_up().pop_up(
                'Falha Ao inserir o Sinal!',
                'Verifique se todos os campos foram \npreenchidos e tente novamente.',
            )
        elif float(self.ids.Valor.text) < 0:
            Pop_up().pop_up(
                'Falha Ao inserir o Sinal!',
                'Verifique o campo valor \ne tente novamente.',
            )
            self.ids.Valor.text = '2.00'
        elif self.sinal in sinais:
            Pop_up().pop_up(
                'Falha Ao inserir o Sinal!',
                'Sinal já foi inserido na agenda!',
            )
        elif OPAL().insere_sinal(self.sinal) == True:
            Pop_up().pop_up(
                'Sucesso!',
                'Seu sinal foi inserido com sucesso!',
            )
            self.ids.Hora.text = '00'
            self.ids.Minuto.text = '00'
            self.ids.Valor.text = '2.00'
        else:
            Pop_up().pop_up(
                'Falha Ao inserir o Sinal!',
                'Verifique se todos os campos foram \npreenchidos e tente novamente.',
            )

    #-> tenta salvar o sinal e retorna True ou False
    def insere_sinal(self):
        self.sinal = []
        OPAL().insere_sinal(self.sinal)
    
    #-> muda para tela menu
    def menu(self):
        self.parent.current = 'TelaMenu'
    
    #- muda para tela de trade
    def trade(self):
        self.parent.current = 'TelaTrade'

# Exibe as informações dos trades programados e realizados 
# e chama a rotina de execução.
class TelaTrade(Screen):

    #-> quando a TelaTrade é chamada, le a lista de sinais e manda inserir na tela os sinais encontrados.
    def on_pre_enter(self, *args):
        print('on pré enter')
        self.sinais = self.le_sinais()
        self.insere_widget(self.sinais)
    
    #-> le os sinais da lista de sinais.
    def le_sinais(self):
        print('le sinais')
        self.sinais = OPAL().le_sinais()
        if self.sinais == []:
            Pop_up().pop_up(
                'Não há sinais na lista!',
                'Por favor insira um sinal e tente novamente!',
            )
            self.para_TelaSinais()
        return self.sinais

    #-> insere na tela os sinais.
    def insere_widget(self, sinais):
        print('insere widget')
        for sinal in sinais:
            self.ids.Lista.add_widget(SinalTrade(sinal))
                
    #-> troca para tela de inserir sinais
    def para_TelaSinais(self):
        print('para_tela_sinais()')
        self.parent.current = 'TelaSinais'
        self.cancelar_trade()
    
    #-> quando a TelaTrade é destruida, le os sinais que estão na tela e manda remover, evitando duplicidade de informação    
    def on_pre_leave(self, *args):
        print('On pré Leave')
        self.cancelar_trade()
        # self.limpa_lista()

    #-> limpa lista de trades na tela
    def limpa_lista(self):
        print('limpa_lista()')
        numero = len(self.ids.Lista.children)
        self.exclui_widget(numero)

    #-> remove os sinais que estão aparecendo na tela pela ordem de apresentação    
    def exclui_widget(self, numero):
        for widget in range(numero):
            self.ids.Lista.remove_widget(self.ids.Lista.children[-1])

    #-> pega a lista de sinais e a agenda, compara cada sinal com o que há na agenda, caso o sinal não esteja na agenda:
    #-> calcula o tempo que falta para a hora do sinal e agenda a execução do sinal, manda atualizar e mostrar a agenda.
    def start_trade(self):
        
        self.ordens = []

        #-> Agenda sinais
        for sinal in self.sinais:
            #-> calcula o tempo para execução do trade.
            self.tempo = self.calcular_tempo(sinal)
            #-> Agenda a execução do trade.
            self.agendar_trade(sinal)
            
        # self.mostra_agenda()
        # -> printa a hora de cada sinal
        # for ordem in self.ordens:
        #     print(ordem[1][0])
        print('start Trade!')
        
    #-> Calcular tempo
    def calcular_tempo(self, sinal) -> int:
        dia = 68400
        hora = datetime.strftime(datetime.now(), "%H:%M:%S") #-> captura a hora atual
        tempo = timedelta.total_seconds(
            datetime.strptime(
                sinal[0] + ':00', 
                '%H:%M:%S'
                ) - datetime.strptime(
                hora, 
                '%H:%M:%S'
            )
        ) - 1
        if tempo <= 0:
            tempo = tempo + dia
        else:
            pass
        return tempo

    #-> agenda a execução do trade, insere o tempo na cinal agendado, salva na agenda.
    def agendar_trade(self, sinal):

        ordem = Clock.schedule_once(partial(self.realiza_trade, sinal), self.tempo), sinal
        TelaApp().ordens.append(ordem)
        # print(self.ordens[0][1])
        # sinal = sinal[:]
        # sinal.insert(0, self.tempo)
        # self.agenda.append(sinal)
        # self.salva_agenda(self.agenda)
        print('agendar trade')





    def salva_agenda(self, agenda):
        print('salva agenda')
        with open('agenda.json', 'w') as a:
            json.dump(agenda, a)




    #-> Carrega o conteúdo da agenda sem o primeiro item
    def carrega_agenda(self):
        print('carrega agenda!')
        agenda = self.le_agenda()
        for item in agenda:
            item.pop(0)
        return agenda

    #-> le o arquivo agenda.json
    def le_agenda(self, agenda=[]):
        print('Le agenda')
        try:
            with open('agenda.json', 'r') as a:
                agenda = json.load(a)
            return agenda
        except:
            return agenda

    #-> salva a agenda no arquivo agenda.json        
    def salva_agenda(self, agenda):
        print('salva agenda')
        with open('agenda.json', 'w') as a:
            json.dump(agenda, a)

    #-> le a agenda, coloca em ordem pelo tempo para o proximo trade, atualiza a lista de sinais, atualiza o horario do proximo trade.        
    def mostra_agenda(self):

        # agenda = self.le_agenda()
        # print(agenda)
        # agenda.sort()
        # for sinal in agenda:
        #     if len(sinal) == 8:
        #         sinal.pop(0)
        # self.limpa_lista()
        # self.insere_widget(agenda)
        # self.proximo_trade(agenda)
        print("Mostra Agenda")

    #-> Exibe o proximo trade na tela
    def proximo_trade(self, agenda=[]):
    #     print("proximo Trade")
    #     try:
    #         # print(agenda[0][0])
    #         self.ids.HoraTrade.text = agenda[0][0]
    #     except:
    #         self.ids.HoraTrade.text = '--:--'
        pass
                
    #-> abre a ordem de acordo com o sinal, agenda a leitura do resultado para o final do tempo.
    #-> remove o sinal da lista de trades e atualiza a agenda
    def realiza_trade(self, sinal=[], *args, **kwargs):
        status, id = OPAL().trade(sinal)
        tempo = int(sinal[3])*60
        if status:
            Clock.schedule_once(partial(self.resultado, id, sinal), tempo)
        self.atualiza_agenda(sinal)

    #-> pega agenda, remove o primeiro indice (tempo), identifica a poição na lista do sinal que está sendo executado
    #-> remove da agenda e da lista de sinais o sinal que esta sendo executado.
    #-> atualiza as informações de tela 
    def atualiza_agenda(self, sinal):
        agenda = self.le_agenda()
        lista = self.le_agenda()
        for item in lista:
            item.pop(0)
        for chave, item in enumerate(lista):
            if item == sinal:
                agenda.pop(chave)
                self.salva_agenda(agenda)
        OPAL().exclui_sinal(sinal)
        self.mostra_agenda()
            
    #-> verifica se a operação foi vencedora ou não:
    #-#-> se foi vencedora atualiza a seção win/rit
    #-#-> se foi perdedora abre nova ordem de acordo com o numero de gales.
    def resultado(self, id, sinal, *args, **kwargs):
        gale = int(sinal[6])
        resultado, lucro = OPAL().resultado(id)
        if resultado != 'win' and gale > 0:
            gale -= 1
            sinal[6] = str(gale)
            self.trade(sinal)  
        else:
            print('atualizar win/rit')
            
    #-> troca para tela de menu            
    def para_TelaMenu(self):
        self.parent.current = 'TelaMenu'



    #-> Cancela os trades agendados
    def cancelar_trade(self):
        for item in self.ordens:
            Clock.unschedule(item)
        # self.mostra_agenda()
        self.limpa_lista()

# Exibe e exclui sinais da lista
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
        self.parent.remove_widget(self)
        TelaTrade().atualiza_agenda(sinal)
        print("exclui sinal")

# Exibe alertas do sistema
class Pop_up(Popup):
    def pop_up(self, titulo, texto):
        box = BoxLayout(orientation = 'vertical', padding = 20, spacing = 10)
        popup = Popup(title = titulo, content = box, size_hint = (None, None), size = (400,200))
        box.add_widget(Label(text = texto))
        box.add_widget(Button(text = 'OK', on_release = popup.dismiss))
        popup.open()
    
# Formata caixa de texto para hora e minutos
class MyTextInput(TextInput):
    """Classe responsavel por limitar o número de caracteres nos campos de texto
    permite apenas 2 caracteres númericos iteiros
    """
    max_characters = NumericProperty(1)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ''
        TextInput.insert_text(self, substring, from_undo)

# Formata caixa de texto para receber hora
class MyTextInput_Hora(MyTextInput):
    """Classe responsável por validar a hora inserida"""
    def _on_textinput_focused(self, instance, value, *largs):
        if self.text != '':
            hora = int(self.text)
            if hora > 23 or hora < 0:
                Pop_up().pop_up('Horario Invalido!', 'Corrija o capo hora e tente novamente!')
                self.text = '00'
        else:
            self.text = '00'
            pass
        return super()._on_textinput_focused(instance, value, *largs)
        
# Formata caixa de texto para receber minuto
class MyTextInput_Minuto(MyTextInput):
    """Classe responsável por validar o valor de minutos inserido"""
    def _on_textinput_focused(self, instance, value, *largs):
        if self.text != '':
            hora = int(self.text)
            if hora > 59 or hora < 0:
                Pop_up().pop_up('Horario Invalido!', 'Corrija o capo minutos e tente novamente!')
                self.text = '00'
        else:
            self.text = '00'
            pass

# Chama as funções do robo e daas telas
class OPAL(App):
    Robo = Robo()
    agenda = TelaTrade().le_agenda()
    agenda.clear()
    TelaTrade().salva_agenda(agenda)
    
    def build(self):
        return Gerenciador()
    
    def login(self, email, senha):
        self.login = self.Robo.singin(email, senha)
        return self.login
    
    def perfil(self):
        self.nome, self.banca = self.Robo.perfil()
        return self.nome, self.banca
    
    def insere_sinal(self, sinal):
        self.sinal = self.Robo.insere_sinal(sinal)
        return self.sinal
    
    def le_sinais(self):
        self.sinais = self.Robo.le_sinais()
        return self.sinais
    
    def exclui_sinal(self, sinal):
        self.Robo.exclui_sinal(sinal)

    def trade(self, sinal):
        status, id = self.Robo.trade(sinal)
        return status, id
    
    def resultado(self, id):
        resultado, lucro = self.Robo.resultado(id)
        return resultado, lucro

# Linha que inicia o sistema
if __name__ == '__main__':
    OPAL().run()

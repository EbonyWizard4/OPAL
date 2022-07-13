
from iqoptionapi.stable_api import IQ_Option
import json

class Robo():
    # --- SISTEMA DE LOGIN --- #
    def singin(self, email='', senha=''):
       
        self.API = IQ_Option("antonio.jhone@hotmail.com", "Krishinna@1")
        self.check,self.reason=self.API.connect()
        
        if self.check:
            print('start your bot')
            return self.API

        else:
            if self.reason=="[Errno -2] Name or service not known":
                print("No Network")
            elif self.reason:
                print("Error Password")
 
    def perfil(self):
        self.perfil = json.loads(json.dumps(self.API.get_profile())) 
        self.nome = self.perfil['result']['name']
        self.banca = str(self.API.get_balance())
        return self.nome, self.banca 
    
    def insere_sinal(self, sinal):
        try:
            self.sinais = self.le_sinais()
            self.sinais.append(sinal)
            self.salva_sinais(self.sinais)
                        
        except:
            self.salva_sinais()
            self.sinais = self.le_sinais()
            self.sinais.append(sinal)
            self.salva_sinais(self.sinais)            
            
        return True
    
    def salva_sinais(self, sinais=[]):
        with open('sinais.json', 'w') as s:
            sinais = sorted(sinais)
            json.dump(sinais, s)
            
    def le_sinais(self, sinais = []):
        try:
            with open('sinais.json', 'r') as s:
                self.sinais = json.load(s)
            
            return self.sinais
        except:
            return sinais

    def exclui_sinal(self, sinal):
        self.sinais = self.le_sinais()
        for i,v in enumerate(self.sinais):
            if sinal == v:
                self.sinais.remove(v)
        self.salva_sinais(self.sinais)

    def trade(self, sinal=[]):
        lista = self.le_sinais()
        print('-----------------------------------------------------------')
        print(lista)
        print('-----------------------------------------------')
        print(sinal)
        try:
            if sinal in lista:
                status,id = self.API.buy(sinal[4], sinal[1], sinal[2], sinal[3])
                return status, id
            else:
                print('sinal not found')
                return None, None
        except:
            return None, None
            
    def resultado(self, id):
        resultado, lucro = self.API.check_win_v3(id)
        return resultado, lucro



        
       
# --- SISTEMA DE ORDENS ---

# def AbreOrdem():
#     #PREENCHE AS VARIAVEIS USANTO TXT EXTERNO COM UM LOOP
#     #EXECUTA A ORDEM EM 
#     Status,id = API.buy(Sinal[4], Sinal[1], Sinal[2], Sinal[3])
#     #CHECA  O RESULTADO DA ORDEM
#     if Status:
#         print('Ordem aberta, aguarde...')
#         resultado, lucro = API.check_win_v3(id)
#         return resultado, lucro
        
# def ordem():
#     i = 0
#     while i<3:
#         resultado, lucro = AbreOrdem()
#         if resultado == 'win':
#             print('Ganhou!', lucro)
#             break
#         else:
#             print('Ops!')
#             Valor = float(Sinal[4])
#             Valor = Valor*1.9
#             Sinal[4] = str(Valor)
#             i += 1
        

# #---Leitura do arquivo de sinais---#
# Sinais = 'lista.txt'
# Sinais = open(Sinais, 'r').read()
# Sinais = Sinais.splitlines()

# for Sinal in sorted(Sinais):
#     Sinal = Sinal.split(',')
#     #[0] -> Horario
#     #[1] -> Paridade
#     #[2] -> Direcao
#     #[3] -> Timeframe
#     #[4] -> Valor
#     schedule.every().day.at(Sinal[0]).do(ordem)

# #--- EXECUÇÃO PROGRAMADA---#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
#   '''
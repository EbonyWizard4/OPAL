
from iqoptionapi.stable_api import IQ_Option
import json
#import schedule
import time


class Robo():
    # --- SISTEMA DE LOGIN --- #
    def singin(self, email='', senha=''):
        error_password="""{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
        self.LOGIN = IQ_Option("antonio.jhone@hotmail.com", "Krishinna@1")
        check,reason=self.LOGIN.connect()
        
        if check:
            print('foi')
            return self.LOGIN    

        else:
            if reason=="[Errno -2] Name or service not known":
                print("No Network")
            elif reason==error_password:
                print("Error Password")
 

    def perfil(self):
        self.perfil = json.loads(json.dumps(self.LOGIN.get_profile())) 
        self.nome = self.perfil['result']['name']
        self.banca = str(self.LOGIN.get_balance())
        return self.nome, self.banca 
    
    def insere_sinal(self, sinal):
        try:
            self.sinais = self.le_sinais(sinal)
            self.sinais.append(sinal)
            self.salva_sinais(self.sinais)
                        
        except:
            self.salva_sinais()
            self.sinais = self.le_sinais(sinal)
            self.sinais.append(sinal)
            self.salva_sinais(self.sinais)            
            
        return True
    
    def salva_sinais(self, sinais=[]):
        with open('sinais.json', 'w') as s:
            json.dump(sinais, s)
            
    def le_sinais(self, sinal):
        with open('sinais.json', 'r') as s:
            self.sinais = json.load(s)
        return self.sinais
        
        
       
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
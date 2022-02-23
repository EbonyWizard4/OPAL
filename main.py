import json


Hora = input('Digite o Horário da operação: ') #Recebe a hora
Par = input('Digite a paridade da operação: ')    #Recebe a moeda
Direcao = input('Digite a direção da operação: ') #Recebe o tipo de operação, PUT/CALL
Time = input('Digite o timeframe da operação: ') #Recebe o Tempo da Operação em minutos
Valor = input('Digite o valor da operação: ') #Recebe o Valor do Lance
    
def insereSinal(Hora, Par, Valor, Time, Direcao):
    with open('sinal.json', 'r') as s:
        sinal = json.load(s)

    sinal.apende([Hora, Par, Valor, Time, Direcao])
    with open('sinal.json', 'w') as s:
       json.dump(sinal, s)
    
    print(sinal)
    print(type(sinal))
    print(sinal[2])

insereSinal(Hora, Par, Valor, Time, Direcao)

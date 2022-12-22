from datetime import datetime, timedelta



def calcula_tempo():
    hora_atual = datetime.strptime(datetime.strftime(datetime.now(), "%H:%M:%S"), "%H:%M:%S")

    hora_sinal = datetime.strptime('07:00:00', "%H:%M:%S")
    print(hora_atual)
    print(hora_sinal)
    tempo = timedelta.total_seconds(hora_sinal - hora_atual) 
    if tempo <=0:
        tempo = tempo + 86400
        return tempo
    return tempo

tempo = calcula_tempo()

print(tempo)
import numpy as np
import matplotlib.pyplot as plt

def saveProgress(attempt):
    try:
        arc = open('progress.txt', 'a')
        arc.write("{}\n".format(attempt))
        arc.close()
    except: pass
    
    return

def clearProgress():
    try:
        arc = open('progress.txt', 'w')
        arc.write("")
        arc.close()
    except: pass
    
    return

def showGraph():
    arc = open('progress.txt', 'r')
    dataY = list(map(lambda i: int(i[0:-1]), arc.readlines()))
    arc.close()
    
    if len(dataY) == 0: return "No data to be shown"
    
    dataX = [i for i in range(1,len(dataY)+1)]

    if dataY[-1] < 22: victoryDotX = len(dataX)+1
    else: victoryDotX = len(dataX)

    fig = plt.figure("Gráfico de progresso")

    plt.plot(dataX, dataY, '.-', linewidth=2, markersize=12, label="Progresso")
    plt.plot(victoryDotX, 22, 'go', markersize=10, label="Alvo")

    plt.title("Progresso no Chrome Dino", fontsize=14, fontweight="600")
    plt.xlabel("Número da tentativa", fontsize=12)
    plt.ylabel("Pontuação", fontsize=12)
    plt.xticks(dataX)
    plt.yticks(dataY+[22])
    plt.legend(loc="lower right")
    plt.grid()

    plt.show()
    return "Ok"

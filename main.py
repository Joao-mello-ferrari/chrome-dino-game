try: from errorHelpers import importErrorMessage
except: print("Coloque o arquivo errorHelpers.py no diretório do main.py!")

# try:
from graphics import *
from time import sleep
from datetime import datetime as d

from objectHelpers import *
from commander import Commander
from graphHelper import *
from demoSimulator import *
    
# except: print(importErrorMessage())


def main(firstTime, win):
    if firstTime:
        win=GraphWin("ChromeDino",1000,600, autoflush=False)
        win.setBackground("#cccccc")
        drawFooter(win, "#222222")

    commander = Commander(win)
    dino, obstacles, line, renderDemo = drawIntro(win)
     
    while True:
        if renderDemo:
            dino, obstacles, line, renderDemo = renderDemoPage(win, dino, obstacles, line)
        else: break
    
    
    levelCounter = 1
    jumpCounter = 0
    jumpCompleted = True
    dinoType = "up"
    boolLastImgFrame = True
    lastKeyFilterTime = d.now()
    lastAnimationTime = d.now()
    timeBuff = 0
    progress = None
    frame = None
    speedButtons = None
    lastButtonIndex = None
    speed = 4
    
    while True:
        print(speed)
        frame, progress = renderProgressBar(win, levelCounter, progress, frame)
        
        obstacles = commander.moveObstacles(obstacles, levelCounter, speed)
        obstacles, levelCounter = commander.checkObstaclesPosition(obstacles, levelCounter)
        obstacles = commander.renderNewObstacles(obstacles, levelCounter)
        
        gameOver = commander.checkColision(dino, obstacles, dinoType)
        if gameOver or (levelCounter == 23 and jumpCompleted): break
        
        key = win.checkKey()
        if key == "space" or not jumpCompleted:
            jumpCompleted, jumpCounter = commander.jump(dino, jumpCounter, speed)
    
        elif key == "Down":
            lastKeyFilterTime = d.now()
            if dinoType == "up": timeBuff = 450000    
            else: timeBuff = 0
            
            dino, dinoType = commander.changeDino(win, dino, dinoType, "down")
        
        elif (d.now() - lastKeyFilterTime).microseconds > 50000+timeBuff:  
            dino, dinoType = commander.changeDino(win, dino, dinoType, "up")
        
        if (d.now() - lastAnimationTime).microseconds > 200000/speed:
            dino, obstacles, boolLastImgFrame = toggleImg(win, dino, obstacles, not boolLastImgFrame, dinoType)
            lastAnimationTime = d.now()
        
        if jumpCompleted:
            click = win.checkMouse()
            speedButtons, _, lastButtonIndex = commander.changeSpeed(win, click, speed, speedButtons, lastButtonIndex)
    
        update(10000)
    
    if not gameOver: dino, obstacles, portic = renderVictoryCenario(win, dino, obstacles, dinoType)
    else: portic = []
    
    objects = obstacles + speedButtons + portic + [dino, line, frame, progress]
    
    shouldClose = showFinalMessage(win, gameOver, objects)
    
    saveProgress(levelCounter-1)
    
    if shouldClose:
        win.close()
        return win, True
    
    return win, False
        

if __name__=="__main__":
    firstTime = True
    win = None
    
    while True:
        try: 
            win, shouldClose = main(firstTime, win)
            
            firstTime = False
            if shouldClose:
                print("Programa encerrado")
                break
        
        except Exception as err: # Se houver exceções
            print("ERRO AO EXECUTAR O PROGRAMA! / PROGRAMA FINALIZADO!")
            break

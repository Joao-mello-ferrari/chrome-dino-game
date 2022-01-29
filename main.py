try: from errorHelpers import importErrorMessage
except: print("Coloque o arquivo errorHelpers.py no diretório do main.py!")

try:
    from graphics import *
    from time import sleep
    from datetime import datetime as d

    from objectHelpers import *
    from commandHelpers import *
    from graphHelper import *
    from demoSimulator import *
    
except: print(importErrorMessage())


def main(firstTime, win):
    if firstTime:
        win=GraphWin("ChromeDino",1000,600, autoflush=False)
        drawFooter(win, "#222222")

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
    speed = 1
    
    while True:
        frame, progress = renderProgressBar(win, levelCounter, progress, frame)
        
        obstacles = moveObstacles(obstacles, levelCounter, speed)
        obstacles, levelCounter = checkObstaclesPosition(obstacles, levelCounter)
        obstacles = renderNewObstacles(win, obstacles, levelCounter)
        
        gameOver = checkColision(dino, obstacles, dinoType)
        if gameOver or (levelCounter == 23 and jumpCompleted): break
        
        key = win.checkKey()
        if key == "space" or not jumpCompleted:
            jumpCompleted, jumpCounter = jump(dino, jumpCounter, speed)
    
        elif key == "Down":
            lastKeyFilterTime = d.now()
            if dinoType == "up": timeBuff = 450000    
            else: timeBuff = 0
            
            dino, dinoType = changeDino(win, dino, dinoType, "down")
        
        elif (d.now() - lastKeyFilterTime).microseconds > 50000+timeBuff:  
            dino, dinoType = changeDino(win, dino, dinoType, "up")
        
        if (d.now() - lastAnimationTime).microseconds > 200000/speed:
            dino, obstacles, boolLastImgFrame = toggleImg(win, dino, obstacles, not boolLastImgFrame, dinoType)
            lastAnimationTime = d.now()
        
        if jumpCompleted:
            click = win.checkMouse()
            speedButtons, speed, lastButtonIndex = changeSpeed(win, click, speed, speedButtons, lastButtonIndex)
    
        update(250)
    
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

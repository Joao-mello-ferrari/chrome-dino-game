from graphics import *
from time import sleep
from datetime import datetime as d

from objectHelpers import drawIntro
from commandHelpers import *

# Renderizar o modo DEMO
def renderDemoPage(win, dino, obstacles, line):
    warning = Rectangle(Point(280,75), Point(720,225))
    warning.setFill("#BBBBBB")
    warning.setOutline("#666666")
    warning.setWidth(2)
    warning.draw(win)
    
    message = Text(Point(500,150), "VOCÊ ESTÁ NO MODO DEMO\nPara sair, aperter ENTER!")
    message.setFace("helvetica")
    message.setSize(18)
    message.setStyle("bold")
    message.setTextColor("#444444")
    message.draw(win)
    
    spaceRec = Rectangle(Point(300,470), Point(570,510))
    spaceRec.setFill("#BBBBBB")
    spaceRec.setOutline("#666666")
    spaceRec.setWidth(0)
    spaceRec.draw(win)
    
    spaceText = Text(Point(440,490), "Space")
    spaceText.setFace("helvetica")
    spaceText.setSize(14)
    spaceText.setTextColor("#444444")
    spaceText.draw(win)
    
    pageDownRec = Rectangle(Point(590,470), Point(700,510))
    pageDownRec.setFill("#BBBBBB")
    pageDownRec.setOutline("#666666")
    pageDownRec.setWidth(0)
    pageDownRec.draw(win)
    
    pageDownText = Text(Point(645,490), "Page Down")
    pageDownText.setFace("helvetica")
    pageDownText.setSize(14)
    pageDownText.setTextColor("#444444")
    pageDownText.draw(win)
    
    # Definir variáveis do loop do DEMO
    levelCounter = 1
    jumpCounter = 0
    jumpCompleted = True
    dinoType = "up"
    lastAnimationTime = d.now()
    boolLastImgFrame = True
    
    # Loop do modo DEMO
    while True:
        if win.checkKey() == "Return": break
        
        obstacles = moveObstacles(obstacles, levelCounter,1)
        obstacles, levelCounter = checkObstaclesPosition(obstacles, levelCounter, inc=1)
        obstacles = renderNewObstacles(win, obstacles, levelCounter)
        
        action = checkAction(obstacles, dino, levelCounter)
        
        if action == "jump" or not jumpCompleted:
            spaceRec.setFill("#777777")
            jumpCompleted, jumpCounter = jump(dino, jumpCounter,1)
        
        elif action == "down":
            pageDownRec.setFill("#777777")
            dino, dinoType = changeDino(win, dino, dinoType, "down")
        
        elif dinoType == "down" and obstacles[0].getAnchor().getX() < 90:
            dino, dinoType = changeDino(win, dino, dinoType, "up")
        
        else:
            spaceRec.setFill("#BBBBBB")
            pageDownRec.setFill("#BBBBBB")
        
        if (d.now() - lastAnimationTime).microseconds > 200000:
            dino, obstacles, boolLastImgFrame = toggleImg(win, dino, obstacles, not boolLastImgFrame, dinoType)
            lastAnimationTime = d.now()
            
        update(250)
    
    for i in obstacles: i.undraw()
    warning.undraw()
    message.undraw()
    spaceRec.undraw()
    spaceText.undraw()
    pageDownRec.undraw()
    pageDownText.undraw()
    dino.undraw()
    line.undraw()
    
    return drawIntro(win, False)
    
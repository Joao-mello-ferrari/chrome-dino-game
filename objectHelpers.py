from time import sleep
from graphics import *
from datetime import datetime as d

from commandHelpers import checkClickArea, toggleImg
from graphHelper import clearProgress, showGraph


# Desenhar rodapé
def drawFooter(win, color):
    t = Text(Point(760,588), "@ Todos os direitos reservados. Atualizado em 24/09/2021, por João Mello.")
    t.setOutline(color)
    t.setFace("helvetica")
    t.setSize(10)
    t.setStyle("bold")
    t.draw(win)


# Mostrar tooltip, se o usuário desejar ver o grafíco, mas não tiverem dados salvos
def showToolTip(win):
    triangle = Polygon(Point(725,520),Point(720,512),Point(730,512))
    triangle.setFill("#BBBBBB")
    triangle.setOutline("#BBBBBB")
    triangle.setWidth(0)
    triangle.draw(win)
    
    rec = Rectangle(Point(640,460),Point(810,512))
    rec.setFill("#BBBBBB")
    rec.setWidth(0)
    rec.draw(win)
    
    text = Text(Point(725, 485), "Faça uma tentativa para\nver seu progresso!")
    text.setFace("helvetica")
    text.setSize(10)
    text.setTextColor("#444444")
    text.draw(win)
    update(100)
    
    sleep(2)
    
    triangle.undraw()
    rec.undraw()
    text.undraw()
    
    return 


# Desenhar o pórtico do final do jogo
def drawPortic(win):
    line1 = Line(Point(800,320),Point(800,420))
    line1.setWidth(6)
    line1.setFill("#444444")
    line1.draw(win)
    
    line2 = Line(Point(750,290),Point(750,390))
    line2.setWidth(6)
    line2.setFill("#444444")
    line2.draw(win)
    
    line3 = Line(Point(747,287), Point(802,322))
    line3.setWidth(6)
    line3.setFill("#444444")
    line3.draw(win)
    
    line4 = Line(Point(750,320), Point(800,350))
    line4.setWidth(6)
    line4.setFill("#444444")
    line4.draw(win)
    
    return [line1, line2, line3, line4]


# Desenhar a abertura do jogo
def drawIntro(win, animation=True):
    baseLine = Line(Point(20,400), Point(980,400))
    baseLine.setWidth(3)
    baseLine.setFill("#747272")
    baseLine.draw(win) 
       
    dino = Image(Point(120,388), "imgs/dino1.gif")
    dino.draw(win)
 
    cactus = Image(Point(600,385), "imgs/cactus1.gif")
    cactus.draw(win)
    
    if animation: i0 = 0
    else: i0 = 99
    
    # Animação da mensagem inicial
    logo = None
    for i in range(i0,100):
        if logo: logo.undraw()
        x1 = 500 - 2.2*i
        x2 = 500 + 2.2*i
        y1 = 200 - 0.75*i
        y2 = 200 + 0.75*i
        logo = Rectangle(Point(x1,y1), Point(x2,y2))
        logo.setFill("#999999")
        logo.setOutline("#666666")
        logo.setWidth(2)
        logo.draw(win)
        update(100)
     
    rec = Rectangle(Point(638, 209), Point(699, 237))
    rec.setFill("#CCCCCC")
    rec.setOutline("#999999")
    rec.draw(win)

    mainText = Text(Point(440,200),
                    '''
                    Bem-vindo(a) ao jogo do dino!
                    Para jogar, aperte ENTER :)
                    Para entrar no modo DEMO, clique  AQUI!
                    ''')
    mainText.setFace("helvetica")
    mainText.setSize(16)
    mainText.draw(win)
    
    graphButton = Rectangle(Point(650, 520), Point(800, 560))
    graphButton.setFill("#5C7AF1")
    graphButton.setWidth(0)
    graphButton.draw(win)
    
    graphButtonText = Text(Point(725,540), "Ver progresso")
    graphButtonText.setSize(11)
    graphButtonText.setFace("helvetica")
    graphButtonText.setTextColor("#FFFFFF")
    graphButtonText.setStyle("bold")
    graphButtonText.draw(win)
    
    clearButton = Rectangle(Point(820, 520), Point(970, 560))
    clearButton.setFill("#F65D3B")
    clearButton.setWidth(0)
    clearButton.draw(win)
    
    clearButtonText = Text(Point(895,540), "Limpar progresso")
    clearButtonText.setSize(11)
    clearButtonText.setFace("helvetica")
    clearButtonText.setTextColor("#FFFFFF")
    clearButtonText.setStyle("bold")
    clearButtonText.draw(win)
    
    # Pegar o comando do usuário
    needHelp = False
    while True:
        click = win.checkMouse()
        if checkClickArea("helpButton", click):
            needHelp = True
            break
        
        if checkClickArea("graphButton", click):
            graphStatus = showGraph()
            if graphStatus == "No data to be shown": showToolTip(win)
            
            
        if checkClickArea("clearButton", click):
            clearProgress()
            clearButton.setFill("#F7BFB3")
            
        if win.checkKey() == "Return": break
    
    logo.undraw()
    rec.undraw()
    mainText.undraw()
    graphButton.undraw()
    graphButtonText.undraw()
    clearButton.undraw()
    clearButtonText.undraw()
    
    return dino, [cactus], baseLine, needHelp


# Mostrar a barra de progresso em tela
def renderProgressBar(win, level, progress, frame):
    if progress is None:
        frame = Rectangle(Point(848, 60),Point(940, 90))
        frame.setOutline("#444444")
        frame.setWidth(4)
        frame.draw(win)
        
    elif (progress.getP2().getX()-850)/4 == level: return frame, progress
    
    if progress is not None: progress.undraw()
    progress = Rectangle(Point(850, 62),Point(850 + level*4, 88))
    progress.setWidth(0)
    progress.setFill("#22DD22")
    progress.draw(win)  
    
    return frame, progress


# Mostrar o cenário de virtória quando o usuário vencer
def renderVictoryCenario(win, dino, obstacles, dinoType):
    portic = drawPortic(win) 
    
    lastAnimationTime = d.now()
    boolLastImgFrame = True
    for i in range(200):
        for j in obstacles: j.move(0,-6)
        for j in portic: j.move(-1,0)
        dino.move(3,0)
        update(50)
        
        if (d.now() - lastAnimationTime).microseconds > 100000:
            dino, obstacles, boolLastImgFrame = toggleImg(win, dino, obstacles, not boolLastImgFrame, dinoType)
            lastAnimationTime = d.now()
            
    return [dino, obstacles, portic]


# Desenhar a mensagem final, com a informação de vitória ou derrota
def showFinalMessage(win, gameOver, objects):
    for i in objects:
        i.undraw()
        update(15)
    
    finalRec = Rectangle(Point(280,100), Point(720,250))
    finalRec.setFill(color_rgb(200,200,200))
    finalRec.setWidth(0)
    finalRec.draw(win)   
    for i in range(200,100,-1):
        finalRec.setFill(color_rgb(i,i,i))
        update(120)
        
    if gameOver:
        dinoImg = Image(Point(500,400), "imgs/sadDino.gif")
        dinoImg.draw(win)
        text = Text(Point(500,140), "GAME OVER")
        text.setTextColor("#E85050")
    else:
        dinoImg = Image(Point(500,410), "imgs/happyDino.gif")
        dinoImg.draw(win)
        text = Text(Point(500,140), "VICTORY!")
        text.setTextColor("#63E03E")
        
    text.setFace("helvetica")
    text.setSize(20)
    text.setStyle("bold")
    text.draw(win)
    
    text1 = Text(Point(500,200), "Para jogar novamente, aperte ENTER.\nPara sair, clique em qualquer lugar da tela!")
    text1.setFace("helvetica")
    text1.setSize(16)
    text1.setTextColor("#BBBBBB")
    text1.draw(win)
    
    while True:
        if win.checkMouse() != None: return True

        if win.checkKey() == "Return":
            finalRec.undraw()
            dinoImg.undraw()
            text.undraw()
            text1.undraw()
            return False
            
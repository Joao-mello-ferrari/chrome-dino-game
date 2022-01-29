from graphics import *
from random import randrange as r

# Nome dos arquivos de imagem dos obstáculos
images = ["cactus1","cactus2","cactus3", "bird1"]

# Mapeamento de pontos dos dinossauros
dino1Dots = [[-20,0],[-15,9],[-9,20],[2,20],[5,7],[18,-12],[18,-19],[0,-10],[-4,-3],[-20,-4]]
dino4Dots = [[25,-12],[25,-4],[21,1],[10,1],[2,2],[-10,11],[-16,7],[-19,-2],[-27,-8],[15,-12],[2,-10],[-13,-11]]

# Mapeamento de seções dos obstáculos
cactus1Dots = [ [[-11,11],[-13,21]], [[-2,3],[-23,-13]] ]
cactus2Dots = [ [[-23,23],[-18,21]], [[-15,-11],[-22,-18]], [[11,15],[-22,-18]] ]
cactus3Dots = [ [[-24,22],[-7,21]], [[-18,-8],[-22,-7]], [[3,25],[-18,22]] ]
birdDots    = [ [[-27,-19],[0,4]], [[-17,-8],[-9,3]], [[-7,28],[-14,14]] ]


# Gerar os obstáculos de maneira aleatória, conforme o nível
def chooseObstacle(level):
    global images
    
    if level == 4: min = 2
    elif level == 3: min = 1
    else: min = 0
    
    return images[r(min,level)]  
 
 
# Identificar se um local da tela foi clicado
def checkClickArea(case, area):
    if not area: return
    
    if case == "helpButton":
        coords = [[645,706],[209,237]]
    elif case == "graphButton":
        coords = [[650,800],[520,560]]
    elif case == "clearButton":
        coords = [[820,970],[520,560]]
    elif case == "slowButton":
        coords = [[730,790],[490,530]]
    elif case == "mediumButton":
        coords = [[800,860],[490,530]]
    elif case == "fastButton":
        coords = [[870,930],[490,530]]
    
    else: coords = [[0,0],[0,0]]
    
    x = area.getX()
    y = area.getY()
        
    if x >= coords[0][0] and x <= coords[0][1]:
        if y >= coords[1][0] and y <= coords[1][1]:
            return True
    
    return False


# Mover os obstáculos
def moveObstacles(obstacles, level, speed):
    if level > 12: coef = 2
    else: coef = (level//3)*0.25 + 1
    
    for i in range(len(obstacles)):
        obstacles[i].move(-1.0 * coef * speed, 0)
        
    return obstacles
 
 
# Remover os obstáculos que estiverem no fim da linha
def checkObstaclesPosition(obstacles, level, inc = 0):
    if not len(obstacles): return []
    
    anchor = obstacles[0].getAnchor()
    if anchor.getX() < 40:
        obstacles[0].undraw()
        obstacles.pop(0)
        level += (1+inc)
    
    return obstacles, level


# Retornar se há colisão do dinossauro com o primeiro obstáculo 
def checkColision(dino, obstacles, dinoType):
    if len(obstacles) == 0: return False 
    
    dinoAnc = dino.getAnchor()
    obsAnc  = obstacles[0]
    
    dx = dino.getAnchor().getX()
    dy = dino.getAnchor().getY()
    ox = obstacles[0].getAnchor().getX()
    oy = obstacles[0].getAnchor().getY()
    
    # A checagem da colisão só é realizada com o dinossauro estiver
    # a menos de 64 píxels de distância do primeiro objeto.
    # Isso serve para otimizar o jogo.
    if ((dx-ox)**2 + (dy-oy)**2)**0.5 > 64: return False
    
    global dino1Dots, dino4Dots, cactus1Dots, cactus2Dots, cactus3Dots, birdDots  
    
    if dinoType == "up": dinoDots = dino1Dots
    else: dinoDots = dino4Dots
    
    obsW = obstacles[0].getWidth()
    if obsW == 23: obsDots = cactus1Dots
    elif obsW == 46: obsDots = cactus2Dots
    elif obsW == 49: obsDots = cactus3Dots
    else: obsDots = birdDots
    
    for i in dinoDots:
        for j in obsDots:
            if j[0][0]+ox <= i[0]+dx and i[0]+dx <= j[0][1]+ox:
                if j[1][0]+oy <= i[1]+dy and i[1]+dy <= j[1][1]+oy: return True
                                
    return False


# Renderizar novos obstáculos, utilizando como base a função "chooseObstacle"
def renderNewObstacles(win, obstacles, level):
    if level > 18: num = 4
    else: num = (level//6) + 1
    
    newObstacleName = chooseObstacle(num)
    if "bird" in newObstacleName: p = Point(900,360)
    else: p = Point(900,385)
    
    
    if obstacles[-1].getAnchor().getX() < 300:
        newObstacle = Image(p, "imgs/{}.gif".format(newObstacleName))
        newObstacle.draw(win)
        obstacles.append(newObstacle)
      
    return obstacles


# Comandar o salto do dinossauro
def jump(dino, counter, speed):
    if counter == 120/speed: return True, 0
    elif counter < 20/speed: dino.move(0,-2 * speed)
    elif counter < 60/speed: dino.move(0,-1 * speed)
    elif counter < 100/speed: dino.move(0,1 * speed)
    else: dino.move(0,2 * speed)
    
    return False,counter+1


# Mudar a imagem do dinossauro (levantado para abaixado e vice-versa)
def changeDino(win, dino, dinoType, action):
    # É realizada uma checagem, para saber se o dinossauro deve ser alterado (otimização)
    if dinoType == action: return dino, dinoType

    if action == "up":
        dino.undraw()
        dino = Image(Point(120,388), "imgs/dino1.gif")
        dino.draw(win)
        
    elif action == "down":
        dino.undraw()
        dino = Image(Point(120,397), "imgs/dino4.gif")
        dino.draw(win)
    
    return dino, action
    

# Animação do dinossauro e do pássaro
def toggleImg(win, dino, obstacles, state, imgType=None):
    for i in range(len(obstacles)):
        w = obstacles[i].getWidth()
        if w == 56 or w == 57:
            birdX = obstacles[i].getAnchor().getX()
            birdY = obstacles[i].getAnchor().getY()
            
            obstacles[i].undraw()
            
            if state: bird = Image(Point(birdX,birdY), "imgs/bird1.gif")
            else: bird = Image(Point(birdX,birdY), "imgs/bird2.gif")
            
            bird.draw(win)
            obstacles[i] = bird
            
    dinoX = dino.getAnchor().getX()
    dinoY = dino.getAnchor().getY()
    dino.undraw()
    
    if imgType == "up":
        if state: dino = Image(Point(dinoX,dinoY), "imgs/dino1.gif")
        else: dino = Image(Point(dinoX,dinoY), "imgs/dino2.gif")
        
    elif imgType == "down":
        if state: dino = Image(Point(dinoX,dinoY), "imgs/dino4.gif")
        else: dino = Image(Point(dinoX,dinoY), "imgs/dino5.gif")

    dino.draw(win)    
    
    return [dino, obstacles, state]


# Determinar a ação do dinossaura no modo DEMO
def checkAction(obstacles, dino, level):
    obstacleCenter = obstacles[0].getAnchor()
    obsX = obstacleCenter.getX()
    obsY = obstacleCenter.getY()
    
    if obsY == 360 and obsX < 250 and obsX > 90: return "down"
    
    elif obsX < 210 and obsX > 120:
        if level <= 5 and obsX < 180: return "jump"
        elif level > 5: return "jump"
        
    return None


# Alterar a velocidade do jogo, conforme os botões forem clicados
def changeSpeed(win, click, speed, buttons, lasButtonIndex):
    buttonCases = ["slowButton","mediumButton","fastButton"]
    
    if not buttons:
        speedRec = Rectangle(Point(720, 480), Point(940, 540))
        speedRec.setFill("#BBBBBB")
        speedRec.setWidth(2)
        speedRec.setOutline("#BBBBBB")
        speedRec.draw(win)
            
        slowButton = Rectangle(Point(730, 490), Point(790, 530))
        slowButton.setFill("#888888")
        slowButton.setWidth(0)
        slowButton.draw(win)
        
        mediumButton = Rectangle(Point(800, 490), Point(860, 530))
        mediumButton.setFill("#444444")
        mediumButton.setWidth(0)
        mediumButton.draw(win)
        
        fastButton = Rectangle(Point(870, 490), Point(930, 530))
        fastButton.setFill("#888888")
        fastButton.setWidth(0)
        fastButton.draw(win)
        
        slowText = Text(Point(760,510), "0.5x")
        slowText.setSize(12)
        slowText.setFace("helvetica")
        slowText.setTextColor("#FFFFFF")
        slowText.setStyle("bold")
        slowText.draw(win)
        
        mediumText = Text(Point(830,510), "1.0x")
        mediumText.setSize(12)
        mediumText.setFace("helvetica")
        mediumText.setTextColor("#FFFFFF")
        mediumText.setStyle("bold")
        mediumText.draw(win)
        
        fastText = Text(Point(900,510), "2.0x")
        fastText.setSize(12)
        fastText.setFace("helvetica")
        fastText.setTextColor("#FFFFFF")
        fastText.setStyle("bold")
        fastText.draw(win)
        
        return [slowButton, mediumButton, fastButton, slowText, mediumText, fastText, speedRec], 1, 1
        
    else:
        for i in range(len(buttonCases)):
            if checkClickArea(buttonCases[i], click):
                buttons[i].setFill("#444444")
                buttons[lasButtonIndex].setFill("#888888")
                speed = [0.5,1,2][i]
                
                return buttons, speed, i
        
        return [buttons, speed, lasButtonIndex]
    
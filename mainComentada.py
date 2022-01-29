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


# Função principal do jogo
def main(firstTime, win):
    
    # Se é a primeira vez, cirar a janela e desenhar o rodapé
    if firstTime:
        win=GraphWin("ChromeDino",1000,600, autoflush=False)
        drawFooter(win, "#222222")
    
    # Desenhar a tela de abertura e pegar o comando do usuário
    dino, obstacles, line, renderDemo = drawIntro(win)
     
    # O loop serve para manter o jogador na tela de abertura, enquanto ele desejar
    # Se ele desejar jogar, então o loop é interrompido
    while True:
        if renderDemo:
            # Exibir o jogo no modo DEMO, enquanto o jogador desejar
            # A funcionalidade de ver o gráfico e limpar os dados é realizada,
            # também, por esse função
            dino, obstacles, line, renderDemo = renderDemoPage(win, dino, obstacles, line)
        else: break
    
    
    # DEFINIÇÃO DAS VARIÁVEIS DO LOOP (sim, são várias)
    
    # Nível do jogo (a cada obstáculo que passa, o nível é incrementado)
    levelCounter = 1
    
    # Contador do pulo (auxilia na realização da animação)
    jumpCounter = 0
    
    # O pulo foi completo (durante o pulo, o jogador não pode alterar a velocidade
    # do jogo nem alterar a imagem (tipo) do dinossauro)
    jumpCompleted = True
    
    # Tipo do dinossauro (levantado, abaixado)
    dinoType = "up"
    
    # Booleano, utilizado para a animação do dinossauro e pássaro
    boolLastImgFrame = True
    
    # Último vez (tempo) que o jogador alterou o tipo do dinossauro de "up" para "down"
    lastKeyFilterTime = d.now()
    
    # Última vez (tempo) que a animação do dinossauro e do pássaro foi realizada
    lastAnimationTime = d.now()
    
    # Buffer de tempo, para auxiliar no "bounce" do botão "Page Down"
    timeBuff = 0
    
    # Objetos visuais que serão criados no loop (barra de progresso + borda e
    # botões de controle de velocidade do jogo)
    progress = None
    frame = None
    speedButtons = None
    
    # Botão de velocidade pressionado
    lastButtonIndex = None
    
    # Velocidade do jogo
    speed = 1
    
    # Loop principal
    while True:
        
        # Rendezerizar a barra de progresso
        frame, progress = renderProgressBar(win, levelCounter, progress, frame)
        
        # Mover os obstáculos
        obstacles = moveObstacles(obstacles, levelCounter, speed)
        # Checar se o primeiro osbtáculo já deve ser retirado de tela
        obstacles, levelCounter = checkObstaclesPosition(obstacles, levelCounter)
        # Renderizar um novo obstáculo, com base no valor de "levelCounter"
        obstacles = renderNewObstacles(win, obstacles, levelCounter)
        
        # Saber se já colisão do dinossauro com o primeiro obstáculo
        gameOver = checkColision(dino, obstacles, dinoType)
        # Se houver colisão ou o jogador venceu (levelCounter == 23)
        # O jumpCompleted é um filtro para garantir que o dinossauro
        # não será encaminhado para o pórtico no meio do pulo
        if gameOver or (levelCounter == 23 and jumpCompleted): break
        
        # Agora entra a parte de pegar os comandos do usuário
       
        # Pegar a tecla clicada
        key = win.checkKey()
        
        # Se o "espaço" foi clicado, chamar função do pulo
        if key == "space" or not jumpCompleted:
            jumpCompleted, jumpCounter = jump(dino, jumpCounter, speed)
        
        # Senão, se a tecla clicada é o "Page Down"
        elif key == "Down":
            # Zerar o tempo de filtro do tecla "Page Down"
            lastKeyFilterTime = d.now()
            
            # Aplicar o filtro de tempo na primeira execução do
            # dinossauro abaixado (para mais detalhes, ler o README.md)
            if dinoType == "up": timeBuff = 450000    
            else: timeBuff = 0
            
            # Alterar a imagem do dinossauro
            dino, dinoType = changeDino(win, dino, dinoType, "down")
        
        # Senão, se já passou o tempo de filtro, alterar o tipo do
        # dinossauro para levantado
        elif (d.now() - lastKeyFilterTime).microseconds > 50000+timeBuff:  
            dino, dinoType = changeDino(win, dino, dinoType, "up")
        
        # Controlar a animação do dinossauro e do pássaro (acontece a cada 0.2 segundos)
        if (d.now() - lastAnimationTime).microseconds > 200000/speed:
            dino, obstacles, boolLastImgFrame = toggleImg(win, dino, obstacles, not boolLastImgFrame, dinoType)
            lastAnimationTime = d.now()
        
        # Alterar a velocidade do jogo, se não estiver no meio do pulo e se o usuário desejar
        if jumpCompleted:
            click = win.checkMouse()
            speedButtons, speed, lastButtonIndex = changeSpeed(win, click, speed, speedButtons, lastButtonIndex)
        
        # Atualizar o jogo, no máximo, 250 vezes por segundo
        update(250)
    
    # Se o usuário não perdeu (ganhou), mostrar o cenário de vitória
    if not gameOver: dino, obstacles, portic = renderVictoryCenario(win, dino, obstacles, dinoType)
    else: portic = []
    
    # Concatenar todos os obsjetos visuais, para enviá-los para a penúltima função do jogo
    objects = obstacles + speedButtons + portic + [dino, line, frame, progress]
    
    # Apagar os objetos visuais e pegar o comando do usuário sobre
    # continuar o jogo ou fechá-lo
    shouldClose = showFinalMessage(win, gameOver, objects)
    
    # Salvar o progresso do usuário
    saveProgress(levelCounter-1)
    
    # Se o joagdor deseja fechar a aplicação (True)
    if shouldClose:
        win.close()
        return win, True
    
    # Senão, retornar que deve continuar (False)
    return win, False
        
    # A a janela (win) é retornada para ser reaproveitada,
    # caso o jogo continue
        

# Se este é o arquivo principal (neste caso, sim)
if __name__=="__main__":
    # É a primeira vez
    firstTime = True
    
    # A janela é indefinida (será criada na linha 19)
    win = None
    
    # Loop que permite o jogo ser executado mais de uma vez
    while True:
        try: # Tentar (serve para, caso tenham error, cair no bloco que lida com exceções)
            
            # Executar o jogo uma vez, e ver se o usuário deseja executar novamente
            # A janela é retornada, para se reaproveitada
            win, shouldClose = main(firstTime, win)
            
            # Dizer que não é mais a primeira execução
            firstTime = False
            
            # Se o usuário deseja sair do jogo, então fecahr a aplicação
            if shouldClose:
                print("Programa encerrado")
                break
        
        except Exception as err: # Se houver exceções
            print("ERRO AO EXECUTAR O PROGRAMA! / PROGRAMA FINALIZADO!")
            break

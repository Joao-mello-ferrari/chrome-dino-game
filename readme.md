Neste arquivo será exposta a função de cada arquivo do projeto, bem como o funcionameno do mesmo e problemas/soluções encontradas durante a fase de desenvolvimento. 
No final será mostrada um trecho de código que pode ser
substituído no arquivo "main.py", que permite ao jogador vencer fazendo 
nenhuma ação.

# Funções dos arquivos
-imgs (pasta de arquivos) |-> Armazenar as imagens utilizadas no jogo
-commandHelpers.py |-> Responsável por analisar cenários da aplicação e propor ações
-demoSimulator.py |-> Guardar a lóica do modo DEMO do jogo
-graphHelper.py |-> Construir o gráfico e manipular o arquivo de dados
-objectHelpers.py |-> Responsável por montar objetos visuais e mostrá-los em tela
-progress.txt |-> Armazenar o progresso do usuário
-errorHelpers |-> Mostrar mensagens de erro
-main.py |-> Arquivo principal do jogo
-mainComentada.py |-> Idêntico ao main.py, porém totalmente comentado

# Funcionamento
O jogo original do Chrome possui algumas funcionalidades extras, e esta versão tem,
da mesma forma, alguns mecanismos adicionais;

O jogo desenvolvido conta com um MODO DEMO, no qual o dinossauro joga de maneira
autônoma, para que o usuário possa entender o funcionamento da aplicação;

O jogo é baseado em dois movimentos: pular e a abaixar, utilizando com teclas o "Espaço" e o "Página para baixo";

É possibilitado ao usuário ver um gráfico que mostra o seu progresso;

Durante o jogo, é possível alterar a velocidade do mesmo;

No final, é mostrada uma mensagem de vitória/derrota.

# Desafios
-LEITURA INCORRETA DAS TECLAS:
Se mantivermos uma tecla pressionada, a função checkKey() não retorna todas as leituras correspondentes: a função executa muito rápido, de forma que a maioria das
leituras são de tecla solta, o que dificulta o desenvolvimento do jogo, pois o dinossauro só fica abaixado se a LEITURA da tecla for "Página para baixo".

Para solucionar, foi feito um filtro de tempo, de forma que uma vez que a tecla foi apertada para baixo, somente depois de x milisegundos que uma nova leitura será considerada. Assim, as leituras indesejadas são desconsideradas.


-BOUNCE DO TECLADO:
O teclado, quando é apertado e pressionado, gera um efeito bounce. Dessa forma, quando a tecla "Página para baixo" é pressionada e mantida, há um tempo que a tecla ainda fica solta. Dessa forma, o dinossauro fica com um bug, no momento em que passa de "levantado" para "abaixado"

Para solucionar, foi feito um buff de tempo, que anula esse tempo de bouce da tecla.


-IDENTIFICAR COLISÃO
Identificar a colisão do dinossauro com um peça é mais difícil do que parece..
O que se fez foi mapear alguns pontos do corpo do dinossauro e, somado a isso, um mapeamento das seções de cada obstáculo.

Dessa forma, para checar se há uma colisão, pega-se cada ponto do dinossauro e se faz uma checagem para saber se ele está dentro de uma das seções do obstáculo.
Se qualquer ponto estiver dentro de qualquer seção, então há uma colisão.

Por ser uma lógica que consome bastante processamento, esse checagem só é realizada quando o dinossauro está bem próximo do obstáculo, pois se estiver longe, é possível afirmar que não há colisão, com muito menos processamento.


# Como ser invencível?
Isso é fácil! 
No arquivo main.py, há na linha 51 a seguinte lógica:

gameOver = checkColision(dino, obstacles, dinoType)

Para torna o dinossauro invencível, tipo um fantasma, basta SUBSTITUIR
essa linha por:

gameOver = False

Se achar o jogo muito difícil, é possível usar esse mecanismo :)





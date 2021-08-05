# Visão Computacional em Python

Usaremos as libs OpenCV-Python e Mediapipe para seguir o curso de 6 horas disponível em:

https://www.freecodecamp.org/news/advanced-computer-vision-with-python/

Que contém algumas aplicações dessas libs de modo a criar aplicações simples que utilizam conceitos de visão computacional. Inicialmente, deve-se instalar todas as depedências do projeto por meio de um "pip install -r requirements.txt". É necessário uma webcam para os projetos que envolvem mãos. <b>Está</b> sendo desenvolvida uma aplicação para aprendizado de visão computacional com base no tutorial acima, sobre: 

### Hand Tracking: identificação e rastreamento de mãos;

### Face Detection: necessário uma pasta "Vídeos" com vídeos iniciando em 1.mp4, analogamente ao explicado acima;

### Face Mesh: os vídeos a serem utilizados são, a princípio, os mesmos da psta "Face Detection". A diferença deste módulo para o anterior reside no fato de ter muito mais pontos (landmarks): 468! Isso permite uma visualização tridimensional mais fiel a realidade;

### Volume Hand Control: iremos controlar o volume do windows por meio de gestos com a ponta dos dedos. Para isso, além das libs anteriores, será usada uma chamada pycaw, que já está incluída na lista de dependências (requirements.txt);

### Finger Counter: será interpretada a informação de quantas dedos estão levantados em uma mão. Serão usadas as imagens contidas na pasta "FingerImages", cujas licenças são Creative Commons. Obs: a mão a ser utilizada deve ser a direita, para simplificar. É possível identificar a mão usada e adaptar a aplicação de modo a trabalhar com qualquer uma das mãos;

## OBSERVAÇÃO: Para os projetos "Pose Tracking" e "Personal AI Trainer" deve-se criar uma pasta "Media" no diretório "Pose Tracking" com os conteúdos dos respectivos treinamentos. Ou seja, vídeos de nomes "1.mp4", "2.mp4", "3.mp4", etc ... bem como "curls.mp4" >>>> e possivelmente "test.jpg". <<<<

### Pose Tracking: identificação e rastreamento de movimentos corporais (posturas). É necessário ter um vídeo de nome "1.mp4" que contém uma pessoa realizando movimentos. Esse vídeo deve estar numa pasta chamada "PoseVideos" a ser criada no mesmo diretório do "PoseModule.py". Em seguida, basta rodá-lo tendo todas as dependências instaladas;


### Personal AI Trainer: baixar os vídeos conforme disponível no tutorial original (https://www.computervision.zone/lessons/project-3-ai-personal-trainer/).
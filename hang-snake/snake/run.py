import pygame
from pynput import keyboard
from random import randrange

WIDTH, HEIGHT = 700, 50
# можно приделать конфиг-файл с параметрами
direction = (1, 0)

#название игры
pygame.display.set_caption("Змейка")


#цвета RGB
MainColor=(0,0,0)
ZmeiColor=(0,200,0)
Apl=(255,0,0)


#определение уровня
bb=0
a=int(input("Выберите уровень сложности от 1 до 3:  "
            ""))
if a==1:
    bb=6
elif a==2:
    bb=8
else:
    bb=12



#рандомное расположение коорднинат змеи
x,y= randrange(0,WIDTH,HEIGHT),randrange(0,WIDTH,HEIGHT)

lenght=1
snake=[(x,y)]

#рандомное расположение коорднинат яблока
apple= randrange(0,WIDTH,HEIGHT),randrange(0,WIDTH,HEIGHT)
if apple==snake:
    apple = randrange(0, WIDTH, HEIGHT), randrange(0, WIDTH, HEIGHT)

#направление движения
dx,dy=0,0


#задержка
blok=120
blok1=0


#создаем рабочее окно
pygame.init()
workW=pygame.display.set_mode([WIDTH,WIDTH])

#шрифт
font_shrift=pygame.font.SysFont('Arial', 28, bold=True)
font_end=pygame.font.SysFont('Arial', 50, bold=True)

#очки
shrift=0

#скорость змеи
clock=pygame.time.Clock()



while True:
    #цвет поля
    workW.fill(MainColor)

    render_shrift = font_shrift.render(f'Score:{shrift}', 1, pygame.Color('green'))
    workW.blit(render_shrift, (5, 5))

    #рисуем яблоко и змейку
    [(pygame.draw.rect(workW, ZmeiColor, (i,ii, HEIGHT, HEIGHT))) for i, ii in snake]
    pygame.draw.rect(workW, Apl,(*apple, HEIGHT,HEIGHT))
    #движения змеи
    blok1=blok1+bb
    if blok1 % blok == 0:
        blok1=0
        x+=dx*HEIGHT
        y+=dy*HEIGHT
        snake.append((x,y))
     #делаем змею не бесконечной
        snake=snake[-lenght:]

    pygame.display.flip()
    clock.tick(blok)

# проверка на закрытие приложения
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    #управление змеёй
    key=pygame.key.get_pressed()
    if key[pygame.K_w]:
        dx,dy=0,-1
    if key[pygame.K_s]:
        dx,dy=0,1
    if key[pygame.K_d]:
        dx,dy=1,0
    if key[pygame.K_a]:
        dx,dy=-1,0


#змея съела яблоко
    if snake[-1]== apple:
        apple=randrange(0,WIDTH,HEIGHT),randrange(0,WIDTH,HEIGHT)
        lenght+=1
        shrift+=1
        #если яблоко заспавнилось на змее:
        if apple==snake:
            apple = randrange(0, WIDTH, HEIGHT), randrange(0, WIDTH, HEIGHT)




    #проигрыши
    if x<0 or x >WIDTH-HEIGHT or y<0 or y > WIDTH-HEIGHT or len(snake) != len(set(snake)):
        while True:
            render_end = font_end.render('Конец Игры',1, pygame.Color('red'))
            workW.blit(render_end,(WIDTH//2-120,WIDTH//3))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()



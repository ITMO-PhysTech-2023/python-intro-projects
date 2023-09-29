import pygame
from random import randrange
SIZE=800# размеры поля
SIZE_body=50# шаг змеи
x,y=randrange(0,SIZE,SIZE_body),randrange(0,SIZE,SIZE_body)
apple=randrange(0,SIZE,SIZE_body),randrange(0,SIZE,SIZE_body)
l=1
snake=[(x, y)] # список координат
x1,y1=0,0
fps=10
pygame.init()
sc=pygame.display.set_mode([SIZE, SIZE])
clock=pygame.time.Clock()
while True:
    sc.fill(pygame.Color('black'))# перед каждым след действием красит поле игры в черный
    [(pygame.draw.rect(sc,pygame.Color('green'),(i,j,SIZE_body,SIZE_body))) for i,j in snake]
    pygame.draw.rect(sc,pygame.Color('red'),(*apple,SIZE_body,SIZE_body))
    x+=x1*SIZE_body# движение змеи
    y+=y1*SIZE_body# точнее: координаты увеличиваются на размер ее головы
    snake.append((x,y))
    snake=snake[-l:]
    # поедание яблока
    if snake[-1]==apple:# поедание яблока
        apple=randrange(0,SIZE,SIZE_body),randrange(0,SIZE,SIZE_body)
        l+=1
        fps+=1
    # конец игры
    if x<0 or x>SIZE-SIZE_body or y<0 or y>SIZE-SIZE_body:# условия выхода из игры(если координаты по х и у выходят за пределы(берем - SIZE_body , так как змея может выйти на длину головы, чтобы повернуть)
        break
    if len(snake)!=len(set(snake)):# проверка на самопоедание ( в сете могут быть повторяющиеся координаты => змея уперлась в себя)
        break
    pygame.display.flip()
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
    # управление
    key=pygame.key.get_pressed()
    if key[pygame.K_w]:
        x1,y1=0,-1
    if key[pygame.K_s]:
        x1,y1=0,1
    if key[pygame.K_a]:
        x1,y1=-1,0
    if key[pygame.K_d]:
        x1,y1=1,0
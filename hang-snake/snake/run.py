# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pynput import keyboard
from random import randint
import time
import pygame
from hangman.run import HangmanGame
from printer.secret import Secret
from hangman.provider import RandomLetterProvider, LetterProvider
class eatableobject:

    def random_position(self):
        position = [randint(20, 780), randint(20, 580)]
        return position
class SnakeGame:
    def __init__(self, secrword: Secret, width: int, height: int, headx: int, heady: int,speed:int,length:int):
        self.width = width
        self.height = height
        self.direc = 1
        self.headx = headx
        self.heady = heady
        self.speed = speed
        self.length = length
        self.dis = pygame.display.set_mode((800, 600))
        self.snake_list=[]
        self.color=0
        self.yellow = (255,255,0)
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.list=[0,0]
        self.secret = secrword.garbage()
        self.eatenletters = []
    def draw_snake(self):
        for x in self.snake_list:
            pygame.draw.rect(self.dis, self.color, [x[1], x[0], self.width, self.height])

    def run(self):
        eat=0

        letter = eatableobject()
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Snake')
        pygame.display.update()
        f1 = pygame.font.Font(None, 36)
        positionsx = [0 for t in range(len(self.secret))]
        positionsy = [0 for t in range(len(self.secret))]
        nletter = [' ' for t in range(len(self.secret))]
        game_over = False
        for j in range(len(self.secret)):
            nletter[j] = self.secret[j]
            self.list = letter.random_position()
            positionsx[j]=self.list[0]
            positionsy[j] = self.list[1]
            pygame.display.update()
        while not game_over:
              for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                      game_over = True
              if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_LEFT:
                      if (self.direc== 2) and (self.length>1):
                          text1 = f1.render('Game Over', True, (255, 0, 0))
                          self.dis.blit(text1, (300, 200))
                          break
                      else:
                        self.direc = 4
                  elif event.key == pygame.K_RIGHT:
                      if (self.direc==4) and (self.length>1):
                          text1 = f1.render('Game Over', True, (255, 0, 0))
                          self.dis.blit(text1, (300, 200))
                          break
                      else:
                         self.direc = 2
                  elif event.key == pygame.K_UP:
                      if (self.direc==1) and (self.length>1):
                          text1 = f1.render('Game Over', True, (255, 0, 0))
                          self.dis.blit(text1, (300, 200))
                          break
                      else:
                         self.direc = 3
                  elif event.key == pygame.K_DOWN:

                      if (self.direc==3) and (self.length>1):
                          text1 = f1.render('Game Over', True, (255, 0, 0))
                          self.dis.blit(text1, (300, 200))
                          break
                      else:
                        self.direc = 1
              if (self.direc == 1):
                  self.headx = self.headx + self.speed
                  self.heady = self.heady
              if (self.direc == 2):
                  self.headx = self.headx
                  self.heady = self.heady + self.speed
              if (self.direc == 3):
                  self.headx = self.headx - self.speed
                  self.heady = self.heady
              if (self.direc == 4):
                  self.headx = self.headx
                  self.heady = self.heady - self.speed
              time.sleep(0.1)
              self.color=self.yellow
              self.dis.fill(self.black)
              snake_Head = []
              snake_Head.append(self.headx)
              snake_Head.append(self.heady)
              self.snake_list.append(snake_Head)
              if (self.headx <= 0) or (self.headx>=600) or (self.heady<=0) or (self.heady>=800):
                  text1 = f1.render('Game Over', True, (255, 0, 0))
                  self.dis.blit(text1, (300, 200))
                  pygame.display.update()
                  break;

              for o in range(len(self.secret)):
                  if(self.headx>=positionsy[o]) and (self.headx<=positionsy[o]+19) and (self.heady>=positionsx[o]) and (self.heady<=positionsx[o]+19):
                      self.eatenletters.append(nletter[o])
                      eat+=1
                      positionsy[o]=3000
                      positionsx[o]=3000
                      self.length += 1
                      provider = RandomLetterProvider()
                      secr = Secret()
                      game = HangmanGame(provider, secr, 1, self.eatenletters)
                      game.run()
                      #for j in range(len(self.secret)):
                         # nletter[j] = self.secret[j]
                         #self.list = letter.random_position()
                          #positionsx[j] = self.list[0]
                          #positionsy[j] = self.list[1]
                          #pygame.display.update()
              for j in range(len(self.secret)):
                  text1 = f1.render(nletter[j], True, (255, 0, 0))
                  self.dis.blit(text1, (positionsx[j],positionsy[j]))
                  pygame.display.update()
              if len(self.snake_list) > self.length:
                  del self.snake_list[0]
              self.draw_snake()
              pygame.display.update()
    pygame.quit()


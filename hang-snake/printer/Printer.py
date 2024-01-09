
from snake.run import SnakeGame
from printer.secret import Secret

secr = Secret()
game = SnakeGame(secr,width=10, height=10,headx=100,heady=100,speed=10,length=1)
game.run()
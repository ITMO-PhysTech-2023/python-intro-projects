from snakeclasses import GameSnake


game = GameSnake()
game.Run()
'''
WIDTH, HEIGHT = 10, 10
# можно приделать конфиг-файл с параметрами
direction = (1, 0)

def random_position():
    a, b = randint(0, HEIGHT - 1), randint(0, WIDTH - 1)
    return a, b


def process_press(key):
    # обработчик нажатия на клавиши (можно сделать и поаккуратнее)
    global direction
    match key:
        case keyboard.Key.left:
            direction = (0, -1)
        case keyboard.Key.up:
            direction = (-1, 0)
        case keyboard.Key.right:
            direction = (0, 1)
        case keyboard.Key.down:
            direction = (1, 0)


FIELD = [['.' for i in range(WIDTH)] for i in range(HEIGHT)]

snake = [[randint(0, HEIGHT - 1), randint(0, WIDTH - 1)]]
apple = random_position()
snake_tail = 0
while apple in snake:
    apple = random_position()

# оно умеет мониторить нажатия на кнопки!
with keyboard.Listener(on_press=process_press) as listener:
    while True:
        os.system('cls')

        FIELD = [['.' for i in range(WIDTH)] for i in range(HEIGHT)]

        for elem in snake:  # обновляем змею
            if snake_tail > 0:
                FIELD[elem[0] % WIDTH][elem[1] % HEIGHT] = 'o'
                FIELD[snake[0][0] % WIDTH][snake[0][1] % HEIGHT] = 's'
            else:
                FIELD[snake[0][0]][snake[0][1]] = 's'

        FIELD[apple[0]][apple[1]] = 'a'

        for row in FIELD:  # печатаем все
            print(' '.join(row))
        ###############################
        if snake_tail > 0:
            for i in range(snake_tail, 0, -1):
                snake[i][0] = snake[i - 1][0]
                snake[i][1] = snake[i - 1][1]
        snake[0][0] = (snake[0][0] + direction[0]) % WIDTH
        snake[0][1] = (snake[0][1] + direction[1]) % HEIGHT

        if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
            apple = random_position()
            snake_tail += 1
            snake.insert(0, [snake[0][0] + direction[0], snake[0][1] + direction[1]])

        time.sleep(0.5)
'''
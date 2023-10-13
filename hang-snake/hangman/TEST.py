from common.util import clear_terminal


def create_secret():
    return 'capybara'

SECRET = create_secret()
n = len(SECRET)
GUESSED = ['_' for _ in range(n)]
FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''.split('\n')
FIELD = FINAL_FIELD
HUMAN = [
    (3, 3),
    (4, 3),
    (4, 2),
    (4, 4),
    (5, 2),
    (5, 4)
]


class field:
    def __init__(self):
        for cell in HUMAN:
            FIELD[cell[0]][cell[1]] = ' '
        human_parts = 0
        ch = 0  # индекс части тела
        chasti_tela = ['o', '|', '/', '\\', '/', '\\']
        return FIELD
print(field)
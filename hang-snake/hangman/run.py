from common.printer import DefaultPrinter, Printer
# from common.util import clear_terminal
from common.providers import LetterProvider, RandomLetterProvider, create_secret


FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''.split('\n')
HUMAN = [
    (3, 3),
    (4, 3),
    (4, 2),
    (4, 4),
    (5, 2),
    (5, 4)
]
HUMAN_PARTS = len(HUMAN)


class Field:
    def __init__(self):
        self.number_mistakes = HUMAN_PARTS
        self.matrix = [
            list(row)
            for row in FINAL_FIELD
        ]
        for row, col in HUMAN:
            self.matrix[row][col] = ' '

    @property
    def width(self):
        return max([len(row) for row in FINAL_FIELD])

    def add_human_part(self):
        row, col = HUMAN[-self.number_mistakes]
        self.number_mistakes -= 1
        self.matrix[row][col] = FINAL_FIELD[row][col]


class Hangmangame:
    def __init__(
            self,
            letter_provider: LetterProvider,
            printer: Printer
    ):
        self.field = Field()
        self.provider = letter_provider
        self.printer = printer
        self.word = create_secret()
        self.n = len(self.word)
        self.guessed = ['_' for _ in range(self.n)]

        self.number_of_errors = 0
        self.MAX_ERRORS = 10

    def read_guess(self) -> str:
        while True:
            letter = self.provider.get_next_letter().lower()
            if len(letter) != 1 and ord(letter) < ord('a') or ord(letter) > ord('z'):
                print('Invalid guess! Try again')
                continue
            return letter

    def check_guess(self, letter: str):
        if letter in self.word:
            new = ""
            for i in range(len(self.word)):
                if letter == self.word[i]:
                    new += letter
                else:
                    new += self.guessed[i]
            self.guessed = new
        else:
            print('There is no such letter in word.')
            self.field.add_human_part()

    def check_possibility(self):
        while True:
            if self.guessed != self.word and\
               self.field.number_mistakes > 0:
                return

    def is_won(self) -> bool:
        return self.guessed == self.word

    def is_lost(self) -> bool:
        return self.field.number_mistakes == 0

    def step(self):
        letter = self.read_guess()
        self.check_guess(letter)

    def build_matrix(self):
        delta = self.field.width - len(self.guessed)
        last_row = [' ' for _ in range(delta // 2)] + list(self.guessed)
        out = self.field.matrix + [
            [],
            last_row
        ]
        return out

    def show(self):
        extra_lines = []
        if self.is_won():
            statement = "Congratulations!The word was ", self.word
            extra_lines.append(statement)
        if self.is_lost():
            statement = "Game over. The word was ", self.word
            extra_lines.append(statement)
        matrix = self.build_matrix()
        for line in extra_lines:
            matrix += [list(line)]
        self.printer.print_field(matrix)

    def run(self):
        self.show()
        while True:
            self.check_possibility()
            self.step()
            self.show()
            if self.is_lost() or self.is_won():
                self.show()
                break


if __name__ == '__main__':
    provider = RandomLetterProvider()
    game = Hangmangame(provider, DefaultPrinter())
    game.run()

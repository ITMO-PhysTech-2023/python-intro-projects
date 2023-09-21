import random


class Word:
    @classmethod
    def select_random_word(cls):
        random_words = ['war', 'world', 'love', 'peace', 'flower', 'music', 'house', 'animal',
                        'window', 'bridge', 'cat', 'dog', 'robot', 'human', 'tree', 'cloud',
                        'car', 'bus', 'football', 'basketball', 'ocean', 'sea', 'memory', 'brain']
        return random_words[random.randint(0, len(random_words))]


class Field:
    @classmethod
    def print_field(cls, count_mistakes):
        human = ['   o    |', '  /|\   |', '  / \   |']
        print('   +----+')
        for i_line in range(7):
            if count_mistakes > 0:
                print('   |    |')
                count_mistakes -= 1
            elif i_line == 6:
                print('\n'.join(human))
            else:
                print('        |')
        print('_______/|\_')


class Check:
    def __init__(self, word):
        self.word = word
        self.check_word = list(word)
        self.correct_letters = list()
        self.introduced_letters = list()

    def check_letter(self, enter_letter):
        self.introduced_letters.append(enter_letter)
        if enter_letter in self.check_word:
            self.correct_letters.append(enter_letter)
            self.check_word.remove(enter_letter)
            return True
        return False

    def input_check(self, enter_letter):
        if enter_letter in self.introduced_letters and enter_letter not in self.check_word:
            return False
        return True

    def all_letters_are_guessed(self):
        if len(self.check_word) == 0:
            return True
        return False

    def coincidence(self):
        enter_word = input()
        if enter_word == self.word:
            return True
        return False

    @classmethod
    def check_len(cls, enter_symbols):
        if len(enter_symbols) != 1:
            return False
        return True


class Game:
    @classmethod
    def launching_the_game(cls):
        secret_word = Check(Word.select_random_word())
        counter = 6
        print('Мы загадали слово. Игра начинается!')
        Field.print_field(0)
        while counter > 0:
            while True:
                while True:
                    enter_letter = input('Введите букву: ')
                    if not secret_word.check_len(enter_letter):
                        print('Ошибка ввода. Нужно ввести один символ!')
                    else:
                        break
                if not secret_word.input_check(enter_letter):
                    print('Вы уже вводили эту букву!')
                else:
                    break
            if secret_word.check_letter(enter_letter):
                print('Вы угадали букву {}!'.format(enter_letter))
                if secret_word.all_letters_are_guessed():
                    print('Список угаданных букв:', secret_word.correct_letters)
                    print('Вы угадали все буквы из слова. Теперь подумайте, что это за слово?', end=' ')
                    while True:
                        if secret_word.coincidence():
                            print('Мы загадали слово {}. Вы победили!'.format(secret_word.word))
                            break
                        else:
                            print('Вы немного ошиблись. Подумайте ещё!', end=' ')
                    break
            else:
                counter -= 1
                print('Буквы {} нет в загаданном слове. Осталось попыток: {}'.format(
                    enter_letter,
                    counter))
            Field.print_field(6 - counter)
            print('Список угаданных букв:', secret_word.correct_letters)
        else:
            print('К сожалению, вы проиграли:( Мы загадали слово:', secret_word.word)

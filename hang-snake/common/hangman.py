def strfindall(s, l):
    return list(map(lambda x: x[0], filter(lambda x: x[1] == l, enumerate(s))))

class Hangman:
    word: str = ""
    mask: int = 0
    fails: int = 0

    def __init__(self, word):
        self.word = word
    def get_partial_word(self):
        return "".join(
                map(
                    lambda x: x[1] if self.mask & (1 << x[0]) != 0 else "_", 
                        enumerate(self.word)))
    def guess(self, l):
        ids = strfindall(self.word, l)
        if len(ids) == 0:
            self.fails += 1
            return False
        for o in ids:
            self.mask |= 1 << (o)
        return True


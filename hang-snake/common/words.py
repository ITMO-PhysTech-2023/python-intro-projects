# Parse files from lang/hangman-<WORDTY>.txt
# Words from WORD_TYPES locales can be obtained in words("LOCALE")

from random import choice, shuffle

WORD_TYPES = ["ru"]
_WORDS = dict()
for l in WORD_TYPES:
    with open(f"lang/hangman-{l}.txt", "r") as f:
        # remove newlines and empty lines
        _WORDS[l] = list(
                filter(
                    lambda x: x != "", 
                    map(
                        # TODO: trim
                        lambda x: x.replace('\n', '').replace('\r', ''),
                        f.readlines())))

"""
ty -- type of word. Can be 'ru'
"""
def words(ty: str = "ru") -> str:
    return _WORDS[ty]

def choice_word(ty: str = "ru") -> str:
    return choice(_WORDS[ty])

def letter_noise(cnt: int = -1):
    letters = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    shuffle(letters)
    return letters if cnt == -1 else letters[:cnt]


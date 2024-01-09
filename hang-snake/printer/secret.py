import random
class Secret:
    def create_secret(self):
        word = 'capybara'
        return word
    def garbage(self):
        rubbish = [' ' for _ in range(4)]
        word = 'capybara'
        for i in range(4):
            rubbish[i] = chr(random.randint(ord('a'), ord('z')))
            word = word + rubbish[i]
        return word
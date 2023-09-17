dictionary = ['capybara', 'giraffe', 'bear', 'horse', 'cat']

FIELDS = [
    r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
''',

r'''
   +----+
   |    |
   o    |
  /|\   |
        |
_______/|\_
''',

r'''
   +----+
   |    |
   o    |
        |
        |
_______/|\_
''',

r'''
   +----+
        |
        |
        |
        |
_______/|\_
''',

r'''
   
        |
        |
        |
        |
_______/|\_
''',

r'''

        
        
        
        
_______/|\_
''',

r'''

        
        
        
        

'''
]

import os


def terminal_size():
    return os.get_terminal_size()


def clear_terminal():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)

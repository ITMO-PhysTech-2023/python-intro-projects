from googletrans import Translator, constants
from pprint import pprint
translator = Translator()
#translation = translator.translate("Hola Mundo", dest="ru")
#print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
def trans(text):
    translation = translator.translate(text, dest="ru")
    return(f"{translation.text}")
print(trans("I love ITMO"))
from pywebio.output import *
from pywebio.input import *
from pywebio.session import set_env, go_app
from pywebio import start_server
from pywebio.output import output as output

import PIL
import asyncio
import sys

try:
    print(sys.argv[1])
    port = sys.argv[1]
except:
    port = 80

# put_button("label", onclick=self.callback, color="primary", small=False, link_style=False, outline=True)
# put_button('ok2', onclick=self.callback)
# put_button('ok1', onclick=self.callback)
class Account_Manager:
    def __init__(self):
        pass
    def login_validate(self):
        pass

class Select_24_game:
    def to_tournement(self):
        pass
    def to_traning(self):
        pass

    def run(self):
        put_image(PIL.Image.open("white.png"), format="png", width="100", height="100")
        put_row([
            put_image(PIL.Image.open("24_t.png"), format="png", title='', width="100", height="100").onclick(self.to_tournement).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
            put_image(PIL.Image.open("24_training.png"), format="png", title='', width="100", height="100").onclick(self.to_traning).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
        ], size=10)

        put_image(PIL.Image.open("white.png"), format="png", width="10", height="10")
        put_row([
            put_text("Tournament"),
            put_text("Training"),
        ], size=10)

class Main_Menu:
    def to_24(self):
        clear(scope=None)
        start_select_24_game()

    def run(self):
        put_image(PIL.Image.open("cover.png"), format="png")
        put_row([
            put_image(PIL.Image.open("24.png"), format="png", title='24 games', width="100", height="100").onclick(self.to_24).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
        ], size=10)
        put_image(PIL.Image.open("white.png"), format="png", width="10", height="10")
        put_row([
            put_text("24 games"),
        ], size=10)


def start_main_menu():
    set_env(title='clicking')
    main_menu=Main_Menu()
    main_menu.run()

def start_select_24_game():
    select_24_game=Select_24_game()
    select_24_game.run()

if __name__ == '__main__':
    start_server(start_main_menu, port=port)

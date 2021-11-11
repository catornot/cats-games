from pywebio.output import *
from pywebio.input import *
from pywebio.session import set_env
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

class Main_Menu:
    def __init__(self):
        self._run = True

    def to_24(self):
        pass

    def mainMenu(self):
        put_image(PIL.Image.open("white.png"), format="png")
        put_row([
            put_image(PIL.Image.open("24.png"), format="png", title='24 games', width="100", height="100").onclick(self.to_24).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
        ], size=10)

        put_row([
            put_text("24 games"),
            put_text("24 games"),
            put_text("24 games"),
        ], size=10)

    def run(self):
        self.mainMenu()


def start_main_menu():
    set_env(title='clicking')
    main_menu=Main_Menu()
    main_menu.run()

if __name__ == '__main__':
    start_server(start_main_menu, port=port)

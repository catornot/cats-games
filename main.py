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

class Client:
    def __init__(self):
        self._run = True
        self.screen = 0
        self.counter = 0

    def callback(self):
        self.var.reset()
        self.counter += 1
        self.var.append("click " + str(self.counter))

    def mainMenu(self):
        self.var = output("")
        put_scrollable(self.var)
        put_row([
            put_image(PIL.Image.open("24.png"), format="png", title='', width="100", height="100").onclick(self.callback).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
            put_button("label", onclick=self.callback, color="primary",
                       small=False, link_style=False, outline=True),
            put_button('ok2', onclick=self.callback),
            put_button('ok1', onclick=self.callback),
        ], size=50)
    def run(self):
        set_env(title='clicking')
        if self.screen == 0:
            self.mainMenu()


client=Client()

if __name__ == '__main__':
    start_server(client.run, port=port)

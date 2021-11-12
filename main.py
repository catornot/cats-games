from pywebio.output import *
from pywebio.input import *
from pywebio.session import set_env, go_app
from pywebio import start_server
from pywebio.output import output as output

import PIL
import asyncio
import sys
import pickle

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
    def login_validate(self,data):
        with open("info.txt","rb") as info:
            infomation = pickle.load(info)
        if data["nickname"] in infomation.keys():
            if not infomation[data["nickname"]][1] == data["password"]:
                return ("password","wrong password")
            else:
                clear()
                start_main_menu()
        else:
            return ("nickname","wrong nickname")

    def signup_validate(self,data):
        with open("info.txt","rb") as info:
            infomation = pickle.load(info)

        if not data["nickname"] in infomation.keys():
            infomation[data["nickname"]] = [data["email"],data["password"],data["nickname"]]
            with open("info.txt","wb") as info:
                pickle.dump(infomation,info)
        else:
            return ("nickname", "nickname already exist" )

class login_Screen:
    def to_signup(self):
        clear()
        self.run_signup()
    def to_login(self):
        clear()
        self.run_login()
    def run_login(self):
        put_markdown("No account?, Sign up!").onclick(self.to_signup)
        data = input_group("Sign in",[
            input('Input your nickname', name='nickname'),
            input('Input your password', name='password', type=PASSWORD)
        ], validate=account_manager.login_validate)

    def run_signup(self):
        put_markdown("Already have account?, Sign in!").onclick(self.to_login)
        data = input_group("Sign in",[
            input('Input your nickname', name='nickname'),
            input('Input your email', name='email'),
            input('Input your password', name='password', type=PASSWORD)
        ], validate=account_manager.signup_validate)
        self.to_login()

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
        clear()
        start_select_24_game()
    def to_signin(self):
        clear()
        start_signin()

    def run(self):
        put_row([
        put_image(PIL.Image.open("cover.png"), format="png"),
        put_button('sign in', onclick=self.to_signin)
        ], size=10)
        put_row([
            put_image(PIL.Image.open("24.png"), format="png", title='24 games', width="100", height="100").onclick(self.to_24).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
        ], size=10)
        put_image(PIL.Image.open("white.png"), format="png", width="10", height="10")
        put_row([
            put_text("24 games"),
        ], size=10)

account_manager = Account_Manager()

def start_main_menu():
    set_env(title='clicking')
    main_menu=Main_Menu()
    main_menu.run()

def start_select_24_game():
    select_24_game=Select_24_game()
    select_24_game.run()
def start_signin():
    login_screen=login_Screen()
    login_screen.run_login()


if __name__ == '__main__':
    start_server(start_main_menu, port=port)

from pywebio.output import *
from pywebio.input import *
from pywebio.session import set_env, run_js, eval_js
from pywebio import start_server
from pywebio.output import output as output

import PIL
import asyncio
import sys
import pickle
import base64
import re
from Algorithm24 import solve, get_random

try:
    print(sys.argv[1])
    port = sys.argv[1]
except:
    port = 80

# put_button("label", onclick=self.callback, color="primary", small=False, link_style=False, outline=True)
# put_button('ok2', onclick=self.callback)
# put_button('ok1', onclick=self.callback)


class Account_Manager:
    def check_email(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return True
        else:
            return False

    def login_validate(self, data):
        with open("info.txt", "rb") as info:
            infomation = pickle.load(info)
        if data["nickname"] in infomation.keys():
            if not infomation[data["nickname"]][1] == base64.standard_b64encode(data["password"].encode()):
                return ("password", "wrong password")
            else:
                setcookie("nickname", data["nickname"], days=0.1)
                run_js("location.reload(true);")
                # clear()
                # start_main_menu()
        else:
            return ("nickname", "wrong nickname")

    def signup_validate(self, data):
        with open("info.txt", "rb") as info:
            infomation = pickle.load(info)

        if not data["nickname"] in infomation.keys() and data["nickname"] != "":
            if self.check_email(data["email"]):
                infomation[data["nickname"]] = [data["email"], base64.standard_b64encode(
                    data["password"].encode()), data["nickname"]]
                with open("info.txt", "wb") as info:
                    pickle.dump(infomation, info)
            else:
                return ("email", "email is not formated right")

        else:
            return ("nickname", "nickname already exist or wrong formating")

    def account_exist(self, nickname):
        with open("info.txt", "rb") as info:
            infomation = pickle.load(info)
        if nickname in infomation.keys():
            return True
        else:
            return False


class login_Screen:
    def to_signup(self):
        clear()
        self.run_signup()

    def to_login(self):
        clear()
        self.run_login()

    def to_menu(self):
        run_js("location.reload(true);")

    def run_login(self):
        put_markdown("No account?, Sign up!").onclick(self.to_signup)
        put_markdown("Back").onclick(self.to_menu)
        data = input_group("Sign in", [
            input('Input your nickname', name='nickname'),
            input('Input your password', name='password', type=PASSWORD),
        ], validate=account_manager.login_validate)

    def run_signup(self):
        put_markdown("Already have account?, Sign in!").onclick(self.to_login)
        data = input_group("Sign up", [
            input('Input your nickname', name='nickname'),
            input('Input your email', name='email'),
            input('Input your password', name='password', type=PASSWORD),
        ], validate=account_manager.signup_validate)
        self.to_login()


class T_24:
    def run_train(self):
        get_random()


class Select_24_game:
    def to_tournement(self):
        pass

    def to_traning(self):
        clear()
        start_train_24()

    def run(self):
        put_image(PIL.Image.open("white.png"),
                  format="png", width="100", height="100")
        put_row([
            put_image(PIL.Image.open("24_t.png"), format="png", title='', width="100", height="100").onclick(
                self.to_tournement).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
            put_image(PIL.Image.open("24_training.png"), format="png", title='', width="100", height="100").onclick(
                self.to_traning).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
        ], size=10)

        put_image(PIL.Image.open("white.png"),
                  format="png", width="10", height="10")
        put_row([
            put_text("Tournament"),
            put_text("Training"),
        ], size=10)


class Main_Menu:
    def ignore(self):
        pass

    def to_24(self):
        clear()
        start_select_24_game()

    def to_signin(self):
        clear()
        start_signin()

    def tf(self):
        run_js("open('https://www.youtube.com/watch?v=j7niWUth9_Y');")

    def run(self):
        if getcookie("nickname") == "Guest":
            text = 'sign in'
        else:
            text = 'signed in as {0}'.format(getcookie("nickname"))
        put_row([
            put_image(PIL.Image.open("cover.png"), format="png"),
            put_button(text, onclick=self.to_signin),

        ], size=10)
        put_row([
            put_image(PIL.Image.open("24.png"), format="png", title='24 games', width="100", height="100").onclick(
                self.to_24).style("outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
        ], size=10)
        put_image(PIL.Image.open("white.png"),
                  format="png", width="10", height="10")
        put_row([
            put_text("24 games"),
        ], size=10)
        put_image(PIL.Image.open("white.png"),
                  format="png", width="10", height="200")
        put_text("Stand by for Titanfall!").onclick(self.tf)


account_manager = Account_Manager()

# with open("info.txt","wb") as info:
#     pickle.dump({},info)

def playsound(url):
    run_js('''var audio = new Audio(url);
        audio.play();''',url = url)


def setcookie(key, value, days=0):
    run_js("setCookie(key, value, days)", key=key, value=value, days=days)


def getcookie(key):
    return eval_js("getCookie(key)", key=key)


def start_main_menu():
    main_menu = Main_Menu()
    main_menu.run()


def start_select_24_game():
    select_24_game = Select_24_game()
    select_24_game.run()


def start_signin():
    login_screen = login_Screen()
    login_screen.run_login()


def start_train_24():
    train_24 = T_24()
    train_24.run_train()


def _start_server():
    set_env(title="cat's games")
    run_js("""
    window.setCookie = function(name,value,days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }
    window.getCookie = function(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }
    """)
    if getcookie("nickname") == None:
        setcookie("nickname", "Guest", days=0.1)
    elif not account_manager.account_exist(getcookie("nickname")) and not getcookie("nickname") == "Guest":
        print("no account found :{0}".format(getcookie("nickname")))
        setcookie("nickname", "Guest", days=0.1)

    start_main_menu()


if __name__ == '__main__':
    start_server(_start_server, port=port)

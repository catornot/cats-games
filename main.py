from pywebio.output import *
from pywebio.input import *
from pywebio.session import set_env, run_js, eval_js, go_app
from pywebio import start_server
from pywebio.output import output as output

import PIL
import asyncio
import sys
import pickle
import base64
import re
import ast
import time
import requests
import json
from Algorithm24 import solve, get_random

try:
    print(sys.argv[1])
    port = sys.argv[1]
except:
    port = 80


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

#login and sign up page
def to_signup():
    clear()
    run_signup()

def to_login():
    clear()
    run_login()
def run_login():
    put_markdown("**No account?, Sign up!**").onclick(to_signup)
    put_link('Back', app='menu')
    data = input_group("Sign in", [
        input('Input your nickname', name='nickname'),
        input('Input your password', name='password', type=PASSWORD),
    ], validate=account_manager.login_validate)

def run_signup():
    put_markdown("Already have account?, Sign in!").onclick(to_login)
    data = input_group("Sign up", [
        input('Input your nickname', name='nickname'),
        input('Input your email', name='email'),
        input('Input your password', name='password', type=PASSWORD),
    ], validate=account_manager.signup_validate)
    to_login()


#training page
def run_training():
    put_text("Getting a problem ready")

    iteration = 0
    Continue = True
    while Continue:
        iteration += 1
        result = get_random()
        print(result)
        if eval(result[0]) == 24:
            clear()
            Continue = False
        elif iteration > 100:
            clear()
            put_error("Nothing found : NotImplementedError")
            raise NotImplementedError
    Time = time.time()
    put_row([
        put_markdown(r""" # 24 game
            Use operators **+, -, / and \*** and numbers **{0}, {1}, {2} and {3}** to get the number 24.
            **You can only use each number once.**
              
        """.format(result[1][0],result[1][1],result[1][2],result[1][3]), lstrip=True),
        put_button("back", onclick=lambda: go_app('menu',False)),

    ], size=10)

    iteration = 0
    Continue = True
    prev_value = ""
    while Continue:
        iteration += 1

        prev_value = answer2 = answer = input('Input your answer', validate=validate_expression,value = prev_value)

        for x in ["(",")","*","/","+","-"]:
            answer2 = answer2.replace(x,"")

        valid = True
        for i in result[1]:

            if not str(i) in list(answer2) and valid:
                valid = False
                put_warning("does not contain all required numbers.", closable=True)

            try:
                e = list(answer2)
                e.pop(list(answer2).index(str(i)))

                if str(i) in e and valid:
                    print(1)
                    valid = False
                    put_warning("contains duplicate required numbers.", closable=True)

            except ValueError:
                pass

        if valid:
            tree = ast.parse(answer, mode='eval')
            result2 = eval(compile(tree, filename='', mode='eval'))

            if result2 == 24:    
                Continue = False
            else:
                put_warning("Doesn't equal to 24", closable=True)

        elif iteration > 100:
            put_warning("{0}, You are incapable!".format(getcookie("nickname")), closable=True)
            run_js("location.reload(true);")

    clear()

    put_markdown(r""" # Your did it!
        You found how to get the number 24 out of **{0}, {1}, {2} and {3}**.
        It took you {4} sec
          
    """.format(result[1][0],result[1][1],result[1][2],result[1][3],time.time() - Time), lstrip=True)
        
    put_button("Continue", onclick=lambda: go_app('training'))




def validate_expression(expression):
    try:
       tree  = ast.parse(expression, mode='eval')
    except SyntaxError:
        return "Not a Python expression"
    if not all(isinstance(node, (ast.Expression,
            ast.UnaryOp, ast.unaryop,
            ast.BinOp, ast.operator,
            ast.Num)) for node in ast.walk(tree)):
        return "not a mathematical expression (numbers and operators)"


#Main menu page
def blank():
    run_js("open('https://r.honeygain.me/PROOV41FC7');")

def run_menu():
    if getcookie("nickname") == "Guest":
        text = 'sign in'
    else:
        text = 'signed in as {0}'.format(getcookie("nickname"))

    put_row([
        put_image(PIL.Image.open("cover.png"), format="png"),
        put_button(text, onclick=lambda: go_app('signin',False)),

    ], size=10)
    put_row([
        put_image(PIL.Image.open("24_t.png"), format="png", title='', width="100", height="100").onclick(
            lambda: put_warning("it will come", closable=True) ).style(
            "outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
        put_image(PIL.Image.open("24_training.png"), format="png", title='', width="100", height="100").onclick(
            lambda: go_app('training',False) ).style(
            "outline: 4px solid #e73;outline-offset: 4px;background: #ffa"),
    ], size=10)

    put_image(PIL.Image.open("white.png"),
              format="png", width="10", height="10")

    put_row([
        put_text("Tournament"),
        put_text("Training"),
    ], size=10)

    put_image(PIL.Image.open("white.png"),
              format="png", width="10", height="200")

    put_link('visit vex\'s leaderboard of advent of code', app='api')
    put_text("")
    put_link(("Stand by for Titanfall!"), url='https://www.youtube.com/watch?v=j7niWUth9_Y',new_window = True)
    put_text("ad").onclick(blank)

#vex leaderboard for https://adventofcode.com/2021
def adventofcode():
    s = requests.Session()
    r = s.get('https://adventofcode.com/2021/leaderboard/private/view/1516691.json',cookies = {"session":"53616c7465645f5f90c07871a62bad84e0e7431b2f06b65e3c5983b16b61306edd0eb2e5e9d2338e6c1d1d8f1ea6a825"})
    Json = r.json()
    output_list = [[span('Name',row=1), span('score', col=1)]]

    for x in Json["members"].keys():
        output_list.append(
            [
            Json["members"][x]["name"],
            Json["members"][x]["local_score"],
            ]
        )


    put_table(output_list)
    # put_text(json.dumps(Json,indent=4, sort_keys=True))



#setting up account manager
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

    go_app('menu',False)


if __name__ == '__main__':
    start_server({"index":_start_server,"menu":run_menu,"training":run_training,"signin":run_login,"api":adventofcode}, port=port)

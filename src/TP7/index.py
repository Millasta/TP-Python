import cgi
import hashlib
import secrets
from os import environ

message = ""
cookie_setter = ""
parameters = cgi.FieldStorage()

SALT = "TOTO"
KEY = None
TAG = None
NONCE = None

def get_pwd_by_login(login):
    with open("data.txt", "rt") as file:
        found = False
        for line in file:
            if found:
                return line
            if (login+'\n') == line:
                found = True
    return None

def login():
    global KEY
    global message
    global cookie_setter

    login = str(parameters.getvalue("login"))
    password = str(parameters.getvalue("password")) + login + SALT
    true_password = get_pwd_by_login(login)

    if true_password is None:
        message = "Ce login n'existe pas !"
        return

    hashed = hashlib.sha512(password.encode()).hexdigest()
    if hashed+'\n' == true_password:
        KEY = hashed[0:32]

        if environ.keys().__contains__('HTTP_COOKIE'):
            if(environ['HTTP_COOKIE'] is not ""):
                for cookie in map(str.strip, str.split(environ['HTTP_COOKIE'], ';')):
                    (key, value) = str.split(cookie, '=');
                    if key == "Token":
                        cookie_token = value
                        # Checking session tokens
                        with open("sessions.txt", "rt") as file:
                            found = False
                            for line in file:
                                if found:
                                    pass
                                if (cookie_token + '\n') == line:
                                    found = True
                        if(found):
                            message = "Vous etes deja connecte ! " \
                                      "<a href='home.py'>Accueil</a>" # home link
                            return

        token = str(secrets.token_hex(16))
        with open("sessions.txt", "a+") as file:
            file.write(login + '\n' + token + '\n')
        cookie_setter = "Set-Cookie:Token = "  + token + " ;\r\n"
        message =   "Vous etes bien connecte ! " \
                    "<a href='home.py'>Accueil</a>" # home link
    else:
        message = "Mot de passe incorrect !"

def deconnect():
    global cookie_setter

    if environ.keys().__contains__('HTTP_COOKIE'):
        if (environ['HTTP_COOKIE'] is not ""):
            for cookie in map(str.strip, str.split(environ['HTTP_COOKIE'], ';')):
                (key, value) = str.split(cookie, '=')
                cookie_token = value
                lines = None
                with open("sessions.txt", "r") as f:
                    lines = f.readlines()
                with open("sessions.txt", "w") as f:
                    for i in range(1, len(lines), 2):
                            if lines[i].strip("\n") != cookie_token: # On retire le token connecté et son login
                                f.write(lines[i - 1])
                                f.write(lines[i])
                cookie_setter = "Set-Cookie:Token = None;\r\n"

if(parameters.getvalue("deconnect") != None):
    deconnect()

if(parameters.getvalue("login") != None and parameters.getvalue("password") != None):
    login()

print(cookie_setter + "Content-type:text/html charset=utf-8\r\n")
html = """<!DOCTYPE html>
<head>
 <title>Connection</title>
</head>
<body>
 <form action="/index.py" method="post">
 <input type="text" name="login" value="Login" />
 <input type="password" name="password" value="Password" />
 <input type="submit" name="send" value="Se connecter">
 </form>
 <p><a href="register.py">S'enregistrer</a></p>
 <p><b>""" + message + """</b></p>
</body>
</html>
"""
print(html)
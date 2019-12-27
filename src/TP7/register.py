import cgi
import hashlib

SALT = "TOTO"
KEY = None
TAG = None
NONCE = None

message = ""
parameters = cgi.FieldStorage()

def get_pwd_by_login(login):
    with open("data.txt", "rt") as file:
        found = False
        for line in file:
            if found:
                return line
            if (login+'\n') == line:
                found = True
    return None

def register():
    global SALT
    global message

    login = str(parameters.getvalue("login"))
    password = str(parameters.getvalue("password")) + login + SALT

    if len(login) <= 1 or len(password) <= 1:
        message = "Login or password too short !"
        return
    if get_pwd_by_login(login) is not None:
        message = "This login is already taken !"
        return

    hashed = hashlib.sha512(password.encode()).hexdigest()

    with open("data.txt", "at") as file:
        file.write(login)
        file.write('\n')
        file.write(hashed)
        file.write('\n')

    message = "Registered, you can now log in !"

if(parameters.getvalue("login") != None and parameters.getvalue("password") != None):
    register()

print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<head>
 <title>Enregistrement</title>
</head>
<body>
 <form action="/register.py" method="post">
 <input type="text" name="login" value="Login" />
 <input type="text" name="password" value="Password" />
 <input type="submit" name="send" value="S'enregistrer">
 </form>
 <p><a href="index.py">Retour</a></p>
 <p><b>""" + message + """</b></p>
</body>
</html>
"""
print(html)
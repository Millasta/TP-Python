import cgi
from os import environ

body = ""

# Check connection
if environ.keys().__contains__('HTTP_COOKIE'):
    if (environ['HTTP_COOKIE'] is not ""):
        for cookie in map(str.strip, str.split(environ['HTTP_COOKIE'], ';')):
            (key, value) = str.split(cookie, '=');
            if key == "Token":
                cookie_token = value
                with open("sessions.txt", "rt") as file:
                    found = False
                    login = ""
                    last_line = ""
                    for line in file:
                        if (cookie_token + '\n') == line:
                            found = True
                            login = last_line
                            pass
                        last_line = line
                    if found: #connected
                        body =  """
                                <p>Vous êtes connecté """ + login + """!</p> 
                                <form action="/index.py" method="post">
                                    <input type="hidden" name="deconnect" value=1 />
                                    <input type="submit" name"Send" value="Se deconnecter" />
                                </form>
                                """ + body
                    else:
                        body = """
                                <p>Vous devez d'abord ous connecter !</p> 
                                <form action="/index.py" method="post">
                                    <input type="hidden" name="deconnect" value=1 />
                                    <input type="submit" name"Send" value="Se connecter" />
                                </form>
                                """ + body


print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<head>
 <title>Accueil</title>
</head>
<body>
""" + body + """
</body>
</html>
"""
print(html)
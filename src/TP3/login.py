import tkinter
import hashlib

from Crypto.Cipher import AES
from tkinter.filedialog import askopenfilename
from tkinter import *

SALT = "TOTO"
KEY = None
TAG = None
NONCE = None

## VIEW
fenetre = Tk()
fenetre.title("TP3 - Login")
fenetre.geometry("200x200")
fenetre.resizable(0, 0)

label_login = tkinter.Label(text="Login:")
label_login.pack(fill=tkinter.X)

field_login = tkinter.Entry()
field_login.pack(fill=tkinter.X)

label_password = tkinter.Label(text="Password:")
label_password.pack(fill=tkinter.X)

field_password = tkinter.Entry(show="*")
field_password.pack(fill=tkinter.X)

button_login = tkinter.Button(text="Login")
button_login.pack(fill=tkinter.X)

button_register = tkinter.Button(text="Register")
button_register.pack(fill=tkinter.X)

button_encrypt_file = tkinter.Button(text="Encrypt", state="disabled")
button_encrypt_file.pack(fill=tkinter.X)

button_decrypt_file = tkinter.Button(text="Decrypt", state="disabled")
button_decrypt_file.pack(fill=tkinter.X)

label_state = tkinter.Label(text="Status")
label_state.pack(fill = tkinter.X)

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
    global field_login
    global field_password
    global label_state
    global SALT

    login = field_login.get()
    password = field_password.get() + login + SALT

    if len(login) <= 1 or len(password) <= 1:
        label_state.config(text="Login or password too short !")
        return
    if get_pwd_by_login(login) is not None:
        label_state.config(text="This login is already taken !")
        return

    hashed = hashlib.sha512(password.encode()).hexdigest()

    with open("data.txt", "at") as file:
        file.write(login)
        file.write('\n')
        file.write(hashed)
        file.write('\n')

    label_state.config(text="Registered, you can now log in.")
button_register.config(command=register)

def login():
    global field_login
    global field_register
    global label_state
    global button_decrypt_file
    global button_encrypt_file
    global KEY

    login = field_login.get()
    password = field_password.get() + login + SALT
    true_password = get_pwd_by_login(login)

    if true_password is None:
        label_state.config(text="This login is not registered yet !")
        return

    hashed = hashlib.sha512(password.encode()).hexdigest()
    if hashed+'\n' == true_password:
        label_state.config(text="Successfully logged in !")
        KEY = hashed[0:32]
        button_decrypt_file.config(state="normal")
        button_encrypt_file.config(state="normal")
    else:
        label_state.config(text="Incorrect password !")
        button_decrypt_file.config(state="disabled")
        button_encrypt_file.config(state="disabled")
button_login.config(command=login)

def encrypt_file() :
    global KEY

    filename = askopenfilename(initialdir="C:/Users/Valentin MAURICE/PycharmProjects/PolytechTP/src/TP3", title="Select file to encrypt",
                                               filetypes=(("texte files", "*.txt"), ("all files", "*.*")))
    with open(filename, "rt") as file:
        try:
            text = str(file.read())
            cipher = AES.new(KEY.encode("utf8"), AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(text.encode("utf8"))
            new_filename = filename[0:len(filename)-4] + "_ciphered.bin"
            print(new_filename)

            with open(new_filename, "wb") as file_out:
                [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
            label_state.config(text="Successful cipher")
        except:
            label_state.config(text="Cipher failed")
            print("Cipher failed, ", sys.exc_info()[0])
button_encrypt_file.config(command=encrypt_file)

def decrypt_file():
    global KEY

    try:
        filename = askopenfilename(initialdir="C:/Users/Valentin MAURICE/PycharmProjects/PolytechTP/src/TP3",
                               title="Select file to decrypt",
                               filetypes=(("bin files", "*.bin"), ("all files", "*.*")))

        data = None

        with open(filename, "rb") as file_in:
            nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
            cipher = AES.new(KEY.encode("utf8"), AES.MODE_EAX, nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)

        new_filename = filename[0:len(filename) - 13] + "_decrypt.txt"

        with open(new_filename, "wt") as file_out:
            file_out.write(data.decode("utf8"))
        label_state.config(text="Sucessfull decrypt")
    except Exception as e:
        label_state.config(text="Decrypt failed")
        print("Decrypt failed, ", e)


button_decrypt_file.config(command=decrypt_file)

fenetre.mainloop()

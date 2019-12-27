import tkinter
from tkinter import *

## VIEW

fenetre = Tk()
fenetre.title("TP2 - Calculatrice")
fenetre.resizable(0, 0)

# Buttons
button_7 = tkinter.Button(text = "7")
button_8 = tkinter.Button(text = "8")
button_9 = tkinter.Button(text = "9")
button_4 = tkinter.Button(text = "4")
button_5 = tkinter.Button(text = "5")
button_6 = tkinter.Button(text = "6")
button_1 = tkinter.Button(text = "1")
button_2 = tkinter.Button(text = "2")
button_3 = tkinter.Button(text = "3")
button_C = tkinter.Button(text = "C")
button_0 = tkinter.Button(text = "0")
button_AC = tkinter.Button(text = "AC")

button_sum = tkinter.Button(text = "+")
button_sub = tkinter.Button(text = "-")
button_mul = tkinter.Button(text = "*")
button_div = tkinter.Button(text = "/")

button_calc = tkinter.Button(text = "=")

button_7.grid(column = 0, row = 2)
button_8.grid(column = 1, row = 2)
button_9.grid(column = 2, row = 2)
button_4.grid(column = 0, row = 3)
button_5.grid(column = 1, row = 3)
button_6.grid(column = 2, row = 3)
button_1.grid(column = 0, row = 4)
button_2.grid(column = 1, row = 4)
button_3.grid(column = 2, row = 4)
button_C.grid(column = 3, row = 2)
button_0.grid(column = 1, row = 5)
button_AC.grid(column = 4, row = 2)

button_sum.grid(column = 5, row = 2)
button_sub.grid(column = 5, row = 3)
button_mul.grid(column = 5, row = 4)
button_div.grid(column = 5, row = 5)

button_calc.grid(column = 3, row = 5, columnspan = 2)

# Input and print
field_input = tkinter.Entry()
field_input.grid(column = 0, row = 0, columnspan = 6)
field_input.focus_set()

# Status bar
label_status = tkinter.Label(text="Calculatrice")
label_status.grid(column = 0, row = 6, columnspan = 6)

# Menus
menu_main = tkinter.Menu()
menu_help = tkinter.Menu()

menu_main.add_cascade(label = "Menu", menu = menu_help)

fenetre.config(menu = menu_main)

## EVENTS

# Buttons clicks
def button_7_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "7")
button_7.config(command = button_7_trigger)

def button_8_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "8")
button_8.config(command = button_8_trigger)

def button_9_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "9")
button_9.config(command = button_9_trigger)

def button_4_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "4")
button_4.config(command = button_4_trigger)

def button_5_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "5")
button_5.config(command = button_5_trigger)

def button_6_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "6")
button_6.config(command = button_6_trigger)

def button_1_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "1")
button_1.config(command = button_1_trigger)

def button_2_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "2")
button_2.config(command = button_2_trigger)

def button_3_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "3")
button_3.config(command = button_3_trigger)

def button_0_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "0")
button_0.config(command = button_0_trigger)

def button_sum_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "+")
button_sum.config(command = button_sum_trigger)

def button_sub_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "-")
button_sub.config(command = button_sub_trigger)

def button_mul_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "*")
button_mul.config(command = button_mul_trigger)

def button_div_trigger():
    global field_input
    field_input.insert(len(field_input.get()), "/")
button_div.config(command = button_div_trigger)

def button_C_trigger():
    global field_input
    field_input.delete(len(field_input.get()) - 1)
button_C.config(command = button_C_trigger)

def button_AC_trigger():
    global field_input
    field_input.delete(0, len(field_input.get()))
button_AC.config(command = button_AC_trigger)

def button_calc_trigger():
    global field_input
    try:
        result = str(eval(field_input.get(), {}))
        button_AC_trigger()
        field_input.insert(0, result)
        label_status.config(text = "Succès !")
    except:
        label_status.config(text = "Erreur !")
button_calc.config(command = button_calc_trigger)

def show_help():
    window_help = tkinter.Toplevel()
    label_help = tkinter.Label(window_help,
                               text="DI5.S9 : Python \n TP n°2 : Calculatrice \n Auteur : Valentin MAURICE")
    label_help.pack()
menu_help.add_command(label = "à propos", command = show_help)

# Key pressed
def key_pressed(evt):
    if evt.keysym == "Return":
        button_calc_trigger()
fenetre.bind("<Key>", key_pressed)

fenetre.mainloop()
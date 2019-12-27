def ChooseName():
    return input("Entrez un nom de fichier : ")

def AddText(file_name):
    try:
        with open(file_name, 'at') as file:
            text = input("Fichier ouvert, entrez le texte à ajouter : ")
            file.write(text + "\n")
    except:
        print("Erreur lors de l'ouverture du fichier")

def PrintFile(file_name):
    try:
        with open(file_name, 'rt') as file:
            print(file.read())
    except:
        print("Erreur lors de l'ouverture du fichier")

def EmptyFile(file_name):
    try:
        file = open(file_name, 'wt')
        file.close()
    except:
        print("Erreur lors de l'ouverture du fichier")

print("Hello World !")

menu = True
file = None
while menu:
    print("------------Menu------------")
    print("1. Choisir nom de fichier")
    print("2. Ajouter un texte")
    print("3. Afficher le fichier complet")
    print("4. Vider le fichier")
    print("9. Quitter le progrmme")

    try:
        choice = int(input("Choix : "))
    except ValueError:
        choice = 0

    if choice == 1:
        print("------------Choix de fichier------------")
        file = ChooseName()
    elif choice == 2:
        print("------------Ajout de texte------------")
        AddText(file)
    elif choice == 3:
        print("------------Affichage de fichier------------")
        PrintFile(file)
    elif choice == 4:
        print("------------Vider le fichier------------")
        EmptyFile(file)
    elif choice == 9:
        menu = 0
        print("------------Quitter le programme------------")
    else :
        print("Choix invalide")
        print("")



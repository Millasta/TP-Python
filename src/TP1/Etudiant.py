from datetime import date
from src.TP1.Date import Date

class Student:
    def __init__(self, first_name, last_name, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def age(self):
        age = date.today().year - self.birth_date.year
        if date.today().month < self.birth_date.month:
            age -= 1
        return age

    def mail(self):
        return self.first_name + "." + self.last_name + "@etu.univ-tours.fr"


birth_date = Date()
birth_date.day = 5
birth_date.month = 3
birth_date.year = 1997

etu = Student("Jean", "RACINE", birth_date)
print("Age : ", etu.age())

# Reading fichetu.csv
students = []
file_name = "fichetu.csv"
try:
    with open(file_name, 'rt') as file:
        for line in file:
            splitted  = line.split(';')
            splitted_date = splitted[2].split('/')

            birth = Date()
            birth.day = int(splitted_date[0])
            birth.month = int(splitted_date[1])
            birth.year = int(splitted_date[2])

            student = Student(splitted[0], splitted[1], birth)
            print("Etudiant : ", student.first_name, " ", student.last_name, " ", student.birth_date, " ", student.mail(), " ", student.age())
            students.append(student)
        print("Nombre d'étudiants : ", len(students))
except:
    print("Erreur : erreur lors de l'ouverture du fichier")
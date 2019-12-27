class Date:
    def __init__(self):
        self.year = 2000
        self.month = 1
        self.day = 1

    def __str__(self):
        return str(self.day) + '/' \
            + str(self.month) + '/' \
            + str(self.year)

    def __eq__(self, other):
        if not other.__class__ is Date:
            print("Erreur: l'argument n'est pas une date")
            return NotImplemented
        if self.day == other.day and self.month == other.month and self.year == other.year:
            return True
        return False

    def __lt__(self, other):
        if not other.__class__ is Date:
            print("Erreur: l'argument n'est pas une date")
            return NotImplemented
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day < other.day:
                    return True
        return False

date_1 = Date()
date_2 = Date()
date_2.day = 12
date_2.month = 2

print(date_1, " < ", date_2, " : ", (date_1<date_2))
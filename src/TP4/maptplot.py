from random import *
import matplotlib.pyplot as plt
plt.style.use('seaborn')

size = 100
random_range1 = 20
randoms1 = []
random_range2 = 10
randoms2 = []

# Génération
for i in range(size):
    randoms1.append(randrange(random_range1))
    randoms2.append(randrange(random_range2))

# Données
plt.plot(randoms1[:100], color="red", label="rouge", ls=":")
plt.plot(randoms2[:100], color="blue", label="bleu")

# Style
print(plt.style.available)

plt.axis([0, 100,-4, 21])
plt.legend(loc='lower left');
axes = plt.axes()
arrow = axes.arrow(5, 20, 15, -5, head_width=0.5, head_length=1)
axes = axes.set(xlabel='Nombres générés', ylabel='Valeur')
plt.title("Graphe")

# Affichage
plt.show()

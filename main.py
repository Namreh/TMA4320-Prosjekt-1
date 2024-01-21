#importerer bibliotek
import numpy as np
import matplotlib.pyplot as plt

##oppgave 1a-1b

#funksjon for å konstruere rett, horisontal polymer
def initalPolymer(N):
    polymer = np.zeros((N, 2))
    for i in range(1, N):
        polymer[i][0] = i
    return polymer

print(initalPolymer(5))

#oppgave 1d
#funksjon for å illustrere polymer
def showPolymer(polymer):
    N = len(polymer)

    #lager en tom matrise
    image = np.zeros((N+2,N+2))
    for i in range(N):
        x, y = int(polymer[i][0]), int(polymer[i][1])
        image[y+(N+2)//2][x+1] = i+1

    #plot
    fig, ax = plt.subplots()
    cmap = plt.get_cmap("Greens")
    cmap.set_under('mistyrose')
    ax.imshow(image, cmap=cmap, vmin=1)
    ax.set_title(f"Polymer, bestående av N={N} monomerer")
    plt.show()

showPolymer(initalPolymer(10))

testPolymer = [[0,0],[2,2],[2,3]]

#1e – funksjon for validitet
def validPolymer(polymer, N):

    #med vår metode for lagring av polymer, vet vi at det alltid er N monomerer, og at de representeres unikt av indeksene, med mindre det er to monomerer på samme plass

    #sjekke at ingen overlapper
    if len(polymer) != len(np.unique(polymer)):
        return False
    
    #sjekke nærmeste nabo
    for i in range(0, N-1):
        mon = polymer[i]
        nextMon = polymer[i+1]

        dX = np.abs(mon[0]-nextMon[0])
        dY = np.abs(mon[1]-nextMon[1])

        if dX+dY != 1:
            return False

    return True

print(validPolymer(testPolymer, 3))
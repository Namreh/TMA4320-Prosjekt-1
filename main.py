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
    cmap.set_under('lightgrey')
    ax.imshow(image, cmap=cmap, vmin=1)
    ax.set_title(f"Polymer, bestående av N={N} monomerer")
    plt.show()

showPolymer(initalPolymer(10))
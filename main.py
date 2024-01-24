#importerer bibliotek
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants as sp #for konstanter

#regne ut beta for boltzmannstatistikken
def beta(T):
    return 1/(sp.k*T)

##oppgave 1a-1b

#funksjon for å konstruere rett, horisontal polymer
def initalPolymer(N):
    polymer = np.zeros((N, 2))
    for i in range(1, N):
        polymer[i][0] = i
    return polymer


#oppgave 1d
#funksjon for å illustrere polymer
def showPolymer(polymer):
    N = len(polymer)

    #lager en tom matrise
    image = np.zeros((N+2,N+2))
    #fyller inn matrisen med polymeren, index er verdien
    for i in range(N):
        x, y = int(polymer[i][0]), int(polymer[i][1])
        image[y+(N+2)//2][x+1] = i+1

    #Fjerner de ytterste kolonnene og radene som kun består av 0.0, og legger til en ekstra kant av 0.0
    non_zero_rows = np.any(image != 0, axis=1)
    non_zero_columns = np.any(image != 0, axis=0)
    trimmed_image = image[non_zero_rows][:, non_zero_columns]
    padded_image = np.pad(trimmed_image, pad_width=1, mode='constant', constant_values=0.0)


    #plot av polymeren
    fig, ax = plt.subplots()
    cmap = plt.get_cmap("Greens")
    cmap.set_under('mistyrose')
    figur = ax.imshow(padded_image, cmap=cmap, vmin=1, origin='lower', resample=True)    
    ax.set_title(f"Polymer, bestående av N={N} monomerer")
    fig.colorbar(figur)
    plt.show()


#1e – funksjon for validitet
def validPolymer(polymer, N):

    #med vår metode for lagring av polymer, vet vi at det alltid er N monomerer, og at de representeres unikt av indeksene, med mindre det er to monomerer på samme plass

    #sjekke at ingen overlapper
    if len(polymer) != len(np.unique(polymer, axis=0)):
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


#1f – rotasjonsfunksjon
def rotatePolymer(polymer, coordinate, rotation):
    N = len(polymer)

    #definerer rotasjonsmatrisen ifht rotation
    rotMatrix = np.array([[0,-1], [1,0]]) if rotation else np.array([[0,1], [-1,0]])

    #finner indeksen til monomeren som skal roteres
    rotIndex = np.where(np.all(polymer==np.array(coordinate), axis=1))
    if len(rotIndex)>0:
        rotIndex = rotIndex[0][0]
    else:
        print("NO POLYMER IN GIVEN COORDINATE")
        

    #deler polymeren i to
    rightPolymer = np.copy(polymer[rotIndex:])
    leftPolymer = np.copy(polymer[:rotIndex])

    #bestemmer hvilken side som er kortest
    if rotIndex+1<N/2:
        #roterer 
        leftPolymer -= coordinate
        leftPolymer = leftPolymer@rotMatrix + coordinate
    else:
        rightPolymer -= coordinate
        rightPolymer = rightPolymer@rotMatrix + coordinate

    return np.concatenate((leftPolymer, rightPolymer))


#1g – funksjon for å rotere en polymer
def randomRotationSimulation(N, N_s):
    counter = 1
    tempPolymer = initalPolymer(N)
    for i in range(N_s):
        randIndex = np.random.randint(1,N-1) #inkluderer her ikke endemonomerer
        rotation = np.random.randint(0,2) #gir boolsk variabel
        newPolymer = rotatePolymer(np.copy(tempPolymer), tempPolymer[randIndex], rotation)
        if validPolymer(newPolymer, N):
            counter += 1
            tempPolymer = newPolymer
    return tempPolymer, counter

# MANGLER LAGRING OG SAMMENLIGNING AV TO POLYMERER
t, c = randomRotationSimulation(5, 100)

#showPolymer(t)

#oppgave 1j – funksjon for å beregne energien i polymer
def polymerEnergy(polymer, V):
    xi, yi = polymer.T #deler opp polymeren i x og y

    dx = np.abs(xi-xi[:, np.newaxis])
    dy = np.abs(yi-yi[:, np.newaxis])

    #lager masken som viser til naboer
    mask = ((dx == 1) & (dy == 0)) | ((dx == 0) & (dy == 1))

    #fjerner ikke-naboer fra V-matrisen – antar at linkede monomerer har 0 i energi i V
    vvMatrix = V[mask] 

    #summerer den gjenværende energien, deler på 2 ifht energiformel
    return 0.5*np.sum(vvMatrix)
    

#funksjon for å lage standard V array av vilkårlig størrelse
def createVarray(N, value):
    tempV = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if not ((i == j) or np.abs((i-j)) == 1):
                tempV[i,j] = value

    return tempV

#oppgave 2a) Metropolisalgoritme, algoritme 2
def metropolisSimulation(polymer, N_s, V, T):
    N = len(polymer)
    tempPolymer = np.copy(polymer)

    E_array = np.zeros(N_s)
    E = polymerEnergy(polymer, V)
    E_array[0] = E
    i = 1
    while i < N_s:
        randIndex = np.random.randint(1,N-1) #inkluderer her ikke endemonomerer
        rotation = np.random.randint(0,2) #gir boolsk variabel
        newPolymer = rotatePolymer(np.copy(tempPolymer), tempPolymer[randIndex], rotation)

        if validPolymer(newPolymer, N):
            i += 1
            E_new = polymerEnergy(newPolymer, V)
            if E_new < E:
                tempPolymer = newPolymer
                E = E_new
            elif np.random.uniform() < np.exp(-beta(T)*(E_new-E)):
                tempPolymer = newPolymer
                E = E_new
            E_array[i-1] = E

    return tempPolymer, E_array

#kode for å kjøre metrolpolis simulering
#metropoly, energy_array = metropolisSimulation(initalPolymer(100), 5000, createVarray(100, -4.0*10**(-21)), 1000)

#funksjon for å finne forventingsverdi
def expectationValue(dataset, start):
    return np.mean(dataset[start:])

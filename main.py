#importerer bibliotek
import numpy as np
import matplotlib.pyplot as plt

##oppgave 1a-1b

#funksjon for å konstruere rett, horisontal polymer
def initalPolymer(N):
    polymer = np.zeros((N, 2))
    for i in range(N):
        polymer[i][0] = i
    return polymer

print(initalPolymer(5))
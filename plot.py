import main as m
import numpy as np
import matplotlib.pyplot as plt

#Oppgave 1i – prosentandel gyldige rotasjoner som funksjon av N
def allowedRotOfN(N_s, start, stop):
    points = 100
    N_vals = np.linspace(start,stop, points)
    percent_values = np.zeros(points)
    for i in range(points):
        _, c = m.randomRotationSimulation(int(N_vals[i]), N_s)
        percent_values[i] = c/N_s
    plt.plot(N_vals, percent_values)
    plt.show()

#kjør denne for å vise oppg 1i
#allowedRotOfN(1000, 10, 1000)
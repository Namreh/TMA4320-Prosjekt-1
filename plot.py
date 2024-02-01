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
#allowedRotOfN(100, 10, 1000)
    
#Oppgave 2e
def oppgave2E():
    N = 30
    N_s = 5000
    t_array = np.arange(10,1000, 30)
    length = len(t_array)
    e_array = np.zeros(length)
    deviation_array = np.zeros(length)

    for i in range(length):
        _, energy_array = m.metropolisSimulation(m.initalPolymer(N), N_s, m.createVarray(N, -4.0*10**(-21)), t_array[i])
        e_array[i] = np.mean(energy_array[1000:])
        deviation_array[i] = np.std(energy_array[1000:])
    
    fig, ax = plt.subplots()
    ax.errorbar(t_array, e_array, yerr=deviation_array)
    plt.show()

#oppgave 2g – plotteoppgave, diameter
def oppgave2g():
    N = 30
    N_s = 5000
    t_array = np.arange(10,1000, 30)
    length = len(t_array)
    e_array = np.zeros(length)
    deviation_array = np.zeros(length)

    #lager tilfeldig v_array
    V_array = m.createRandomVarray(N, -6*10**-21, -2*10**-21)

    for i in range(length):
        _, energy_array = m.metropolisSimulation(m.initalPolymer(N), N_s, V_array, t_array[i])
        e_array[i] = np.mean(energy_array[1000:])
        deviation_array[i] = np.std(energy_array[1000:])
    
    fig, ax = plt.subplots()
    ax.errorbar(t_array, e_array, yerr=deviation_array)
    plt.show()
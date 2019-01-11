from multiprocessing import Process, Lock, Queue
import queue
import time
from os import getpid


COEF_TEMP = 0.2
COEF_SUN = 0.1
COEF_WIND = 0.08
SELL = 0
GIVE = 1
TRYGIVE = 2
TIMEOUT = 100


class DispoEnergy:
    def __init__(self, source, amount):
        self.source = source
        self.amount = amount


def Homes(weather, chan):
    N = 10 # NOMBRE DE MAISONS
    lock = Lock()
    global wind
    global sun
    global temp
    global energy
    energy = 0.0
    wind = weather[0]
    sun = weather[1]
    temp = weather[2]
    q = Queue()

    q = queue.Queue()
    home = list()
    for i in range(N):
        home.append(Process(target=Home, args=(lock, q)))
    for p in home:
        p.start()
    for p in home:
        p.join()


def Home(lock, q, time=60, politic=SELL,  c_initial=200, p_initial=100):
    while True:
        global energy
        energy_politic = 1  # ou 2 ou 3, dépend de s'il veut donner
        energy_propre = - time*(c_initial + temp*COEF_TEMP) #conso
        energy_propre += time*(p_initial + wind*COEF_WIND + sun*COEF_SUN) #prod
        if politic != SELL and energy_propre > 0:
            g = DispoEnergy(getpid(), energy_propre)
            q.put(g, timeout=TIMEOUT)
        with lock:
            energy += energy_propre

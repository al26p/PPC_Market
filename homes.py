import random
from multiprocessing import Process, Lock, Queue, Value
import queue
import time as ptime
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


def homes(weather):
    N = 10 # NOMBRE DE MAISONS
    lock = Lock()
    energy = Value('f')
    energy.value = 0
    hom = list()
    for i in range(N):
        c = random.randrange(0, 2000)
        p = random.randrange(0, 2000)
        hom.append(Process(target=home, args=(lock, energy, weather, c, p)))
    hom.append(Process(target=show, args=(5, energy)))
    for p in hom:
        p.start()
    print('Homes started')
    for p in hom:
        p.join()
    ptime.sleep(1)
    print('See ya !')


def show(ttl, nrj):
    while True:
        print('Global energy', nrj.value)
        ptime.sleep(ttl)


# begin with capitalism
def home(lock, energy, weather, c_initial=200, p_initial=100, time=60, politic=SELL):
    while True:
        try:
            ptime.sleep(2)
            energy_propre = - time*(c_initial + 1/weather[0]*COEF_TEMP) #conso
            energy_propre += time*(p_initial + weather[2]*COEF_WIND + weather[1]*COEF_SUN) #prod
            print('energy home', getpid(), energy_propre, 'meteo', weather[0])
            with lock:
                energy.value += energy_propre
        except KeyboardInterrupt:
            break
    print("end of home", getpid())


if __name__=='__main__':
    try:
        homes([1, 2, 10])
    except KeyboardInterrupt:
        print('exitting')
        ptime.sleep(2)

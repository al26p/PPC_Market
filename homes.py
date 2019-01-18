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

def Homes(weather):
    N = 10 # NOMBRE DE MAISONS
    lock = Lock()
    global wind
    global sun
    global temp
    energy = 0.0
    wind = weather[0]
    sun = weather[1]
    temp = weather[2]

    home = list()
    for i in range(N):
        home.append(Process(target=Home, args=(lock,)))
    for p in home:
        p.start()
    print('Homes started')
    for p in home:
        p.join()
    print('See ya !')

# begin with capitalism
def Home(lock, time=60, politic=SELL,  c_initial=200, p_initial=100):
    while True:
        try:
            ptime.sleep(2)
            global energy
            energy_politic = 1
            energy_propre = - time*(c_initial + temp*COEF_TEMP) #conso
            energy_propre += time*(p_initial + wind*COEF_WIND + sun*COEF_SUN) #prod
            print('energy home', getpid(), energy_propre)
            with lock:
                energy += energy_propre
                print('energy global', energy)
        except KeyboardInterrupt:
            break
    print("end of home", getpid())


if __name__=='__main__':
    try:
        Homes([1,2,10])
    except KeyboardInterrupt:
        print('exitting')
        ptime.sleep(2)

import random
from multiprocessing import Process, Lock, Queue, Value
import queue
import time as ptime
from os import getpid
import sysv_ipc

COEF_TEMP = 0.2
COEF_SUN = 0.1
COEF_WIND = 0.08
SELL = 0
GIVE = 1
TRYGIVE = 2
TIMEOUT = 1


class DispoEnergy:
    def __init__(self, amount, time_expire, sender):
        self.amount = amount
        self.timeout = time_expire
        self.sender = sender


def homes(weather):
    N = 10  # NOMBRE DE MAISONS
    lock = Lock()
    energy = Value('f')
    energy.value = 0
    hom = list()
    for i in range(N):
        c = random.randrange(0, 2000)
        p = random.randrange(0, 2000)
        pol = SELL
        hom.append(Process(target=home, args=(lock, energy, weather, c, p, pol)))
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
    energy_propre = 0
    while True:
        try:
            ptime.sleep(time)
            energy_propre += - time * (c_initial + 1 / weather[0] * COEF_TEMP)  # conso
            energy_propre += time * (p_initial + weather[2] * COEF_WIND + weather[1] * COEF_SUN)  # prod
            print('energy home', getpid(), energy_propre, 'meteo', weather[0])
            with lock:
                energy.value += energy_propre
            energy_propre = request(politic, energy_propre)
        except KeyboardInterrupt:
            break
    print("end of home", getpid())


def request(politic, nrj):
    if nrj > 0:  # selling nrj
        if politic == 1:
            # Proposer NRJ dans queue 2, t fini mais pas bloquant, si t infini : on suppose qu'on stocke
            try:
                send = sysv_ipc.MessageQueue(2, flag=sysv_ipc.IPC_CREAT)
            except sysv_ipc.ExistentialError:
                send = sysv_ipc.MessageQueue(2)
            send.send(DispoEnergy(nrj, ptime.time() + TIMEOUT, getpid()))
        if politic == 2:
            # Proposer NRJ dans queue 2, t fini mais bloquant, on attends une réponse dans la queue 3. si pas de réponse, sell
            try:
                send = sysv_ipc.MessageQueue(2, sysv_ipc.IPC_CREAT)
            except sysv_ipc.ExistentialError:
                send = sysv_ipc.MessageQueue(2)
            timeout = ptime.time() + TIMEOUT
            send.send(DispoEnergy(nrj, timeout, getpid()))
            r = DispoEnergy(0, timeout, getpid())
            while True:
                try:
                    rcv = sysv_ipc.MessageQueue(3, sysv_ipc.IPC_CREAT)
                except sysv_ipc.ExistentialError:
                    rcv = sysv_ipc.MessageQueue(3)
                while True:
                    try:
                        (r, _) = rcv.receive([False, [getpid()]])
                        nrj = r.amount
                    except sysv_ipc.BusyError:
                        # ptime.sleep(0.01)
                        pass
                    if ptime.time() > timeout:
                        break
                if ptime.time() > timeout:
                    break
                if r.amount != 0:
                    nrj = r.amount
                    send.send(r)
                else:
                    break
            to_market(getpid(), nrj)
        if politic == 0:
            # requeste au marché : queue 1
            to_market(getpid(), nrj)

    if nrj < 0:  # buying
        nrj = abs(nrj)
        try:
            rcv = sysv_ipc.MessageQueue(2, sysv_ipc.IPC_CREAT)
        except sysv_ipc.ExistentialError:
            rcv = sysv_ipc.MessageQueue(2)
        while True:
            try:
                (r, _) = rcv.receive([False, ])
                try:
                    send = sysv_ipc.MessageQueue(3, sysv_ipc.IPC_CREAT)
                except sysv_ipc.ExistentialError:
                    send = sysv_ipc.MessageQueue(3)
                if nrj < r.amount:
                    r.amount = r.amount - nrj
                    nrj = 0
                if nrj > r.amount:
                    nrj = nrj - r.amount
                    r.amount = 0
                    send.send(r, [True, [r.sender]])
            except sysv_ipc.BusyError:
                print('no vendors')
                break
        to_market(getpid(), - nrj)

    return 0


def to_market(pid, nrj):
    # NRJ to send/request to the market
    if nrj < 0:
        neg = 'buying'
    else:
        neg = 'selling'
    print(pid, "resquest to market", nrj, neg)


if __name__ == '__main__':
    try:
        homes([1, 2, 10])
    except KeyboardInterrupt:
        print('exitting')
        ptime.sleep(2)

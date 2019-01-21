import random
from multiprocessing import Process, Lock, Queue, Value, Semaphore
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
TIMEOUT = 10


class DispoEnergy:
    def __init__(self, amount, time_expire, sender):
        self.amount = amount
        self.timeout = time_expire
        self.sender = sender

    def serialize(self):
        return (str(self.amount) + ',' + str(self.timeout) + ',' + str(self.sender)).encode('UTF-8')

    def deserialize(self, serialized):
        serialized = serialized.decode('UTF-8')
        s = serialized.split(',')
        self.amount = float(s[0])
        self.timeout = float(s[1])
        self.sender = int(s[2])


def homes(weather, queue, sem):
    N = 10  # NOMBRE DE MAISONS
    lock = Lock()
    energy = Value('f')
    energy.value = 0
    hom = list()
    for i in range(N):
        c = random.randrange(100, 500)
        p = random.randrange(50, 450)
        pol = GIVE
        hom.append(Process(target=home, args=(lock, energy, weather, sem, queue, c, p, 2, pol)))
    hom.append(Process(target=show, args=(5, energy)))
    for p in hom:
        p.start()
    print('Homes started')
    for p in hom:
        p.join()
    ptime.sleep(1)
    sysv_ipc.MessageQueue(2).remove()
    sysv_ipc.MessageQueue(3).remove()
    print('See ya !')


def show(ttl, nrj):
    while True:
        print('Global energy', nrj.value)
        ptime.sleep(ttl)


# begin with capitalism
def home(lock, energy, weather, sem, queue, c_initial=200, p_initial=100, time=60, politic=SELL):
    energy_propre = 0
    while True:
        try:
            ptime.sleep(time)
            energy_propre += - time * (c_initial + 1 / weather[0] * COEF_TEMP)  # conso
            energy_propre += time * (p_initial + weather[2] * COEF_WIND + weather[1] * COEF_SUN)  # prod
            print('energy home', getpid(), energy_propre, 'meteo', weather[0])
            with lock:
                energy.value += energy_propre
            energy_propre = request(politic, energy_propre, sem, queue)
        except KeyboardInterrupt:
            break
    print("end of home", getpid())


def request(politic, nrj, sem, queue):
    if nrj > 0:  # selling nrj
        if politic == 1:
            # Proposer NRJ dans queue 2, t fini mais pas bloquant, si t infini : on suppose qu'on stocke
            try:
                send = sysv_ipc.MessageQueue(2, flags=sysv_ipc.IPC_CREAT)
            except sysv_ipc.ExistentialError:
                send = sysv_ipc.MessageQueue(2)
            send.send(DispoEnergy(nrj, ptime.time() + TIMEOUT, getpid()).serialize())
            print(getpid(), 'shares', nrj, 'for (s)', TIMEOUT)
        if politic == 2:
            # Proposer NRJ dans queue 2, t fini mais bloquant, on attends une réponse dans la queue 3. si pas de réponse, sell
            try:
                send = sysv_ipc.MessageQueue(2, flags=sysv_ipc.IPC_CREAT)
            except sysv_ipc.ExistentialError:
                send = sysv_ipc.MessageQueue(2)
            timeout = ptime.time() + TIMEOUT
            send.send(DispoEnergy(nrj, timeout, getpid()).serialize())
            r = DispoEnergy(0, timeout, getpid())
            while True:
                try:
                    rcv = sysv_ipc.MessageQueue(3, flags=sysv_ipc.IPC_CREAT)
                except sysv_ipc.ExistentialError:
                    rcv = sysv_ipc.MessageQueue(3)
                while True:
                    try:
                        (s, _) = rcv.receive(block=False, type=getpid())
                        r.deserialize(s)
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
                    send.send(r.serialize())
                else:
                    break
            to_market(getpid(), nrj, sem, queue)
        if politic == 0:
            # requeste au marché : queue 1
            to_market(getpid(), nrj, sem, queue)

    if nrj < 0:  # buying
        nrj = abs(nrj)
        r = DispoEnergy(0,0,0)
        try:
            rcv = sysv_ipc.MessageQueue(2, flags=sysv_ipc.IPC_CREAT)
        except sysv_ipc.ExistentialError:
            rcv = sysv_ipc.MessageQueue(2)
        while True:
            print('searching')
            try:
                (s, _) = rcv.receive(block=False)
                print(getpid(),'found',s.decode('UTF-8'))
                r.deserialize(s)
                try:
                    send = sysv_ipc.MessageQueue(3, flags=sysv_ipc.IPC_CREAT)
                except sysv_ipc.ExistentialError:
                    send = sysv_ipc.MessageQueue(3)
                if nrj < r.amount:
                    r.amount = r.amount - nrj
                    nrj = 0
                if nrj > r.amount:
                    nrj = nrj - r.amount
                    r.amount = 0
                    send.send(r.serialize(), block=True, type=r.sender)
            except sysv_ipc.BusyError:
                print('no vendors')
                break
        to_market(getpid(), - nrj, sem, queue)

    return 0


def to_market(pid, nrj, sem, queue):
    sem.acquire()
    print(getpid(), 'aquired sem')
    if nrj == 0:
        return
    # NRJ to send/request to the market
    if nrj < 0:
        neg = 'buying'
    else:
        neg = 'selling'

    nrj = str(round(nrj, 2))
    print(pid, "resquest to market", nrj, neg)
    queue.put(nrj)


if __name__ == '__main__':
    try:
        homes([1, 2, 10])
    except KeyboardInterrupt:
        print('exitting')
        ptime.sleep(2)

from time import sleep
from os import getpid
import multiprocessing
import threading
import signal
import sysv_ipc
import external

Y = 0.99  # long term attenuation coef
S = 1000  # 1 over the coef of the impact of the homes selling energy to the market
B = 1000  # 1 over the coef of the impact of the market selling energy to the homes
EXT_CTE1 = 0.5
EXT_CTE2 = 1
TIME = 60

# average price of kW/h in France in centimes of € is 14.69c
prix_prec = 14.69
prix_actuel = 14.69

# average energy consumption should be around 300 kW/h per house per month (per house per message)
energy_sell = 0  # energy : home -> market
energy_bought = 0  # energy : market -> home
energy_mutex = threading.Lock()

external_value1 = 0
external_value2 = 0
external1 = False
external2 = False
external_mutex = threading.Lock()  # to protect the variable upside this line


class Market(multiprocessing.Process):
    def __init__(self, semaphore, time=5):
        super().__init__()
        global TIME
        TIME = time
        self.queue_semaphore = semaphore
        try:
            self.energy_queue = sysv_ipc.MessageQueue(1, flags=sysv_ipc.IPC_CREAT)
        except sysv_ipc.ExistentialError:
            self.energy_queue = sysv_ipc.MessageQueue(1)



    def run(self):
        signal.signal(signal.SIGUSR1, handler)
        signal.signal(signal.SIGUSR2, handler)
        external_process = external.External(1, getpid())
        energy_thread = threading.Thread(target=gettingEnergy, args=(self.energy_queue, self.queue_semaphore,));
        price_thread = threading.Thread(target=CalculatingPrice)

        energy_thread.start()
        price_thread.start()
        external_process.start()

        energy_thread.join()
        price_thread.join()
        external_process.join()

    def __del__(self):
        self.energy_queue.remove()
        print('queue cleaned')


def gettingEnergy(energy_queue, queue_semaphore):
    print ('Geting energy')
    global energy_mutex
    global energy_bought
    global energy_sell

    while True:
        (value,_) = energy_queue.receive(type=1)
        queue_semaphore.release()
        print ('energy receive '+value.decode())
        value = float(value.decode())
        with energy_mutex:

            if 0 > value:
                energy_bought += -value
            else:
                energy_sell += -value


def CalculatingPrice():
    print('CalculatingPrice')
    global EXT_CTE1
    global EXT_CTE2
    global TIME

    global external1
    global external2
    global external_value1
    global external_value2
    global external_mutex

    global prix_prec
    global prix_actuel

    global energy_bought
    global energy_sell
    global energy_mutex

    while True:
            if external1:()
                external_value1 += EXT_CTE1
            else:
                external_value1 = 0

            if external2:
                external_value2 += EXT_CTE2
            else:
                external_value2 = 0

        with energy_mutex:
            prix_prec = prix_actuel
            prix_actuel = Y * prix_prec + energy_sell/S + energy_bought/B + external_value1 + external_value2
            energy_sell = 0
            energy_bought = 0
        print('Market Price :', prix_actuel)


def handler(sig, frame):
    global external1
    global external2

    if sig == signal.SIGUSR1:
        if (not external1):
            print('wow ! Exceptional crisis 1')
            external1 = True
        else:
            print('End of the Exceptional crisis 1')
            external1 = False

    if sig == signal.SIGUSR2:
        if (not external2):
            print('wow ! Exceptional crisis 2')
            with external_mutex:
                external2 = True
        else:
            print('End of the Exceptional crisis 2')
            with external_mutex:
                external2 = False

if __name__ == '__main__':
    if __name__ == "__main__":
        queue_semaphore=multiprocessing.Semaphore(8)
        p = Market(queue_semaphore)
        p.start()
        print ('l.134')
        try:
            energy_queue = sysv_ipc.MessageQueue(1, flags=sysv_ipc.IPC_CREAT)
        except sysv_ipc.ExistentialError:
            energy_queue = sysv_ipc.MessageQueue(1)
        sleep(15)
        queue_semaphore.acquire()
        energy_queue.send("350".encode())
        sleep(5)
        queue_semaphore.acquire()
        energy_queue.send("2500".encode())
        sleep(5)
        queue_semaphore.acquire()
        energy_queue.send("-250".encode())
        p.join()
        print('l.136, end')

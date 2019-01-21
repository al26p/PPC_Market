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
    def __init__(self, queue, time=5, running):
        super().__init__()
        global TIME
        TIME = time
        self.queue = queue
        self.running = running

    def run(self):
        signal.signal(signal.SIGUSR1, handler)
        signal.signal(signal.SIGUSR2, handler)
        external_process = external.External(1, getpid())
        energy_thread = threading.Thread(target=gettingEnergy, args=(self.queue,self.running,))
        price_thread = threading.Thread(target=CalculatingPrice, args=(self.running,))

        energy_thread.start()
        price_thread.start()
        external_process.start()

        energy_thread.join()
        price_thread.join()
        external_process.join()

def gettingEnergy(queue, running):
    print('Geting energy')
    global energy_mutex
    global energy_bought
    global energy_sell
    global fichier
    while running:
        value = queue.get()
        print('\t energy receive ' + value + "\n")
        value = float(value)
        with energy_mutex:

            if 0 > value:
                energy_bought += -value
            else:
                energy_sell += -value


def CalculatingPrice(running):
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

    global fichier
    with open('prices.json', 'w') as wfile:
        wfile.write('{\"prices\":[')
    while running:
        if external1:
            external_value1 += EXT_CTE1
        else:
            external_value1 = 0

        if external2:
            external_value2 += EXT_CTE2
        else:
            external_value2 = 0

        with energy_mutex:
            prix_prec = prix_actuel
            prix_actuel = Y * prix_prec + energy_sell / S + energy_bought / B + external_value1 + external_value2
            energy_sell = 0
            energy_bought = 0
            if prix_actuel < 0:
                prix_actuel = 0
        print('Market Price :', str(prix_actuel) + "\n")
        with open('prices.json', 'a') as wfile:
            wfile.write(str(prix_actuel)+',')
        sleep(TIME)


def handler(sig, frame):
    global external1
    global external2
    global fichier

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
    energy_queue = multiprocessing.Queue(8)
    p = Market(energy_queue)
    p.start()
    print('l.134')
    sleep(15)
    energy_queue.put("350")
    sleep(5)
    energy_queue.put("2500")
    sleep(5)
    energy_queue.put("-250")
    p.join()
    print('l.136, end')

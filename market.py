from time import sleep
import multiprocessing
import threading
import signal
import sysv_ipc

Y = 0.99 #long term attenuation coef
S = -1000 #1 over the coef of the impact of the homes selling energy to the market
B = 1000 #1 over the coef of the impact of the market selling energy to the homes
EXT_CTE1 = 0.5
EXT_CTE2 = 1

#average price of kW/h in France in centimes of € is 14.69c
prix_prec = 14.69
prix_actuel = 14.69

# average energy consumption should be around 300 kW/h per house per month (per house per message)
energy_sell = 0 #energy : home -> market
energy_bought = 0 #energy : market -> home
energy_mutex = threading.Lock()

external_value1 =0
external_value2 =0
external1 = False
external2 = False
external_mutex = threading.Lock() #to protect the variable upside this line

time

class Market (Process):
    def __init__(self, the_key, queue_semaphore, time=60):
        super().__init__()
        signal.signal(signal.SIGUSR1, handler)
        signal.signal(signal.SIGUSR2, handler)
        global time = time
        energy_queue = sysv_ipc.MessageQueue(key)
    def run(self):
        energy_thread = threading.Thread(target=gettingEnergy, args=(energy_queue, queue_semaphore,));
        price_thread = threading.Thread(target=CalculatingPrice)

def gettingEnergy() :
    global energy_mutex
    global energy_bought
    global energy_sell

    while True :
        value = mq.receive(type=1)
        queue_semaphore.release()
        value = float(value.decode())
        with energy_mutex :
            if 0 > value :
                energy_bought += value
            else :
                energy_sell += value


def CalculatingPrice () :
    global EXT_CTE1
    global EXT_CTE2
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

    while True :
        sleep(time) # we re-calculate the price each "x" milisecond where x is Time and it's an hard-coded constant
        # check if exceptionnal event
        with  external_mutex:
            if external1 :
                external_value1 += EXT_CTE1
            else :
                external_value1 = 0

            if external2 :
                external_value2 += EXT_CTE2
            else :
                external_value2 = 0

        with energy_mutex:
            prix_prec = prix_actuel
            prix_actuel = Y*prix_prec + energy_sell/S + energy_bought/B + external_value1 + external_value2 #where y s and b are hard-coded constant factor
            external = 0
        print('Market Price :', prix_actuel)



def handler(sig, frame) :
    global external1
    global external2

    if sig == signal.SIGUSR1:
        if (!external1):
            print('wow ! Exceptional crisis 1')
            external1 = True
        else :
            print('End of the Exceptional crisis 1')
            external1 = False

    if sig == signal.SIGUSR2:
        if (!external2):
            print('wow ! Exceptional crisis 2')
            with external_mutex :
                external2 = True
        else :
            print('End of the Exceptional crisis 2')
            with external_mutex :
                external2 = False

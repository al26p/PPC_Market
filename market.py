# all of this need to be global variable
from time import sleep
from threading import Lock
import signal

Y = 0.1
S = 0.1
B = 0.1

energy_bought = 0
external = 0 #value in $ of the influence of the external factor on the energy price

prix_prec = 0
prix_actuel = 0
energy_mutex = Lock()

external1 = False
external2 = False
external_mutex = Lock() #to protect the variable upside this line
time = 60

'''
signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGUSR2, handler)
'''

def CalculatingPrice () :
    global external1
    global external2
    global external
    global PrixPrec
    global PrixActuel
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    while True :
        sleep(time) # we re-calculate the price each "x" milisecond where x is Time and it's an hard-coded constant
        # check if exceptionnal event
        with  external_mutex:
            if external1 :
                external += cte
                external1 = False
            if external2 :
                external += cte
                external2 = False

        with energy_mutex:
            PrixPrec = PrixActuel
            PrixActuel = Y * PrixPrec + S * energySell + B * energyBought + external #where y s and b are hard-coded constant factor
            external = 0
        print('Market Price :', PrixActuel)



def handler(sig, frame) :
    global external1
    global external2

    if sig == signal.SIGUSR1:
        print('wow ! Exceptional crisis 1')
        with external_mutex :
            external1 = True

    if sig == signal.SIGUSR2:
        print('wow ! Exceptional crisis 2')
        with external_mutex :
            external2 = True

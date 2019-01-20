from time import sleep
from threading import Lock
import signal

Y = 0.99 #long term attenuation coef
S = 0.001 #coef of the impact of the homes selling energy to the market
B = 0.01 #coef of the impact of the market selling energy to the homes

energy_bought = 0
external = 0 #value in $ of the influence of the external factor on the energy price

prix_prec = 0
prix_actuel = 0.145
energy_mutex = Lock()

external1 = False
external2 = False
external_mutex = Lock() #to protect the variable upside this line
time = 60

def CalculatingPrice () :
    global external1
    global external2
    global external_value1
    global external_value2
    global prix_prec
    global prix_actuel
    global energy_bought
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    while True :
        sleep(time) # we re-calculate the price each "x" milisecond where x is Time and it's an hard-coded constant
        # check if exceptionnal event
        with  external_mutex:
            if external1 :
                external_value1 += cte
            else :
                external_value1 = 0

            if external2 :
                external_value2 += cte
            else :
                external_value2 = 0

        with energy_mutex:
            prix_prec = prix_actuel
            prix_actuel = Y * prix_prec + S * energySell + B * energy_bought + external_value1 + external_value2 #where y s and b are hard-coded constant factor
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

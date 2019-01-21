import sys
from multiprocessing import Process, Array, Semaphore, Queue, Value
# import market
import weather
import homes
import market
import time
import sysv_ipc
import json
import matplotlib.pyplot as plt

SELL = 0
GIVE = 1
TRYGIVE = 2
CVOUKIVOI = 4


def graph():
    with open('prices.json', 'a') as w:
        w.write("0]}")
    with open('prices.json', 'r') as r:
        a = json.load(r)
        a = a['prices']
        a.pop()
        plt.plot(a)
        plt.show()
    print("end")


if __name__ == '__main__':
    print("Hello")
    running = Value('b', True)
    maxRequests = 4
    print('Initialization of the weather')
    a = Array('f', range(3))
    w = weather.Weather(a, running, 1)
    q = Queue(maxRequests)
    n = 12
    pol = CVOUKIVOI
    h = Process(target=homes.homes, args=(a, q, running, n, pol))
    m = market.Market(q, running, 2)
    m.start()
    w.start()
    h.start()
    print("gogogo")
    if input("Press any key") is not None:
        running.value = False
        print('STOPP')
    w.join()
    h.join()
    m.join()
    graph()

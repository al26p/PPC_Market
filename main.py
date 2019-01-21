from multiprocessing import Process, Array, Semaphore, Queue
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
    try:
        print("Hello")

        maxRequests = 4
        print('Initialization of the weather')
        a = Array('f', range(3))
        w = weather.Weather(a, 1)
        q = Queue(maxRequests)
        n = 10
        pol = GIVE
        h = Process(target=homes.homes, args=(a, q, n, pol))
        m = market.Market(q, 2)

        m.start()
        w.start()
        h.start()
        print("gogogo")
        w.join()
        h.join()
        m.join()
    except KeyboardInterrupt:
        time.sleep(1)
        try:
            sysv_ipc.remove_message_queue(2)
        except sysv_ipc.ExistentialError:
            pass
        try:
            sysv_ipc.remove_message_queue(3)
        except sysv_ipc.ExistentialError:
            pass
        graph()

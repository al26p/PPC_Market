from multiprocessing import Process, Array, Semaphore, Queue
# import market
import weather
import homes
import market
import time
import sysv_ipc

if __name__ == '__main__':
    try:
        print("Hello")

        maxRequests = 4
        print('Initialization of the weather')
        a = Array('f', range(3))
        w = weather.Weather(a, 1)
        q = Queue(maxRequests)
        h = Process(target=homes.homes, args=(a, q))
        m = market.Market(q, 2)

        m.start()
        w.start()
        h.start()
        print("gogogo")
        w.join()
        h.join()
        m.join()
    except KeyboardInterrupt:
        time.sleep(5)
        sysv_ipc.remove_message_queue(2)
        sysv_ipc.remove_message_queue(3)

    print("end")

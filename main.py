from multiprocessing import Process, Array, Semaphore
# import market
import weather
import homes
import market
import time

if __name__ == '__main__':
    try:
        print("Hello")


        print('Initialization of the weather')
        queue_semaphore=multiprocessing.Semaphore(4)
        a = Array('f', range(3))
        w = weather.Weather(a, 1)
        h = Process(target=homes.homes, args=(a,queue_semaphore,))
        m = market.Market(queue_semaphore, 2)

        m.start()
        w.start()
        h.start()
        print("gogogo")
        w.join()
        h.join()
        m.join()
    except KeyboardInterrupt:
        time.sleep(3)
    print("end")

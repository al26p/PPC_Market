from multiprocessing import Process, Array
# import market
import weather
import homes
import time

if __name__ == '__main__':
    try:
        print("Hello")


        print('Initialization of the weather')
        a = Array('f', range(3))
        w = weather.Weather(a, 1)
        h = Process(target=homes.homes, args=(a,))

        w.start()
        h.start()
        print("gogogo")
        w.join()
        h.join()
    except KeyboardInterrupt:
        time.sleep(3)
    print("end")
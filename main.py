from multiprocessing import Process, Array
# import market
import weather
import homes


if __name__ == '__main__':
    print("Hello")


    print('Initialization of the weather')
    a = Array('f', range(3))
    w = weather.Weather(a, 1)
    h = Process(target=homes.Homes, args=(a,))

    w.start()
    h.start()
    print("gogogo")
    w.join()
    h.join()
    print("end")
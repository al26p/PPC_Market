from multiprocessing import Process, Array

import weather
import homes


if __name__ == '__main__':
    print("Hello")


    print('Initialization of the weather')
    a = Array('i', range(2))
    w = Process(target=weather.weather, args=(a,))

    print('Opening tunnel with market')
    q = MessageQueue(1)
    m = Process(target=market.Main, args=(a, q))
    h = Process(target=homes.CalculatingPrice, args=(a, q))

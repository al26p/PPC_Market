from multiprocessing import Process, Array

import weather
import homes


if __name__ == '__main__':
    print("Hello")
    print('Initialization of the weather')
    a = Array('i', range(2))
    w = Process(target=weather.weather, args=(a,))
    h = Process(target=homes.Homes, args=(a, 'chan'))

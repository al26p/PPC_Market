from time import sleep
from multiprocessing import Lock, Process
import json


class Weather (Process) :
    def __init__ (self, mutex, array, refresh_interval=10):
        super().__init__()
        self.mutex = mutex
        self.array = array
        self.refresh_interval = refresh_interval

    def run (self):
        with open("meteoData.json", 'r') as in_data:
            data = json.load(in_data)
        while True :
            for i in range(len(data["wind"])):
                self.array = [273.15 + data["temp"][i], data["sun"][i], data["wind"][i]]
                print(self.array)
                sleep(self.refresh_interval)


if __name__ == "__main__" :
    p = Weather(Lock(),list(),0.01)
    p.start()
    p.join()

from time import sleep
from multiprocessing import Process
import json


class Weather(Process):
    def __init__(self, array, refresh_interval=10.0, debug=False):
        super().__init__()
        self.array = array
        self.refresh_interval = refresh_interval
        self.debug = debug

    def run(self):
        with open("meteoData.json", 'r') as in_data:
            data = json.load(in_data)
        while True:
            for i in range(len(data["wind"])):
                self.array[0] = round(273.15 + data["temp"][i], 2)
                self.array[1] = data["sun"][i]
                self.array[2] = data["wind"][i]
                if self.debug:
                    print(self.array)
                sleep(self.refresh_interval)


if __name__ == "__main__":
    p = Weather(list(), 0.01, True)
    p.start()
    p.join()

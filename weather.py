import random
import time


def weather(array, refresh_interval=60):
    while True:
        array[0] = random.randrange(0, 100) #wind
        array[1] = random.randrange(0, 100) #sun
        array[2] = random.randrange(220, 300) #temp in K
        time.sleep(refresh_interval)

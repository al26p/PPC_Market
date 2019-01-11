from time import sleep()


def weather(mutex, array, refresh_interval=10):
    f=open("meteoData.txt", 'r')
    while True:
        str = f.readline()
        str = str.strip('\n')
        str = str.split(' ')
        with mutex :
            array = str
        print(array)
        sleep(refresh_interval)

if __name__ == "__main__" :
    weather(list())

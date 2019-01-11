from multiprocessing import Process, Lock


COEF_TEMP = 0.2
COEF_SUN = 0.1
COEF_WIND = 0.08


def Homes(weather, chan):
    N = 10 # NOMBRE DE MAISONS
    lock = Lock()
    consomation = 0.0
    production = 0.0
    p_over_c = production / consomation
    global wind
    global sun
    global temp
    wind = weather[0]
    sun = weather[1]
    temp = weather[2]

    home = list()
    for i in range(N):
        home.append(Process(target=Home, args=(lock,)))
    for p in home:
        p.start()
    for p in home:
        p.join()


def Home(lock, time=60, c_initial=200, p_initial=100):
    while True:
        global consomation
        global production
        energy_politic = 1  # ou 2 ou 3, dépend de s'il veut donner
        consomation = time*(c_initial + temp*COEF_TEMP)
        production = time*(p_initial + wind*COEF_WIND + sun*COEF_SUN)
        with lock:
            consomation += consomation_propre
            production += production_propre

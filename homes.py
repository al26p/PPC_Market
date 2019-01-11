from multiprocessing import Process, Lock


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


def Home(lock, time, c_initial, p_initial):
    while True:
        global consomation
        global production
        energy_politic = 1  # ou 2 ou 3, dépend de s'il veut donner
        consomation = time*(c_initial + temp*coef_temp)
        production = time*(p_initial + wind*coef_wind + sun*coef_sun)
        with lock:
            consomation += consomation_propre
            production += production_propre

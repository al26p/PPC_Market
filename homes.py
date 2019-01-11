def Homes(weather, chan):
    lock = Lock()
    consomation = 0.0
    production = 0.0
    p_over_c = production / consomation
    wind = weather[0]
    sun = weather[1]
    temp = weather[2]

    runThread(Home(lock))

def Home(lock):
    global consomation
    global production
    energy_politic = 1  # ou 2 ou 3, dépend de s'il veut donner
    consomation = v_initiale + calcul_magique_conso(temp)
    production = v_initial + calcul_magique_prod(wind, sun)
    with lock:
        consomation += consomation_propre
        production += production_propre
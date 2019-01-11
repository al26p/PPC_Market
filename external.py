# randomly send a signal 1 or 2 to the market, telling it an event occur.
# sending a second time the same signal mean that the event end.

import random

class External(Process):

    proba1 = 0.1
    proba2 = 0.05
    crProba1 = 0.5
    crProba1 = 0.3
    p1
    p2


    def __init__ (time, marketPid)
        super().__init__()
        self.time = time
        self.marketPid = marketPid
        p1 = proba1
        p2 = proba2
        random.seed()

    def run (self) :
        while True :
            wait (time)
            i = random.random ()
            j = random.random ()
            if i < p1 :
                if p1 == proba1 :
                    p1 = crProba1
                else :
                    p1 = proba1
                signal(SIGUSR1, marketPid)
            if j < p2 :
                if p2 == proba2 :
                    p2 = crProba2
                else :
                    p2 = proba2
                signal(SIGUSR2, marketPid)

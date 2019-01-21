# randomly send a signal 1 or 2 to the market, telling it an event occur.
# sending a second time the same signal mean that the event end.
import random
from time import sleep
from multiprocessing import Process
from os import kill
import signal


class External(Process):
    PROBA1 = 0.04
    PROBA2 = 0.01
    CR_PROBA1 = 0.2
    CR_PROBA2 = 0.1

    def __init__(self, time, marketPid):
        super().__init__()
        self.time = time
        self.marketPid = marketPid
        self.p1 = self.PROBA1
        self.p2 = self.PROBA2
        random.seed()

    def run(self):
        while True:
            try:
                sleep(self.time)
                i = random.random()
                j = random.random()
                if i < self.p1:
                    if self.p1 == self.PROBA1:
                        self.p1 = self.CR_PROBA1
                    else:
                        self.p1 = self.PROBA1
                    kill(self.marketPid, signal.SIGUSR1)
                if j < self.p2:
                    if self.p2 == self.PROBA2:
                        self.p2 = self.CR_PROBA2
                    else:
                        self.p2 = self.PROBA2
                    kill(self.marketPid, signal.SIGUSR2)
            except KeyboardInterrupt:
                break

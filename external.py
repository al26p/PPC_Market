# randomly send a signal 1 or 2 to the market, telling it an event occur.
# sending a second time the same signal mean that the event end.
import random
from time import sleep
from multiprocessing import Process
from os import kill
import signal


class External(Process):
    PROBA1 = 0.1
    PROBA2 = 0.05
    CR_PROBA1 = 0.5
    CR_PROBA1 = 0.3

    def __init__(self, time, marketPid):
        super().__init__()
        self.time = time
        self.marketPid = marketPid
        self.p1 = self.PROBA1
        self.p2 = self.PROBA2
        random.seed()

    def run(self):
        while True:
            sleep(self.time)
            i = random.random()
            j = random.random()
            if i < self.p1:
                if self.p1 == self.PROBA1:
                    self.p1 = self.CR_PROBA1
                else:
                    self.p1 = self.PROBA1
                kill(signal.SIGUSR1, self.marketPid)
            if j < self.p2:
                if self.p2 == self.PROBA2:
                    self.p2 = self.CR_PROBA2
                else:
                    self.p2 = self.PROBA2
                kill(signal.SIGUSR2, self.marketPid)

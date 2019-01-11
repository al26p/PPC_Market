# randomly send a signal 1 or 2 to the market, telling it an event occur.
# sending a second time the same signal mean that the event end.
import random
from time import sleep
from multiprocessing import Process
from os import kill
import signal


class External(Process):
    proba1 = 0.1
    proba2 = 0.05
    cr_proba1 = 0.5
    cr_proba1 = 0.3

    def __init__(self, time, marketPid):
        super().__init__()
        self.time = time
        self.marketPid = marketPid
        self.p1 = self.proba1
        self.p2 = self.proba2
        random.seed()

    def run(self):
        while True :
            sleep(self.time)
            i = random.random()
            j = random.random()
            if i < self.p1:
                if self.p1 == self.proba1:
                    self.p1 = self.cr_proba1
                else:
                    self.p1 = self.proba1
                os.kill(signal.SIGUSR1, self.marketPid)
            if j < self.p2:
                if self.p2 == self.proba2:
                    self.p2 = self.cr_proba2
                else:
                    self.p2 = self.proba2
                os.kill(signal.SIGUSR2, self.marketPid)

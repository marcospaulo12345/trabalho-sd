from cProfile import run
from multiprocessing import Semaphore
import this
import threading 
import time
import random

class TicketSeller(threading.Thread):
    ticketsSold = 0

    def __init__(self, semaphore):
        threading.Thread.__init__(self);
        self.sem = semaphore
        print('Ticket Seller Started Work')

    def run(self):
        global ticketAvaliable
        running = True
        while running:
            self.randomDelay()

            self.sem.acquire()
            if (ticketAvaliable <= 0):
                running = False
            else:
                self.ticketsSold = self.ticketsSold + 1
                ticketAvaliable = ticketAvaliable - 1
                print('{} Sold One ({} left)'.format(self.getName(), ticketAvaliable))

            self.sem.release()
        print('Ticket Seller {} Sold {} ticket in total'. format(self.getName(), self.ticketsSold))
    def randomDelay(self):
        time.sleep(random.randint(0, 4) / 4)

semaphore = threading.Semaphore()

ticketAvaliable = 6

sellers = []
for i in range(4):
    seller = TicketSeller(semaphore)
    seller.start()
    sellers.append(seller)

for seller in sellers:
    seller.join()
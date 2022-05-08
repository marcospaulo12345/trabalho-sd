from cProfile import run
from multiprocessing import Semaphore
import this
import threading 
import time
import random

class TicketSeller(threading.Thread):
    ticketsSold = 0
    

    def __init__(self, semaphore, n):
        threading.Thread.__init__(self);
        self.sem = semaphore
        self.n = n
        print('Ticket Seller Started Work')

    def run(self):
        global servers
        print(servers)
        global CapServerActive
        self.sem.acquire()
        CapServerActive = servers[0][1]
        self.sem.release()
        running = True

        print('cap',CapServerActive)
        if (threading.active_count() - 1) <= n:
            print('Sevidor principal')
            time.sleep(8)
        else:
            while running:
                self.sem.acquire()
                print(CapServerActive)
                if (CapServerActive <= 0):
                    servers.remove(servers[0])
                    print(servers)
                    if servers:
                        CapServerActive = servers[0][1]
                    running = False
                else:
                    self.ticketsSold = self.ticketsSold + 1
                    CapServerActive = CapServerActive - 1
                    print('servidor parceiro:', servers[0][0])
                    print('{} Sold One ({} left)'.format(self.getName(), CapServerActive))
                    self.randomDelay()
                self.sem.release()
                

                
            print('Ticket Seller {} Sold {} ticket in total'. format(self.getName(), self.ticketsSold))
    def randomDelay(self):
        time.sleep(8)

semaphore = threading.Semaphore()

servers = [[1, 1], [2, 1]]
n = 1
CapServerActive = 0

sellers = []
for i in range(3):
    seller = TicketSeller(semaphore, n)
    seller.start()
    sellers.append(seller)

for seller in sellers:
    seller.join()
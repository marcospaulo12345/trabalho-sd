from re import L
import threading, queue
import time

q = queue.Queue()
listBloque = []
count = 0

def worker(n):
    global count
    global listBloque
    running = True
    if (threading.active_count() - 1) <= n:
        print('Servidor principal')
        time.sleep(5)
    else:
        print("count",count)
        if count <= 0:
            item = q.get()
            print('aaaa')
            q.task_done()
            if q.qsize() > 0:
                count = list(q.queue)[0][1]
                count = count - 1
                if item:
                    listBloque.append(item)
                print('lista bloque', listBloque)
                print('servidor ', list(q.queue)[0][0])
                time.sleep(5)
                for i in listBloque:
                    l = list(q.queue)
                    if i not in l:
                        q.put(i)
                print("kjdh: ", list(q.queue))
                
                if q.qsize() > 0:
                        lista_not_order = sorted(list(q.queue), key = lambda x: x[1], reverse=False)
                print('sdhfhghgj')
                with q.mutex:
                    q.queue.clear()
                for i in lista_not_order:
                    q.put(i)
                print(list(q.queue))
            print("count2",count)
        else:
            count = count - 1
            #print(f'Working on {item}')
            print("servidor: ",list(q.queue)[0][0])
            time.sleep(5)
            #print(f'Finished {item}')
        #print(list(q.queue))

# Turn-on the worker thread.

# Send thirty task requests to the worker.
"""for item in range(5):
    q.put(['parceiro', 1])"""

q.put(['parceiro1',1])
q.put(['parceiro2',2])

n = 1
count = list(q.queue)[0][1]
print(list(q.queue))
print(q.qsize())
threads = []
for i in range(3):
    thread = threading.Thread(target=worker, args=(n,))
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()
    print(thread)



# Block until all tasks are done.
q.join()
print('All work completed')
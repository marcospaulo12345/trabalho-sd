import socket
import pickle
import numpy as np
import pandas as pd
import threading, queue
import time
from multiprocessing import Process, Semaphore


UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT_NO = 6789

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

servers = []
q = queue.Queue()
CapServerActive = 0
list_servers_block = []

def prodMatrix(matrizA, matrizB):
    """Multiplica duas matrizes."""
    sizeLA = len(matrizA)
    sizeCA = len(matrizA[0]) # deve ser igual a sizeLB para ser possível multiplicar as matrizes
    sizeCB = len(matrizB[0])
    matrizR = []
    # Multiplica
    for i in range(sizeLA):
        matrizR.append([])
        for j in range(sizeCB):
            val = 0
            for k in range(sizeCA):
                    val += matrizA[i][k]*matrizB[k][j]
            matrizR[i].append(val)
    return matrizR

def run(data, addr, n, semaphore):
    result = False
    global count 
    global list_servers_block
    count = (threading.active_count() - 1)
    print("count !!!!", count)

    global servers
    global CapServerActive

    running = True

    if count <= n:
        print('n:', n, 'count:', count)
        try:
            data_arr = pickle.loads(data)
            print(len(data_arr))
            for i in range(len(data_arr)):
                #print(data_arr[i])
                if i > 1:
                    result = prodMatrix(result, data_arr[i])
                elif i == 1:
                    result = prodMatrix(data_arr[0], data_arr[1])
            print(result)
            result = pickle.dumps(result)
        except:
            pass
        message = 'recebido'
        time.sleep(20)
        serverSock.sendto(result, addr)
    else: 
        print('chama o servidor parceiro')
        print(threading.currentThread().name)
        print('porta',addr)
        UDP_IP_ADDRESS = list(q.queue)[0][1]
        UDP_PORT_NO = 6789
        desempenho = 0
        print(UDP_IP_ADDRESS)
        print('cap',CapServerActive)
        if (CapServerActive <= 0):
            item = q.get()
            print('aaaa')
            q.task_done()
            if q.qsize() > 0:
                CapServerActive = list(q.queue)[0][2]
                UDP_IP_ADDRESS = list(q.queue)[0][1]
                CapServerActive = CapServerActive - 1
                print('servidor parceiro:', list(q.queue)[0][0])
                print(CapServerActive)

                if item:
                    list_servers_block.append(item)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((UDP_IP_ADDRESS, UDP_PORT_NO))
                    s.sendall(data)
                    data_send = pickle.loads(data)

                    tm = len(data_send[0]) ** len(data_send)
                    t1 = time.time()
                    data_r = s.recv(65536)
                    tp = time.time() - t1
                    td = tm / tp

                    result = pickle.loads(data_r)
                    print('Recebido do servidor parceiro:', result)
                    result = pickle.dumps(result)
                    print('send to',addr)
                    serverSock.sendto(result, addr)
                print('ajksdhksdjKKKKKKKKK', CapServerActive)
                for i in list_servers_block:
                    l = list(q.queue)
                    if i not in l:
                        q.put(i)
                CapServerActive = list(q.queue)[0][2]
                
            print(list(q.queue))
            running = False
        else:
            CapServerActive = CapServerActive - 1
            print('servidor parceiro:', list(q.queue)[0][0])
            print(CapServerActive)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((UDP_IP_ADDRESS, UDP_PORT_NO))
                s.sendall(data)
                data_send = pickle.loads(data)

                tm = len(data_send[0]) ** len(data_send)
                t1 = time.time()
                data_r = s.recv(65536)
                tp = time.time() - t1
                td = tm / tp

                result = pickle.loads(data_r)
                print('Recebido do servidor parceiro:', result)
                result = pickle.dumps(result)
                print('send to',addr)
                serverSock.sendto(result, addr)
            CapServerActive = list(q.queue)[0][2]
        #else: 
        #    serverSock.sendto('Tente novamente mais tarde'.encode(), addr)
        #servidores
        #df_ordenado = servidores.sort_values(by='desempenho')

def runServerUDP(n):
    global count
    count = 0   
    global servers
    
    servers = [['parceiro1', '172.17.0.2', 1, 0],
               ['parceiro2', '172.17.0.3', 2, 0]]

    for i in servers:
        q.put(i)
    
    global CapServerActive
    CapServerActive = list(q.queue)[0][2]
    threads = []
    while True:
        
        print("rayner gay", servers)
        data, addr = serverSock.recvfrom(65536)
        semaphore = threading.Semaphore()
        thread = threading.Thread(target=run, args=(data, addr, n, semaphore))
        thread.start() 
        print(list(q.queue))
        threads.append(thread)
        
        print('Numero de thread: ' + str(threading.active_count()))
        #print(threading.enumerate())
    for thread in threads:
        thread.join()

def runServerTCP():
    global servers
    print('Essa merda é o TCP')
    TCP_IP_ADDRESS = '0.0.0.0'
    TCP_PORT_NO = 7005
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TCP_IP_ADDRESS, TCP_PORT_NO))
        s.listen()
        
        while True:
            conn, addr = s.accept()
            print("Conectado com: ", addr)
            data = conn.recv(65536)
            
            try:
                data_arr = pickle.loads(data)
                print(data_arr)

                try:
                    data2 = pd.read_csv('serverPc.csv')
                    data1 = pd.DataFrame([data_arr], columns=["Nome", "IP", "capacidade", "desempenho"])
                    saida = pd.concat([data2, data1], axis=0)
                    saida.to_csv('serverPc.csv', index=False)
                    servers = saida.values.tolist()
                    
                except:
                    data1 = pd.DataFrame([data_arr], columns=["Nome", "IP", "capacidade", "desempenho"])
                    print(data1)
                    data1.to_csv('serverPc.csv', index=False)
                    servers = data1.values.tolist()
                
                #lista.append(data_arr)
                conn.sendall('teste'.encode())
            except:
                print('caiu aqui?')
                pass

import os

"""def child():
    print('servidor parceiro')
    runServerTCP()

def parent():
    file = 'serverPc.csv'
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")

    n = int(input('Informe o número de requisições que o servidor suporta\n'))
    
    print('We are in the parent process with PID= %d' % os.getpid())
    newRef = os.fork()
    if newRef == 0:
        child()
    else:
        runServerUDP(n)
        print('We are in the parent process and our child process has PID = %d' % newRef)

if __name__ == '__main__':
    parent()"""

n = int(input('Informe o número de requisições que o servidor suporta\n'))
proc1 = Process(target=runServerTCP, args=())
proc2 = Process(target=runServerUDP, args=(n,))

proc1.start()
proc2.start()

proc1.join()
proc2.join()

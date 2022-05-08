import socket
import pickle
import numpy as np
import pandas as pd
import threading, queue
import time
from multiprocessing import Process, Semaphore
import os


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

def runServerPartner(UDP_IP_ADDRESS, UDP_PORT_NO, data, addr, serverSock):
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
    return td

def reuturn_servers_to_queue(list_servers_block):
    for i in list_servers_block:
        l = list(q.queue)
        if i not in l:
            q.put(i)

def update_performace_servers(td):
    copia_fila = list(q.queue).copy()
    with q.mutex:
        q.queue.clear()
    for i in range(len(copia_fila)):
        if copia_fila[i][1] == UDP_IP_ADDRESS:
            copia_fila[i][3] = td
    for i in copia_fila:
        q.put(i)

def order_queue():
    lista_not_order = sorted(list(q.queue), key = lambda x: x[3], reverse=True)
    with q.mutex:
        q.queue.clear()
    for i in lista_not_order:
        q.put(i)

def run(data, addr, n, semaphore):
    result = False
    global list_servers_block

    global servers
    global CapServerActive

    if (threading.active_count() - 1) <= n:
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
        time.sleep(20)
        serverSock.sendto(result, addr)
    else: 
        print('chama o servidor parceiro')
        
        if (CapServerActive <= 0):
            item = q.get(block=True)
            print('aaaa')
            if q.qsize() > 0:
                CapServerActive = list(q.queue)[0][2]
                UDP_IP_ADDRESS = list(q.queue)[0][1]
                UDP_PORT_NO = 6789
                CapServerActive = CapServerActive - 1
                print('servidor parceiro:', list(q.queue)[0][0])
                print(CapServerActive)

                if item:
                    list_servers_block.append(item)
                td = 0
                td = runServerPartner(UDP_IP_ADDRESS, UDP_PORT_NO, data, addr, serverSock)

                reuturn_servers_to_queue(list_servers_block)

                update_performace_servers(td)

                order_queue()
                CapServerActive = list(q.queue)[0][2]
                
            q.task_done()
            print(list(q.queue))
        else:
            UDP_IP_ADDRESS = list(q.queue)[0][1]
            UDP_PORT_NO = 6789
            print(UDP_IP_ADDRESS)
            CapServerActive = CapServerActive - 1
            print('servidor parceiro:', list(q.queue)[0][0])
            print(CapServerActive)
            td = 0
            td = runServerPartner(UDP_IP_ADDRESS, UDP_PORT_NO, data, addr, serverSock)

            update_performace_servers(td)

            order_queue()

            CapServerActive = list(q.queue)[0][2]
        #else: 
        #    serverSock.sendto('Tente novamente mais tarde'.encode(), addr)
        #servidores
        #df_ordenado = servidores.sort_values(by='desempenho')

def runServerUDP(n): 
    global servers

    servers = [['parceiro1', '172.17.0.2', 1, 0],
               ['parceiro2', '172.17.0.3', 2, 0]]

    for i in servers:
        q.put(i)
    
    global CapServerActive
    CapServerActive = list(q.queue)[0][2]
    while True:
        data, addr = serverSock.recvfrom(65536)
        semaphore = threading.Semaphore()
        thread = threading.Thread(target=run, args=(data, addr, n, semaphore))
        thread.start() 
        
        print('Numero de thread: ' + str(threading.active_count()))

def runServerTCP():
    global servers
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


UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT_NO = 6789

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

servers = []
q = queue.Queue()
CapServerActive = 0
list_servers_block = []

file = 'serverPc.csv'
if(os.path.exists(file) and os.path.isfile(file)):
    os.remove(file)
    print("file deleted")
else:
    print("file not found")

n = int(input('Informe o número de requisições que o servidor suporta\n'))
proc1 = Process(target=runServerTCP, args=())
proc2 = Process(target=runServerUDP, args=(n,))

proc1.start()
proc2.start()

proc1.join()
proc2.join()

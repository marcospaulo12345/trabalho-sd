import socket
import pickle
import numpy as np
import threading
import time
from multiprocessing import Process

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

def run(conn):
    
    data = conn.recv(65536)
    
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
        print('aaaaaaaaaaaaa')
        time.sleep(20)
        print('chegou aqui')
        conn.sendall(result)
    except:
        pass
    

def runServer():

    UDP_IP_ADDRESS = '172.17.0.3'
    UDP_PORT_NO = 6789
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
        while True:
            s.listen()
            conn, addr = s.accept()
            print("Conectado com: ", addr)

            thread = threading.Thread(target=run, args=(conn,))
            thread.start()

def runRegister():
    TCP_IP_ADDRESS = '192.168.0.104'
    #TCP_IP_ADDRESS = '10.0.0.110'
    TCP_PORT_NO = 7005
    global isRegister

    arr = ['parceiro2', socket.gethostbyname(socket.gethostname()), 2, 0]

    data_string = pickle.dumps(arr)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_IP_ADDRESS, TCP_PORT_NO))
        s.sendall(data_string)
        data = s.recv(65536)
        if data:
            isRegister = True
        print('Recebido do servidor:', data)


proc1 = Process(target=runRegister, args=())
proc2 = Process(target=runServer, args=())

proc1.start()
proc2.start()

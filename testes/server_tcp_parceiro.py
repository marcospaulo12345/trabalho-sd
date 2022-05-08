import socket
import pickle
import numpy as np
import threading
import time

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

UDP_IP_ADDRESS = '172.17.0.2'
UDP_PORT_NO = 6789

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    s.listen()
    
    while True:
        conn, addr = s.accept()
        print("Conectado com: ", addr)
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
            print(type(result))
            conn.sendall(result)
        except:
            pass

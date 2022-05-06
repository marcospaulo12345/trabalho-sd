import socket
import pickle
import numpy as np

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while 1:
    data = conn.recv(4096)
    result = False
    try:
        data_arr = pickle.loads(data)
        for i in range(len(data_arr)):
            #print(data_arr[i])
            if i > 1:
                result = np.dot(result, data_arr[i])
            elif i == 1:
                result = np.dot(data_arr[0], data_arr[1])
        print(result)
        result = pickle.dumps(result)
        conn.send(result)
    except:
        pass
    
conn.close()
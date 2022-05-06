import socket
import pickle
import numpy as np

UDP_IP_ADDRESS = '127.0.0.1'
#UDP_IP_ADDRESS = '172.17.0.3'
UDP_PORT_NO = 6789

arr = []
num_matriz = np.random.randint(2,8)
print(num_matriz)
for i in range(num_matriz):
    array = np.random.randint(100, size=(10, 10)).tolist()
    print(type(array))
    arr.append(array)

print(arr)

data_string = pickle.dumps(arr)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((UDP_IP_ADDRESS, UDP_PORT_NO))
    s.sendall(data_string)
    data = s.recv(65536)
    data_arr = pickle.loads(data)
    print('Recebido do servidor:', data_arr)
import socket
import pickle
import numpy as np


#UDP_IP_ADDRESS = '172.17.0.2'
UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT_NO = 6789

Message = 'Hello Server'

arr = []
num_matriz = np.random.randint(2,8)
print(num_matriz)
for i in range(num_matriz):
    array = np.random.randint(100, size=(10, 10)).tolist()
    print(type(array))
    arr.append(array)

print(arr)

"""arr = [[[1,2,3],[1,2,3], [1,2,3]],
      [[9,9,9],[1,2,3], [9,9,9]]]"""

data_string = pickle.dumps(arr)

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(data_string, (UDP_IP_ADDRESS, UDP_PORT_NO))

data, server = clientSock.recvfrom(65536)

try:

    data_arr = pickle.loads(data)
    print(data_arr)
except:
    print(data.decode())
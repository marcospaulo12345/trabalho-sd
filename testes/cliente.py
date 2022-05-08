import socket, pickle

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
arr = [[[1,2,3],[1,2,3], [1,2,3]],
      [[9,9,9],[1,2,3], [9,9,9]]]
data_string = pickle.dumps(arr)
s.send(data_string)

data = s.recv(4096)
data_arr = pickle.loads(data)
s.close()
print('Received', repr(data_arr))
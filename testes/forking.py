import os, sys, time

r,w=os.pipe()
r,w=os.fdopen(r,'r'), os.fdopen(w,'w')

pid = os.fork()
if pid:          # Parent
    w.close()
    data=r.readline()
    print("parent read: " + data.strip())
    print('servidor')   
else:           # Child
    r.close()
    while True:
        n = int(input('Informe o número de requisições que o servidor suporta\n'))
        w.write(str(n)+'\n')
        w.flush()
        time.sleep(1)


"""import os
import time
  
def communication(child_writes):
    # file descriptors r, w for reading and writing
    r, w = os.pipe()
      
    #Creating child process using fork
    processid = os.fork()
    if processid:
        # This is the parent process
        # Closes file descriptor w
        os.close(w)
        r = os.fdopen(r)
        print ("Parent reading")
        str = r.read()
        print( "Parent reads =", str)
    else:
        # This is the child process
        time.sleep(4)
        os.close(r)
        w = os.fdopen(w, 'w')
        print ("Child writing")
        w.write(child_writes+'gafs')
        print("Child writes = ",child_writes)
        w.close()
          
# Driver code        
child_writes = "Hello geeks"
communication(child_writes)"""
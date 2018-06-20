import numpy as np
import cv2
import socket
import time
import random
import sys

try:
    remote_ip = socket.gethostbyname( host )

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('10.0.0.208', 8082))

name = str(random.random())

s.send(str.encode(host))

def rcv():
    data = b''
    while 1:

        try:
            r = s.recv(180912)
            print(r)
            if len(r) == 0:
                print("1")
                exit(0)
            a = r.find(b'END!')
            if a != -1:
                data += r[:a]
                print("2")
                break
            data += r
        except Exception as e:
            print(e)
            continue
    nparr = numpy.fromstring(data, numpy.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if type(frame) is type(None):
        print('3')
        pass
    else:
        try:
            cv2.imshow(name,frame)
            if cv2.waitKey(10) == ord('q'):
                client_socket.close()
                sys.exit()
        except:
            client_socket.close()
            exit(0)

while 1:
    rcv()

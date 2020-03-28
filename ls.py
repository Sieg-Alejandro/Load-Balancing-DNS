import threading
import time
import random
import socket as mysoc
import pickle
import sys
# server task
def server():
    if len(sys.argv) != 6:
        print "Improper arguments. Please enter socket number"
        exit()
    if  not sys.argv[1].isdigit():
        print "Please enter a valid socket number"
        exit()
    
     
    portnum=int(sys.argv[1])
    ts1HostName=sys.argv[2]
    ts1portnum=int(sys.argv[3])
    ts2HostName=sys.argv[4]
    ts1portnum=int(sys.argv[5])

    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        ss.setsockopt(mysoc.SOL_SOCKET,mysoc.SO_REUSEADDR,1)
        ss2=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        ss2.setsockopt(mysoc.SOL_SOCKET,mysoc.SO_REUSEADDR,1)
        print("[S]: Server sockets created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',portnum)
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)

    ts1_binding=(ts1HostName, ts1portnum)
    ss2.connect(ts1_binding)
   
    
    
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)
    # send a intro  message to the client.
    while(True):
        client_recv=csockid.recv(4096)
        client_query=client_recv.decode('utf-8').rstrip()
        print("%s", client_recv)
        ss2.send(client_query.encode('utf-8'))
        if(client_query=="finished sending"):
            break
        csockid.send(client_recv)
        print("client queery: "+ client_query.lower()+'\n')
       
        
   # Close the server socket
    ss.close()
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()
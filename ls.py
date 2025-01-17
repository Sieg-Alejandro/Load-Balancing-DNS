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
    ts2portnum=int(sys.argv[5])

    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        ss.setsockopt(mysoc.SOL_SOCKET,mysoc.SO_REUSEADDR,1)
        tss1=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        tss2=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        
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
    print("ts1:info %s %s",ts1HostName,ts1portnum)
    tss1.connect(ts1_binding)

    ts2_binding=(ts2HostName, ts2portnum)
    print("ts2:info %s %s",ts2HostName,ts2portnum)
    tss2.connect(ts2_binding)



   
    
    
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)
    # send a intro  message to the client.
    while(True):
        check=1
        client_recv=csockid.recv(4096)
        client_query=client_recv.decode('utf-8').rstrip()
        print("%s", client_recv)
        tss1.send(client_query.encode('utf-8'))
        tss1.settimeout(5.0)
        try:
            server_response=tss1.recv(4096).decode('utf-8')
            tss1.settimeout(None)
            print server_response
            #If we get a response in this try block then we got an A record
        except mysoc.error, e:
            #timeout so we write host not found
            print(e)
            check=0
            print("Time out time\n")
        
        if check==0:
            tss2.send(client_query.encode('utf-8'))
            tss2.settimeout(5.0)
            try:
                server_response=tss2.recv(4096).decode('utf-8')
                tss2.settimeout(None)
                print server_response
                #If we get a response in this try block then we got an A record
            except mysoc.error, e:
                #timeout so we write host not found
                print(e)
                server_response="not in ts1 or ts2"
                print("Time out time\n")
        
        print("this is the end %s", server_response)
         

        #recvr=tss1.recv(4096)
        #print("here %s", recvr)
        
        if(client_query=="finished sending"):
            tss2.send(client_query.encode('utf-8'))
            break
        csockid.send(server_response.encode('utf-8'))
    
        
       
        
   # Close the server socket
    tss1.close()
    tss2.close()
    ss.close()
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()
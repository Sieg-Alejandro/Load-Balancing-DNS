import threading
import time
import random
import socket as mysoc
import pickle
import sys
# server task
def server():
    if len(sys.argv) != 2:
        print "Improper arguments. Please enter port number"
        exit()
    if  not sys.argv[1].isdigit():
        print "Please enter a valid port number"
        exit()

    portnum=int(sys.argv[1])
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        ss.setsockopt(mysoc.SOL_SOCKET,mysoc.SO_REUSEADDR,1)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',portnum)
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)

    #Open File
    fp=open('PROJI-DNSTS.txt')
    lines=fp.readlines()
    DNSTABLE={}
    TSHostname=""
    for line in lines:
        print(line)
        (hostname,ip,rtype)=line.split()
        if rtype=="NS":
            TSHostname=hostname
        DNSTABLE[hostname.lower()]=(ip,rtype)

    print DNSTABLE

    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)
    # send a intro  message to the client.
    while(True):
        client_recv=csockid.recv(4096)
        client_query=client_recv.decode('utf-8').rstrip()
        if(client_query=="finished sending"):
            break
        server_response=""
        # made client query lower so i didnt need to change it and it ignores case of the ips
        if client_query.lower() in DNSTABLE:
            ip,rtype=DNSTABLE[client_query.lower()]
            hostname=client_query
            server_response="%s %s %s" % (client_query,ip,rtype)
            csockid.send(server_response.encode('utf-8'))
            continue
        if client_query or client_query!="":
            server_response=(client_query+" Error:HOST NOT FOUND")
            csockid.send(server_response.encode('utf-8'))
       
        
        
   # Close the server socket
    ss.close()
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()

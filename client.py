import threading
import time
import random
import socket as mysoc
import pickle
import sys
import os
def client():
    if len(sys.argv) != 3:
        print "Improper arguments. Please enter port number"
        exit()
    if  not sys.argv[2].isdigit() and not sys.argv[3].isdigit():
        print "Please enter a valid port number"
        exit()

    lsListenport=int(sys.argv[2])
    lsHostName=sys.argv[1]
    try:
        cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        csts=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
# Define the port on which you want to connect to the server
    
    sa_sameas_myaddr =mysoc.gethostbyname(mysoc.gethostname())
# connect to the server on local machine
    server_binding=(lsHostName,lsListenport)
#Open file and send each line
    fp=open('PROJ2-HNS.txt')
    fp2=open("RESOLVED.txt", 'w')
    
   

    lines=fp.readlines()
    #lower cases all of the lines in the first file
    words=[]
    cs.connect(server_binding)
    connected=False
    for line in lines:
        cs.send(line.encode('utf-8'))  
        server_response=cs.recv(4096).decode('utf-8')
        print server_response
        
        #A record means get it from
       
        

    msg="finished sending"
    cs.send(msg.encode('utf-8'))
    cs.close()   
    if connected:
        csts.send(msg.encode('utf-8'))
        csts.close()

   
    fp.close()
    fp2.close()   
    os.system('truncate -s -1 RESOLVED.txt') #gets rid of the trailing new line character
    exit()



t2 = threading.Thread(name='client', target=client)
t2.start()
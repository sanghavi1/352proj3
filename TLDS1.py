import threading
import time
import random

import socket as mysoc

dns = {};

def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',38465) #Set up socket
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept() #Accept connection request
    print ("[S]: Got a connection request from a client at", addr)

# Continuous loop which receives data from the client
    while 1:
        data_from_client=csockid.recv(1024) #Receive data from client
        msg = data_from_client.decode('utf-8')
        print("[S]: Data Received: ", msg)

        if(msg.strip() == "disconnecting"): #If disconnecting, break out of the loop
            ss.close()
            exit()
        else:
            data = lookUp(msg) #Look up data sent in dictionary table
            csockid.sendall(data.encode('utf-8'))

   # Close the server socket
    ss.close()
    exit()

def createDict():
    fin = open("PROJ3-TLDS1.txt", "r"); #Open the file and insert all data into the dictionary
    flines = fin.readlines();
    for x in flines:
        splitStr = x.split();
        dns[splitStr[0]] = [splitStr[1], splitStr[2]] #Use hostname as key and assign flag and IP

def lookUp(hostname):
    if hostname in dns:
        if dns[hostname][1] == "A": #Check flag and return value based on that
            return hostname + " " + dns[hostname][0] + " " + dns[hostname][1];
    else:
        print ("Lookup was not found in dictionary at all") #If not found, return appropriate message
        return "Hostname - Error:HOST NOT FOUND"

createDict()
t1 = threading.Thread(name='server', target=server)
t1.start()
time.sleep(random.random()*5)
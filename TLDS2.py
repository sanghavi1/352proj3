import threading
import time
import random
import hmac

import socket as mysoc

dns = {};
key = ""

def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TLDS2]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',27463) #Set up socket
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[TLDS2]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[TLDS2]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()#Accept connection request
    print ("[TLDS2]: Got a connection request from a client at", addr)

# Continuous loop which receives data from the client
    while 1:
        data_from_client=csockid.recv(1024) #Receive data from client
        msg = data_from_client.decode('utf-8')
        print("[TLDS2]: Data Received: ", msg)

        if(msg.strip() == "disconnecting"): #If disconnecting, break out of the loop
            ss.close()
            exit()
        else:
            digest = hmac.new(key.encode(), msg.encode('utf-8'))

            csockid.sendall(digest.hexdigest().encode('utf-8'))

   # Close the server socket
    ss.close()
    exit()

def serverWithClient():
    try:
        css = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TLDS2]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', 35450)  # Set up socket
    css.bind(server_binding)
    css.listen(1)
    host = mysoc.gethostname()
    print("[TLDS2]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[TLDS2]: Server IP address is  ", localhost_ip)
    csockid, addr = css.accept()  # Accept connection request
    print ("[TLDS2]: Got a connection request from a client at", addr)

    # Continuous loop which receives data from the client
    while 1:
        data_from_client = csockid.recv(1024)  # Receive data from client
        msg = data_from_client.decode('utf-8')
        print("[TLDS2]: Data Received: ", msg)

        if (msg.strip() == "disconnecting"):  # If disconnecting, break out of the loop
            css.close()
            exit()
        else:
            data = lookUp(msg)
            csockid.sendall(data.encode('utf-8'))

    # Close the server socket
    css.close()
    exit()

def createDict():
    fin = open("PROJ3-TLDS2.txt", "r"); #Open the file and insert all data into the dictionary
    flines = fin.readlines();
    for x in flines:
        splitStr = x.split();
        dns[splitStr[0]] = [splitStr[1], splitStr[2]] #Use hostname as key and assign flag and IP
    fin = open("PROJ3-KEY2.txt", "r")
    global key
    key = fin.readline().rstrip('\n')


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

t2 = threading.Thread(name='serverWithClient', target=serverWithClient)
t2.start()


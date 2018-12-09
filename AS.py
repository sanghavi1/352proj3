import threading
import time
import random

import socket as mysoc

dns = {}


def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',55765) #Set up socket
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid,addr=ss.accept() #Accept connection request
    print ("[S]: Got a connection request from client at", addr)

    try: #Create socket for tlds1 Server
        tlds1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[RS]: Socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    try: #Create socket for tlds2 Server
        tlds2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[RS]: Socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    tlds1port = 38469
    sa_sameas_myaddr = mysoc.gethostbyname("cpp.cs.rutgers.edu")
    # Connect to the server on local machine
    #ip = mysoc.gethostbyname("Location of the EDU")
    server_binding = (sa_sameas_myaddr, tlds1port)

    tlds1.connect(server_binding)
    # Define the port on which you want to connect to the server
    tlds2port = 27463
    sa_sameas_myaddr = mysoc.gethostbyname("java.cs.rutgers.edu")
    #ip = mysoc.gethostbyname("Location of the COM")

    # Connect to the server using its IP and defined port
    server_binding = (sa_sameas_myaddr, tlds2port)
    tlds2.connect(server_binding)

# Continuous loop which receives data from the client
    while 1:
        data_from_client=csockid.recv(1024) #Receive data from client
        msg = data_from_client.decode('utf-8')
        print("[S]: Data Received: ", msg)

        if(msg.strip() == "disconnecting"): #If disconnecting, break out of the loop
            tlds1.sendall("disconnecting".encode('utf-8'))
            tlds2.sendall("disconnecting".encode('utf-8'))

            ss.close()
            tlds1.close()
            tlds2.close()
            exit()
        else:
            arr = msg.split(":")

            challenge = arr[0]
            digest = arr[1]
            tlds1.sendall(challenge.encode('utf-8'))
            digest1 = tlds1.recv(1024)

            tlds2.sendall(challenge.encode('utf-8'))
            digest2 = tlds2.recv(1024)
            d1 = digest1.decode('utf-8')
            d2 = digest2.decode('utf-8')
            if(d1==digest):
                server = "cpp.cs.rutgers.edu"
            elif(d2==digest):
                server = "java.cs.rutgers.edu"
            else:
                print("The matching digest was not found.")

            csockid.sendall(server.encode('utf-8'))


    tlds1.sendall("disconnecting".encode('utf-8'))
    tlds2.sendall("disconnecting".encode('utf-8'))

    time.sleep(random.random() * 10)
    #Close the server socket
    ss.close()
    #close other sockets
    tlds1.close()
    tlds2.close()
    exit()

def contactTLDS(server, message, tlds1, tlds2):

    msg = message

    if(server == "EDU"):
        tlds1.sendall(msg.rstrip().encode('utf-8'))
        print("[AS]: Data sent to TLDS1 server:", msg)  # Send the data to the Server and announce it
        data_from_server = tlds1.recv(1024) #Receive data from server, announce and decode it
        str = data_from_server.decode('utf-8')
        print("[AS]: Data received:", str)

    if server == "COM": #If the data returned from the RS Server has 'NS,' then send to TS Server
        tlds2.sendall(msg.rstrip().encode('utf-8'))
        print("[AS]: Data sent to TLDS2 server:", msg)  # Send the data to the Server and announce it
        data_from_server = tlds2.recv(1024)
        str = data_from_server.decode('utf-8') #Overwrite previous information with new info
        print("[AS]: Data received:", str)

    # Inform the servers that client is disconnecting
    # Close all open sockets/files

    return str

t1 = threading.Thread(name='server', target=server)
t1.start()
time.sleep(random.random()*5)

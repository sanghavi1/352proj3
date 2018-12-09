import threading
import socket as mysoc
import hmac


def client():
    #AS Socket Connection
    try:
        asss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    port = 55765
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    # Connect to the server on local machine
    server_binding = (sa_sameas_myaddr, port)
    asss.connect(server_binding)

    #TLDS1 Socket Connection
    try:
        tlds1ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    tlds1port = 35460
    sa_sameas_myaddr = mysoc.gethostbyname("cpp.cs.rutgers.edu")
    # Connect to the server on local machine
    server_binding = (sa_sameas_myaddr, tlds1port)
    tlds1ss.connect(server_binding)

    #TLDS2 Socket Connection
    try:
        tlds2ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    tlds2port = 35450
    sa_sameas_myaddr = mysoc.gethostbyname("java.cs.rutgers.edu")
    # Connect to the server on local machine
    server_binding = (sa_sameas_myaddr, tlds2port)
    tlds2ss.connect(server_binding)


    # Open the input file and output file, the output file will be created if it doesn't exist
    fout = open("PROJ3-HNS.txt", "r");
    fin = open("RESOLVED.txt", "w")

    flines = fout.readlines();
    # Read each line in the input file
    for x in flines:
        arr = x.split();
        key = arr[0]
        challenge = arr[1]
        hostname = arr[2]
        digest = hmac.new(key.encode(),challenge.encode('utf-8'))
        msg = challenge+":"+digest.hexdigest()
        print("[C]: Data sent to AS server:", msg)
        asss.sendall(msg.rstrip().encode('utf-8'))
        data_from_server = asss.recv(1024) #Which TLDS server to connect to
        str = data_from_server.decode('utf-8')
        print("[C]: Data received:", str)

        if(str == "cpp.cs.rutgers.edu"):
            tlds1ss.sendall(hostname.encode('utf-8'))
            finalHostName = tlds1ss.recv(1024)
        elif(str == "java.cs.rutgers.edu"):
            tlds2ss.sendall(hostname.encode('utf-8'))
            finalHostName = tlds2ss.recv(1024)


        fin.write(finalHostName.decode('utf-8') + '\n') #Write to file

    asss.sendall("disconnecting".encode('utf-8'))
    tlds1ss.sendall("disconnecting".encode('utf-8'))
    tlds2ss.sendall("disconnecting".encode('utf-8'))
    # Inform the servers that client is disconnecting
    # Close all open sockets/files
    fout.close()
    fin.close()
    asss.close()
    tlds1ss.close()
    tlds2ss.close()

    exit()

t2 = threading.Thread(name='client', target=client)
t2.start()

input("Hit ENTER  to exit")

exit()

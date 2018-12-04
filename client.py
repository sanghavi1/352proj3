import threading
import socket as mysoc

def client():
    try: #Create socket for RS Server
        rsss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    port = 55765
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    # Connect to the server on local machine
    server_binding = (sa_sameas_myaddr, port)
    rsss.connect(server_binding)

    # Open the input file and output file, the output file will be created if it doesn't exist
    fout = open("PROJ2-HNS.txt", "r");
    fin = open("RESOLVED.txt", "w")

    flines = fout.readlines();
    # Read each line in the input file
    for x in flines:
        msg = x
        rsss.sendall(msg.rstrip().encode('utf-8'))
        print("[C]: Data sent to RS server:", msg)  # Send the data to the Server and announce it
        data_from_server = rsss.recv(1024) #Receive data from server, announce and decode it
        str = data_from_server.decode('utf-8')
        print("[C]: Data received:", str)
        fin.write(str + '\n') #Write to file

    rsss.sendall("disconnecting".encode('utf-8'))
    # Inform the servers that client is disconnecting
    # Close all open sockets/files
    fout.close()
    fin.close()
    rsss.close()
    exit()

t2 = threading.Thread(name='client', target=client)
t2.start()

input("Hit ENTER  to exit")

exit()
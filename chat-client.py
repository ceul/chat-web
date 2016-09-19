from socket import *

def client():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    addr = ('', 3457)
    clientSocket.connect(addr)
    while True:
        message = raw_input("ingrese el exto a enviar: ")
        clientSocket.send(message+'\n')
        #data, server = clientSocket.recvfrom(1024)
        #print (data)
            #clientSocket.close()
    print "ejecuto"
client()
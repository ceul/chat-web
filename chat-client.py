from socket import *
import threading

def client():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    addr = ('', 3457)
    clientSocket.connect(addr)
    sending=threading.Thread(target=client_send, args=(clientSocket, ))
    listening=threading.Thread(target=client_listening, args=(clientSocket, ))
    listening.start()
    sending.start()


def client_send(clientSocket, ):
    print "entro"
    while True:
        message = raw_input("ingrese el exto a enviar: ")
        clientSocket.send(message+'\n')
            #clientSocket.close()

def client_listening(clientSocket, ):
    print"listening"
    while True:
        data, server = clientSocket.recvfrom(1024)
        print (data)
        if data=='';
            printf ("Reinicie el servicio, se ha caido la conexion")
            else:
                try:
                    clientSocket.send(u"\u2713")
                    except:
                        
                        continue

client()

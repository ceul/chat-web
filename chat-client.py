from socket import *

def client():
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    message = 'test'
    addr = ("", 3457)
    clientSocket.sendto(message, addr)
    #clientSocket.close()

client()
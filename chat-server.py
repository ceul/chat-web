from socket import *
import thread

def server():
    client_list=[]
    host, port = '', 3457
    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    #listen_socket.settimeout(60)
    listen_socket.bind((host, port))
    listen_socket.listen(50) #comienza a escuchar el puerto y se define que solo va a existir una conexion
    while True:
        client_connection, client_address = listen_socket.accept() #acepta la conexion
        client_list.append(client_connection)
        thread.start_new_thread(new_client, (client_connection, client_address,client_list))

def new_client(client_connection, client_address,client_list):
    while True:
        message = client_connection.recv(1024)#recive la conexion
        broadcast(client_list,message,client_connection)
        print "llego mensage"


def broadcast(client_list,message, actual_client):
    for client in client_list:
        if client == actual_client:
            continue
        else:
        #client_connection=client_list[client]
            client.sendall(message)# Envia la respuesta al cliente
    #client_connection.close()#Se cierra la conexion

server()
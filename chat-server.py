from socket import *
import thread
import MySQLdb
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import SystemRandom

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
    flag=False
    while flag==False:
        message = client_connection.recv(1024)#recibe la conexion
        if message =='':
            client_list.remove(client_connection)
            client_connection.close()
            print "Se cerro la conexion"
            flag=True
        elif (message.startswith('Login:'))==True:
            print message
            pos1=(message.find('User:',7)+5)
            pos2=(message.find('\n',pos1))
            user= message[pos1:pos2]
            pos3=message.find('Passw:',pos2)+6
            pos4=(message.find('\n',pos3))
            passw=message[pos3:pos4]
            res=compdatabase(user,passw)
            client_connection.sendall(res)
        elif (message.startswith('Register:'))==True:
            print message
            pos1=(message.find('User:',10)+5)
            pos2=(message.find('\n',pos1))
            user= message[pos1:pos2]
            IngresarUsuario(user)
        else:
            broadcast(client_list,message,client_connection)
            print message
            print "llego mensage"


def broadcast(client_list,message, actual_client):
    for client in client_list:
        if client == actual_client:
            continue
        else:
            client.sendall(message)# Envia la respuesta al cliente

def compdatabase(user,password):
    bd = MySQLdb.connect("localhost", "root", "admin", "bd_chat")
    cursor = bd.cursor()
    sql = 'SELECT correo,contrasena FROM usuario WHERE correo="%s" AND contrasena="%s"' % (user, password)
    rows_count = cursor.execute(sql)
    resultados = cursor.fetchall()
    print resultados
    if rows_count > 0:
        resultado = cursor.fetchall()
        print "El usuario esta registrado"
        return 'ok'
    else:
        print "El usuario no esta registrado"
        return 'no'
    bd.close()

def IngresarUsuario(user):
    def database(user, p):
        bd = MySQLdb.connect("localhost", "root", "admin", "bd_chat")
        # Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
        cursor = bd.cursor()
        # Preparamos el query SQL para insertar un registro en la BD
        sql = 'INSERT INTO usuario (correo,contrasena) VALUES("%s","%s")' % (user, p)
        try:
            cursor.execute(sql)
            bd.commit()
            print("\n Se inserto con exito")
        except:
            print("Hubo un problema")
            bd.rollback()
        bd.close()
    pass
    ##########  INICIO DATOS CORREO  #############
    # establecer conexion con el servidor de gmail
    mailserver = SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login("omgchat1.0@gmail.com", "ucatolica123")
    # construccion del mensaje
    mensaje = MIMEMultipart()
    mensaje['from'] = "omgchat1.0@gmail.com"
    mensaje['to'] = user
    mensaje['subject'] = "Confirmacion de cuenta OMGChat"
    longitud = 10
    valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cryptogen = SystemRandom()
    p = ""
    while longitud > 0:
        p = p + cryptogen.choice(valores)
        longitud = longitud - 1
    mensaje.attach(MIMEText("Saludos usuario, envio confirmacion de correo:\n Su contrasena es:" + p))
    database(user,p)
    # Enviar correo
    try:
        mailserver.sendmail(mensaje['from'], mensaje['to'], mensaje.as_string())
        print ("Envio correo")
    except:
        print("Error en envio del correo")
    # Cerrar conexion
    mailserver.close()

server()
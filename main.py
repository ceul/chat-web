from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import *
from kivy.uix.anchorlayout import *
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import SystemRandom
import MySQLdb
from socket import *
from kivy.uix.progressbar import ProgressBar
import threading
import os

Builder.load_string("""
<ChatLabel@Label>:
    text_size: (self.width, None)  # Step 1
    halign: 'left'
    valign: 'top'
    size_hint: (1, None)  # Step 2
    height: self.texture_size[1]  # Step 3
<ChatLabelOther@Label>
    text_size: (self.width, None)  # Step 1
    halign: 'left'
    valign: 'top'
    size_hint: (1, None)  # Step 2
    height: self.texture_size[1]  # Step 3
<ScrollView>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
<LoginScreen>:
    canvas.before:
        Color:
            rgb: (0.5, 0.5, 0.5, 1.0)
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Image:
            source: '/home/ceul/app/chat-web-master/icono.png'
            size: self.texture_size
            height: '55dp'
            size_hint_y: None
            pos_hint: {'center_x': .5, 'center_y': .8}
    FloatLayout:
        orientation: 'vertical'
        FloatLayout:
            orientation: 'vertical'
            Label:
                text:'Usuario'
                pos_hint: {'center_x': .5, 'center_y': .65}
                color: (0,0,0,1)
            TextInput:
                id:user
                size_hint_y: None
                height: '32dp'
                text: 'Ingrese su correo'
                focus: True
                pos_hint: {'center_x': .5, 'center_y': .55}
            Label:
                text:'Contrasena'
                pos_hint: {'center_x': .5, 'center_y': .47}
                color: (0,0,0,1)
            TextInput:
                id:passw
                size_hint_y: None
                height: '32dp'
                focus: True
                password:True
                pos_hint: {'center_x': .5, 'center_y': .4}
            FloatLayout:
                Button:
                    size_hint_y: None
                    height: '45dp'
                    pos_hint: {'center_x': .5, 'center_y': .28}
                    text: 'Iniciar Sesion'
                    on_press: root.compdatabase(user.text,passw.text)#aqui se envia la informacion que hay en los text inputs para ser procesadas
                Button:
                    size_hint_y: None
                    height: '45dp'
                    pos_hint: {'center_x': .5, 'center_y': .15}
                    text: 'Registrarse'
                    on_press: root.manager.current = 'register'
<LoginChatScreen>:
    canvas.before:
        Color:
            rgb: (0.5, 0.5, 0.5, 1.0)
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Image:
            source: '/home/ceul/app/chat-web-master/icono.png'
            size: self.texture_size
            height: '55dp'
            size_hint_y: None
            pos_hint: {'center_x': .5, 'center_y': .8}
    FloatLayout:
        orientation: 'vertical'
        FloatLayout:
            orientation: 'vertical'
            Label:
                text:'Usuario'
                pos_hint: {'center_x': .5, 'center_y': .65}
            TextInput:
                id:user
                size_hint_y: None
                height: '32dp'
                text: 'Ingrese su correo'
                focus: True
                pos_hint: {'center_x': .5, 'center_y': .55}
            Label:
                text:'Contrasena'
                pos_hint: {'center_x': .5, 'center_y': .47}
            TextInput:
                id:passw
                size_hint_y: None
                height: '32dp'
                focus: True
                password:True
                pos_hint: {'center_x': .5, 'center_y': .4}
            FloatLayout:
                Button:
                    size_hint_y: None
                    height: '45dp'
                    pos_hint: {'center_x': .5, 'center_y': .26}
                    text: 'Iniciar Sesion'
                    on_press: root.compdatabase1(user.text,passw.text)

<ChatScreen>:
    on_enter: root.recvMsg(chat_logs)
    BoxLayout:
        padding: 2
        orientation: 'vertical'
        Button:
            text:'Desconectar'
            size_hint: (0.2, 0.05)
        Button:
            text:'Enviar Archivo'
            on_press: root.manager.current='file'
            size_hint: (0.2, 0.05)
        ScrollView:
            ChatLabel:
                id: chat_logs
                color: (0,0,0,1)
        BoxLayout:
            height: 90
            orientation: 'horizontal'
            padding: 1
            size_hint: (1, 0.08)
            TextInput:
                id: message
            Button:
                text: 'Enviar'
                size_hint: (0.3, 1)
                on_press: root.sendMsg(message.text,chat_logs,message)
<RegisterScreen>:
    popup:popup.__self__
    canvas.before:
        Color:
            rgb: (0.5, 0.5, 0.5, 1.0)
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Image:
            source: '/home/ceul/app/chat-web-master/icono.png'
            size: self.texture_size
            height: '55dp'
            size_hint_y: None
            pos_hint: {'center_x': .5, 'center_y': .8}
    FloatLayout:
        orientation: 'vertical'
        FloatLayout:
            orientation: 'vertical'
            Label:
                text:'Email'
                pos_hint: {'center_x': .5, 'center_y': .58}
            TextInput:
                id:user
                size_hint_y: None
                height: '32dp'
                text: 'Ingrese su correo'
                focus: True
                pos_hint: {'center_x': .5, 'center_y': .5}
        FloatLayout:
            id: b1
            Popup:
                id:popup
                title:'Registro'
                on_parent:
                    if self.parent==b1:self.parent.remove_widget(self)
                Button:
                    text:'Un mensaje con su contrasena ah sido enviada a su correo Entendido'
                    on_release:popup.dismiss()
            Button:
                size_hint_y: None
                height: '45dp'
                pos_hint: {'center_x': .5, 'center_y': .26}
                text: 'Registrate'
                on_press:root.popup.open()
                on_press: root.IngresarUsuario(user.text)

                on_press: root.manager.current = 'login'
            Button:
                size_hint_y: None
                height: '45dp'
                pos_hint: {'center_x': .5, 'center_y': .15}
                text: 'Atras'
                on_press: root.manager.current = 'login'

<FileScreen>:
    BoxLayout:
        orientation:'vertical'
        Button:
            text: "Enviar"
            size_hint: (0.2, 0.05)
            on_release: root.send(filechooser.selection)
            on_release: root.manager.current='chat'
        FileChooserIconView:
            id: filechooser
""")
#on_press: root.manager.current = 'chat'
# Declare both screens

class LoginScreen(Screen):

    def compdatabase(self,user,password):

        bd = MySQLdb.connect("localhost", "root", "admin", "bd_chat")

        # Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
        cursor = bd.cursor()

        # Preparamos el query SQL para insertar un registro en la BD
        sql = 'SELECT correo,contrasena FROM usuario WHERE correo="%s" AND contrasena="%s"' % (user, password)

        rows_count = cursor.execute(sql)
        resultados = cursor.fetchall()
        print resultados
        if rows_count > 0:
            resultado = cursor.fetchall()
            print "El usuario esta registrado"
            conn.connect()
            self.manager.current = 'chat'
        else:
            print "El usuario no esta registrado"
        bd.close()
    pass

class LoginChatScreen(Screen):

    def compdatabase1(self,user,password):

        bd = MySQLdb.connect("localhost", "root", "admin", "bd_chat")
        # Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
        cursor = bd.cursor()

        # Preparamos el query SQL para insertar un registro en la BD
        sql = 'SELECT correo,contrasena FROM usuario WHERE correo="%s" AND contrasena="%s"' % (user, password)

        rows_count = cursor.execute(sql)
        resultados = cursor.fetchall()
        print resultados
        if rows_count > 0:
            resultado = cursor.fetchall()
            print "El usuario esta registrado"
            conn.connect()
            self.manager.current = 'chat'
        else:
            print "El usuario no esta registrado"
        bd.close()
    pass

class ChatScreen(Screen):
    def recvMsg(self,chat_logs_o):
        conn.listener_1(chat_logs_o)

    def sendMsg(self,msg,chat,message):
        conn.send_msg(msg,chat,message)
    pass

class FileScreen(Screen):
    def send(self, filename):
        print "selected: %s" % filename[0]
        #conn.send_file(filename[0])


class RegisterScreen(Screen):
    def IngresarUsuario(self,user):
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
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(LoginChatScreen(name='login2'))
sm.add_widget(ChatScreen(name='chat'))
sm.add_widget(RegisterScreen(name='register'))
sm.add_widget(FileScreen(name='file'))

class OMGChatApp(App):
    def build(self):
        return sm
    def connect(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        addr = ('', 3457)
        self.clientSocket.connect(addr)

    def send_msg(self,msg,chat_logs,message):
        if msg=='':
            pass
        else:
            self.clientSocket.send('%s' % ( msg))
            chat_logs.text += ('yo: %s\n' % ( msg))
            message.text = ''

    def send_file(self,path):
        with open(path, "rb") as archivo:
            buffer = archivo.read()
        while True:
            print "Enviando buffer"
            self.clientSocket.send(str(len(buffer)))
            print enviado
            recibido = self.clientSocket.recv(10)
            if recibido == "OK":
                for byte in buffer:
                    self.clientSocket.send(byte)
                break

    def listener_1(self,chat_logs):
        listening=threading.Thread(target=self.listener, args=(chat_logs, ))
        listening.start()

    def listener(self,chat_logs_o):
        while True:
            data, server = self.clientSocket.recvfrom(1024)
            print (data)
            if data=='':
                print ("Reinicie el servicio, se ha caido la conexion")
            else:
                print data
                chat_logs_o.text += ('otro: %s\n' % ( data))

conn=OMGChatApp()
if __name__ == '__main__':
        OMGChatApp().run()
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import *
from kivy.uix.anchorlayout import *
from socket import *
import threading
import thread
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
            rgb: (0.5, 0.5, 0.5, 1.0)
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
        orientation: 'vertical'
        FloatLayout:
            orientation: 'vertical'
            Label:
                text: 'Bienvenidos a OMGChat'
                pos_hint: {'center_x': .5, 'center_y': .85}
                height: '50dp'
                color: (0,0,0,1)
            Label:
                text:'Usuario'
                pos_hint: {'center_x': .5, 'center_y': .7}
                color: (0,0,0,1)
            TextInput:
                id:user
                size_hint_y: None
                height: '32dp'
                text: 'Ingrese su correo'
                focus: True
                pos_hint: {'center_x': .5, 'center_y': .6}
            Label:
                text:'Contrasena'
                pos_hint: {'center_x': .5, 'center_y': .5}
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
                    size_hint: (0.5, 0.085)
                    pos_hint: {'center_x': .5, 'center_y': .28}
                    text: 'Iniciar Sesion'
                    on_press: root.connect(user.text,passw.text)
                Button:
                    size_hint_y: None
                    height: '45dp'
                    size_hint: (0.5, 0.085)
                    pos_hint: {'center_x': .5, 'center_y': .15}
                    text: 'Registrarse'
                    on_press: root.manager.current = 'register'
<ChatScreen>:
    on_enter: root.recvMsg(chat_logs)
    BoxLayout:
        padding: 2
        orientation: 'vertical'
        Button:
            text:'Enviar Archivo'
            on_press: root.manager.current='file'
            size_hint: (0.4, 0.06)
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
        orientation: 'vertical'
        FloatLayout:
            orientation: 'vertical'
            Label:
                text: 'Bienvenidos a OMGChat'
                pos_hint: {'center_x': .5, 'center_y': .78}
                height: '50dp'
                color: (0,0,0,1)
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
                size_hint: (0.5, 0.085)
                pos_hint: {'center_x': .5, 'center_y': .26}
                text: 'Registrate'
                on_press: root.IngresarUsuario(user.text)
                on_press:root.popup.open()
                on_press: root.manager.current = 'login'
            Button:
                size_hint_y: None
                height: '45dp'
                size_hint: (0.5, 0.085)
                pos_hint: {'center_x': .5, 'center_y': .15}
                text: 'Atras'
                on_press: root.manager.current = 'login'
<FileScreen>:
    FloatLayout:
        orientation:'vertical'
        FileChooserIconView:
            id: filechooser
        Button:
            text: "Enviar"
            size_hint: (0.3, 0.08)
            pos_hint: {'center_x': .82, 'center_y': .22}
            on_release: root.send(filechooser.selection)
            on_release: root.manager.current='chat'
        Button:
            text: "Atras"
            size_hint: (0.3, 0.08)
            pos_hint: {'center_x': .82, 'center_y': .1}
            on_release: root.manager.current='chat'


""")
#on_press: root.manager.current = 'chat'
# Declare both screens

class LoginScreen(Screen):
    def connect(self,user,password):
        conn.connect()
        ans=conn.logindb(user,password)
        if ans=='1':
            self.manager.current='chat'

class ChatScreen(Screen):
    def recvMsg(self,chat_logs_o):
        conn.listener_1(chat_logs_o)

    def sendMsg(self,msg,chat,message):
        conn.send_msg(msg,chat,message)
    pass

class FileScreen(Screen):
    def send(self, filename):
        print "selected: %s" % filename[0]
        conn.send_file(filename[0])


class RegisterScreen(Screen):
    def IngresarUsuario(self,user):
        conn.registerdb(user)

# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(ChatScreen(name='chat'))
sm.add_widget(RegisterScreen(name='register'))
sm.add_widget(FileScreen(name='file'))

class OMGChatApp(App):
    def build(self):
        return sm
    def on_pause(self):
        return True
    def connect(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        addr = ('192.168.0.26', 3457)
        self.clientSocket.connect(addr)
        confile = ('', 9002)
        self.servidor = socket(AF_INET, SOCK_STREAM)
        self.servidor.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.servidor.bind(confile)
        self.servidor.listen(50)

    def send_msg(self,msg,chat_logs,message):
        if msg=='':
            pass
        else:
            if msg.endswith('\n'):
                msg=msg[:-1]
                self.clientSocket.send('%s: %s' % ( self.nick,msg))
                chat_logs.text += ('%s: %s' % ( self.nick,msg))
                message.text = ''
            else:
                self.clientSocket.send('%s: %s' % ( self.nick,msg))
                chat_logs.text += ('%s: %s' % ( self.nick,msg))
                message.text = ''

    def registerdb(self,user):
        if '@'in user:
            self.clientSocket.send('Register:\nUser:%s\n' % ( user))
        else:
            print 'no hay arroba'

    def logindb(self,user,password):
        if '@' in user:
            self.clientSocket.send('Login:\nUser:%s\nPassw:%s\n' % ( user,password))
            pos1=user.find('@')
            self.nick=user[0:pos1]
            data, server = self.clientSocket.recvfrom(1024)
            if data=='Login ok':
                print 'entro'
                return '1'
        else:
            print 'no hay arroba'
    def send_file(self,path):
        head, name = os.path.split(path)
        self.clientSocket.send('File:\nName:%s\n' % ( name))
        sending_file=threading.Thread(target=self.send_file1, args=(path, ))
        sending_file.start()

    def send_file1(self,path):
        #self.clientSocket.send('threading')
        CONEXION = ('192.168.0.26', 9001)
        cliente = socket(AF_INET, SOCK_STREAM)
        #self.clientSocket.send('1')
        cliente.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        #self.clientSocket.send('2')
        cliente.connect(CONEXION)
        #self.clientSocket.send('conecto')
        with open(path, "rb") as archivo:
            buffer = archivo.read()
        while True:
            print "Enviando buffer"
            cliente.send(str(len(buffer)))
            recibido = cliente.recv(10)
            if recibido == "OK":
                for byte in buffer:
                    cliente.send(byte)
                break

    def recv_file(self,name,chat_logs):
        sck, addr = self.servidor.accept()
        print "Conectado a: {0}:{1}".format(*addr)
        while True:
            recibido = sck.recv(1024).strip()
            if recibido:
                print "Recibido:", recibido
            if recibido.isdigit():
                sck.send("OK")
                buffer = 0
                with open("/storage/emulated/0/OMGchat/"+name, "wb") as archivo:
                    while (buffer <= int(recibido)):
                        data = sck.recv(1)
                        if not len(data):
                            break
                        archivo.write(data)
                        buffer += 1
                    if buffer == int(recibido):
                        print "Archivo descargado con exito"
                        chat_logs.text+=("Llego Archivo: "+name+"\n")
                    else:
                        print "Ocurrio un error/Archivo incompleto"
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
            elif (data.startswith("('_')")):
                chat_logs_o.text += ('              %s\n'% data )
            elif (data.startswith('File:'))==True:
                print 'entro'
                print data
                pos1=(data.find('Name:',6)+5)
                pos2=(data.find('\n',pos1))
                name= data[pos1:pos2]
                #head, name = os.path.split(path)
                print name
                recv=threading.Thread(target=self.recv_file, args=(name,chat_logs_o))
                recv.start()
            else:
                print data
                chat_logs_o.text += ('%s\n' % ( data))

nuevaruta = r'/storage/emulated/0/OMGchat'
if not os.path.exists(nuevaruta): os.makedirs(nuevaruta)
conn=OMGChatApp()
conn.connect()
if __name__ == '__main__':
        OMGChatApp().run()


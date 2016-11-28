from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import *
from kivy.uix.anchorlayout import *
from kivy.uix.image import *
from socket import *
import threading
import os
from plyer import *
import time
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from jnius import autoclass

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
            rgb: (0.16, 0.32, 0.75)
        Rectangle:
            pos: self.pos
            size: self.size

<LoginScreen>:
    canvas.before:
        Color:
            rgb: (0.16, 0.32, 0.75)
        Rectangle:
            pos: self.pos
            size: self.size
    Image:
        source:'/storage/emulated/0/OMG/icon.png'
        size: self.texture_size
        height:'55dp'
        size_hint_y:None
        pos_hint: {'center_x': .5, 'center_y': .85}
    FloatLayout:
        orientation: 'vertical'
        FloatLayout:
            orientation: 'vertical'
            Label:
                text:'Usuario'
                pos_hint: {'center_x': .5, 'center_y': .7}
                color: (1,1,1,1)
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
                color: (1,1,1,1)
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
                    background_color:(1,1,1,0.3)
                    height: '45dp'
                    size_hint: (0.5, 0.085)
                    pos_hint: {'center_x': .5, 'center_y': .28}
                    text: 'Iniciar Sesion'
                    on_press: root.connect(user.text,passw.text)
                Button:
                    size_hint_y: None
                    background_color:(1,1,1,0.3)
                    height: '45dp'
                    size_hint: (0.5, 0.085)
                    pos_hint: {'center_x': .5, 'center_y': .16}
                    text: 'Registrarse'
                    on_press: root.manager.current = 'register'
                
<ChatScreen>:
    on_enter: root.recvMsg(chat_logs)
    BoxLayout:
        padding: 2
        orientation: 'vertical'
        BoxLayout:
            height: 90
            orientation: 'horizontal'
            size_hint: (1, 0.05)
            Button:
                text:'Enviar Archivo'
                on_press: root.manager.current='file'
                size_hint: (1, 1)
                background_color:(1,1,1,0.3)
            Button:
                text:'Foto'
                on_press: root.cameraPic()
                size_hint: (1, 1)
                background_color:(1,1,1,0.3)
                
            Button:
                text:'Video'
                on_press: root.cameraVid()
                size_hint: (1, 1)
                background_color:(1,1,1,0.3)

            Button:
                text:'Audio'
                on_press: root.manager.current='audio'
                size_hint: (1, 1)
                background_color:(1,1,1,0.3)
        ScrollView:
            ChatLabel:
                id: chat_logs
                color: (1,1,1,1)
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
                background_color:(1,1,1,0.3)

<RegisterScreen>:
    popup:popup.__self__
    canvas.before:
        Color:
            rgb: (0.16, 0.32, 0.75)
        Rectangle:
            pos: self.pos
            size: self.size
    Image:
        source:'/storage/emulated/0/OMG/icon.png'
        size: self.texture_size
        height:'55dp'
        size_hint_y:None
        pos_hint: {'center_x': .5, 'center_y': .85}
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
                size_hint: (0.5, 0.085)
                background_color:(1,1,1,0.3)
                pos_hint: {'center_x': .5, 'center_y': .26}
                text: 'Registrate'
                on_press: root.IngresarUsuario(user.text)
                on_press:root.popup.open()
                on_press: root.manager.current = 'login'
            Button:
                size_hint_y: None
                height: '45dp'
                size_hint: (0.5, 0.085)
                background_color:(1,1,1,0.3)
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

<AudioTool>
    orientation: 'vertical'
    Label:
        id: display_label
        text: '00:00'
        pos_hint: {'center_x': .5, 'center_y': .6}
    FloatLayout:
        TextInput:
            id: user_input
            text: '5'
            size_hint_y: None
            height: '32dp'
            focus: True
            pos_hint: {'center_x': .5, 'center_y': .46}
            disabled: duration_switch.active == False #TUT 3 IF SWITCH IS OFF TEXTINPUT IS DISABLED
            on_text: root.enforce_numeric()
        Switch:
            id: duration_switch
            pos_hint: {'center_x': .5, 'center_y': .35}
    FloatLayout:
        orientation:'horizontal'
        Button:
            size_hint_y: None
            height: '45dp'
            size_hint: (0.5, 0.085)
            id: start_button
            text: 'Empezar Grabacion'
            on_release: root.startRecording_clock()
            pos_hint: {'center_x': .25, 'center_y': .1}
        Button:
            size_hint_y: None
            height: '45dp'
            size_hint: (0.5, 0.085)
            id: stop_button
            text: 'Terminar Grabacion'
            pos_hint: {'center_x': .5, 'center_y': .23}
            on_release: root.stopRecording()
            disabled: True
        Button:
            size_hint_y: None
            height: '45dp'
            size_hint: (0.5, 0.085)
            id: back_button
            text: 'Atras'
            pos_hint: {'center_x': .75, 'center_y': .1}
            on_release: root.manager.current='chat'
""")
#on_press: root.manager.current = 'chat'
# Declare both screens

class LoginScreen(Screen):
    def connect(self,user,password):
        #conn.connect()
        ans=conn.logindb(user,password)
        if ans=='1':
            self.manager.current='chat'

class ChatScreen(Screen):
    def cameraPic(self):
        conn.camPic()
    def cameraVid(self):
        conn.camVid()
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

class MyRecorder:
    def __init__(self):
        '''Recorder object To access Android Hardware'''
        path='/storage/emulated/0/OMGchat/OMGAudios/'
        date=time.strftime("%d%m%y")
        i=0
        audname='AUD-'+date+'-OMG'+str(i)+'.3gp'
        cpath=path+audname
        while(True):
            if os.path.exists(cpath):
                i=i+1
                audname='AUD-'+date+'-OMG'+str(i)+'.3gp'
                cpath=path+audname
            else:
                break
        self.MediaRecorder = autoclass('android.media.MediaRecorder')
        self.AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
        self.OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
        self.AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

        # create out recorder
        self.mRecorder = self.MediaRecorder()
        self.mRecorder.setAudioSource(self.AudioSource.MIC)
        self.mRecorder.setOutputFormat(self.OutputFormat.THREE_GPP)
        self.mRecorder.setOutputFile(cpath)
        self.mRecorder.setAudioEncoder(self.AudioEncoder.AMR_NB)
        self.mRecorder.prepare()

class AudioTool(Screen):
    def __init__(self, **kwargs):
        super(AudioTool, self).__init__(**kwargs)

        self.start_button = self.ids['start_button']
        self.stop_button = self.ids['stop_button']
        self.display_label = self.ids['display_label']
        self.switch = self.ids['duration_switch']  # Tutorial 3
        self.user_input = self.ids['user_input']

    def enforce_numeric(self):
        '''Make sure the textinput only accepts numbers'''
        if self.user_input.text.isdigit() == False:
            digit_list = [num for num in self.user_input.text if num.isdigit()]
            self.user_input.text = "".join(digit_list)

    def startRecording_clock(self):

        self.mins = 0  # Reset the minutes
        self.zero = 1  # Reset if the function gets called more than once
        self.duration = int(self.user_input.text)  # Take the input from the user and convert to a number
        Clock.schedule_interval(self.updateDisplay, 1)
        self.start_button.disabled = True  # Prevents the user from clicking start again which may crash the program
        self.stop_button.disabled = False
        self.switch.disabled = True  # TUT Switch disabled when start is pressed
        Clock.schedule_once(self.startRecording)  ## NEW start the recording

    def startRecording(self, dt):  # NEW start the recorder
        self.r = MyRecorder()
        self.r.mRecorder.start()

    def stopRecording(self):

        Clock.unschedule(self.updateDisplay)
        self.r.mRecorder.stop()  # NEW RECORDER VID 6
        self.r.mRecorder.release()  # NEW RECORDER VID 6
        path='/storage/emulated/0/OMGchat/OMGAudios/'
        date=time.strftime("%d%m%y")
        i=0
        audname='AUD-'+date+'-OMG'+str(i)+'.3gp'
        cpath=path+audname
        while(True):
            if os.path.exists(cpath):
                i=i+1
                audname='AUD-'+date+'-OMG'+str(i)+'.3gp'
                cpath=path+audname
            else:
                break
        i=i-1
        audname='AUD-'+date+'-OMG'+str(i)+'.3gp'
        cpath=path+audname
        conn.send_file(cpath)

        Clock.unschedule(self.startRecording)  # NEW stop the recording of audio VID 6
        self.display_label.text = 'Finished Recording!'
        self.start_button.disabled = False
        self.stop_button.disabled = True  # TUT 3
        self.switch.disabled = False  # TUT 3 re enable the switch

    def updateDisplay(self, dt):
        if self.switch.active == False:
            if self.zero < 60 and len(str(self.zero)) == 1:
                self.display_label.text = '0' + str(self.mins) + ':0' + str(self.zero)
                self.zero += 1

            elif self.zero < 60 and len(str(self.zero)) == 2:
                self.display_label.text = '0' + str(self.mins) + ':' + str(self.zero)
                self.zero += 1

            elif self.zero == 60:
                self.mins += 1
                self.display_label.text = '0' + str(self.mins) + ':00'
                self.zero = 1

        elif self.switch.active == True:
            if self.duration == 0:  # 0
                self.display_label.text = 'Recording Finished!'
                self.stopRecording()  # NEW VID 6 / THIS ONE LINE SHOULD TAKE CARE OF THE RECORDING NOT STOPPING.
                # self.start_button.disabled = False # Re enable start
                # self.stop_button.disabled = True # Re disable stop
                # Clock.unschedule(self.updateDisplay) #DELETE FOR VID 6
                # self.switch.disabled = False # Re enable the switch
                
            elif self.duration > 0 and len(str(self.duration)) == 1:  # 0-9
                self.display_label.text = '00' + ':0' + str(self.duration)
                self.duration -= 1

            elif self.duration > 0 and self.duration < 60 and len(str(self.duration)) == 2:  # 0-59
                self.display_label.text = '00' + ':' + str(self.duration)
                self.duration -= 1

            elif self.duration >= 60 and len(str(self.duration % 60)) == 1:  # EG 01:07
                self.mins = self.duration / 60
                self.display_label.text = '0' + str(self.mins) + ':0' + str(self.duration % 60)
                self.duration -= 1

            elif self.duration >= 60 and len(str(self.duration % 60)) == 2:  # EG 01:17
                self.mins = self.duration / 60
                self.display_label.text = '0' + str(self.mins) + ':' + str(self.duration % 60)
                self.duration -= 1


# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(ChatScreen(name='chat'))
sm.add_widget(RegisterScreen(name='register'))
sm.add_widget(FileScreen(name='file'))
sm.add_widget(AudioTool(name='audio'))


class OMGChatApp(App):
    def build(self):
        return sm
    def on_pause(self):
        return True
    def connect(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        addr = ('192.168.0.19', 3457)
        self.clientSocket.connect(addr)
        confile = ('', 9002)
        self.servidor = socket(AF_INET, SOCK_STREAM)
        self.servidor.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.servidor.bind(confile)
        self.servidor.listen(50)

    def  camPic(self):
        path='/storage/emulated/0/OMGchat/OMGImages/'
        date=time.strftime("%d%m%y")
        i=0
        imgname='IMG-'+date+'-OMG'+str(i)+'.jpg'
        cpath=path+imgname
        while(True):
            if os.path.exists(cpath):
                i=i+1
                imgname='IMG-'+date+'-OMG'+str(i)+'.jpg'
                cpath=path+imgname
            else:
                break
        camera.take_picture(cpath,self.done)

    def done(self,path):
        self.send_file(path)
        self.root.current='chat'

    def  camVid(self):
        path='/storage/emulated/0/OMGchat/OMGVideos/'
        date=time.strftime("%d%m%y")
        i=0
        vidname='VID-'+date+'-OMG'+str(i)+'.mp4'
        cpath=path+vidname
        while(True):
            if os.path.exists(cpath):
                i=i+1
                vidname='VID-'+date+'-OMG'+str(i)+'.mp4'
                cpath=path+vidname
            else:
                break
        camera.take_video(cpath,self.done1)

    def done1(self,path):
        self.send_file(path)
        self.root.current='chat'


    def send_msg(self,msg,chat_logs,message):
        hour =time.strftime("%H:%M:%S")
        if msg=='':
            pass
        else:
            if msg.endswith('\n'):
                msg=msg[:-1]
                self.clientSocket.send('%s: %s' % ( self.nick,msg))
                chat_logs.text += ('\n-%s: %s        %s' % ( self.nick,msg,hour))
                message.text = ''
            else:
                self.clientSocket.send('%s: %s' % ( self.nick,msg))
                chat_logs.text += ('\n-%s: %s        %s' % ( self.nick,msg,hour))
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
        self.chat_log.text+=('Enviando archivo: %s \n'% name)
        sending_file=threading.Thread(target=self.send_file1, args=(path,name))
        sending_file.start()
    def on_key_up(self):
        Window.softinput_mod='pan'
    def send_file1(self,path,name):
        #self.clientSocket.send('threading')
        CONEXION = ('192.168.0.19', 9001)
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
                self.chat_log.text+=('Termino de enviar archivo: %s \n'% name)
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
        self.chat_log=chat_logs
        listening=threading.Thread(target=self.listener, args=(chat_logs, ))
        listening.start()

    def listener(self,chat_logs_o):
        while True:
            data, server = self.clientSocket.recvfrom(1024)
            print (data)
            chat_logs_o.text+='-'
            if data=='':
                print ("Reinicie el servicio, se ha caido la conexion")
            elif (data.startswith("('_')")):
                print 'llego'
                chat_logs_o.text += ('              ...r\n')
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
                vibrator.cancel()
                vibrator.vibrate(time=1)
                hour =time.strftime("%H:%M:%S")
                chat_logs_o.text += ('%s       %s\n\n' % ( data,hour))

nuevaruta = r'/storage/emulated/0/OMGchat'
if not os.path.exists(nuevaruta): os.makedirs(nuevaruta)
nuevaruta1 = r'/storage/emulated/0/OMGchat/OMGImages'
if not os.path.exists(nuevaruta1): os.makedirs(nuevaruta1)
nuevaruta2 = r'/storage/emulated/0/OMGchat/OMGVideos'
if not os.path.exists(nuevaruta2): os.makedirs(nuevaruta2)
nuevaruta3 = r'/storage/emulated/0/OMGchat/OMGAudios'
if not os.path.exists(nuevaruta3): os.makedirs(nuevaruta3)

conn=OMGChatApp()
conn.connect()
if __name__ == '__main__':
        OMGChatApp().run()

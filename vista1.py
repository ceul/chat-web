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
from kivy.uix.progressbar import ProgressBar

Builder.load_string("""
<ChatLabel@Label>:
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
            source: '/home/julian/Escritorio/app/icono.png'
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
            source: '/home/julian/Escritorio/app/icono.png'
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
    BoxLayout:
        padding: 2
        orientation: 'vertical'
        Button:
            text: 'Desconectar'
            size_hint: (0.2, 0.05)
            on_press: root.manager.current = 'login'
        ScrollView:
            ChatLabel:
                id: chat_logs
                text: 'User says: foo'
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
                disabled: True

<RegisterScreen>:
    canvas.before:
        Color:
            rgb: (0.5, 0.5, 0.5, 1.0)
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Image:
            source: '/home/julian/Escritorio/app/icono.png'
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
            Button:
                size_hint_y: None
                height: '45dp'
                pos_hint: {'center_x': .5, 'center_y': .26}
                text: 'Registrate'
                on_press: root.IngresarUsuario(user.text)
                on_press: root.manager.current = 'login2'


""")
#on_press: root.manager.current = 'chat'
# Declare both screens

class LoginScreen(Screen):

    def compdatabase(self,user,password):

        bd = MySQLdb.connect("localhost", "root", "Agape102", "bd_chat")

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
            self.manager.current = 'chat'
        else:
            print "El usuario no esta registrado"
        bd.close()
    pass

class LoginChatScreen(Screen):

    def compdatabase1(self,user,password):

        bd = MySQLdb.connect("localhost", "root", "Agape102", "bd_chat")
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
            self.manager.current = 'chat'
        else:
            print "El usuario no esta registrado"
        bd.close()
    pass

class ChatScreen(Screen):
    pass

class RegisterScreen(Screen):

    def IngresarUsuario(self,user):
        def database(user, p):
            bd = MySQLdb.connect("localhost", "root", "Agape102", "bd_chat")
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

class OMGChatApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
        OMGChatApp().run()
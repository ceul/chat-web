from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import *
from kivy.uix.anchorlayout import *

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
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text:'Usuario'
            TextInput:
                id:user
            Label:
                text:'Contrasena'
            TextInput:
                id:pass
        BoxLayout:
            Button:
                text: 'Iniciar Sesion'
                on_press: root.manager.current = 'chat'
                size_hint: (0.1, 0.3)
            Button:
                text: 'Registrarse'
                on_press: root.manager.current = 'register'
                size_hint: (0.1, 0.3)

<ChatScreen>:
    BoxLayout:
        padding: 2
        orientation: 'vertical'
        Button:
            text: 'Desconectar'
            size_hint: (0.2, 0.05)
            on_press: root.current = 'login'
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

<RegisterScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text:'Email'
            TextInput:
                id:user
        BoxLayout:
            Button:
                text: 'Registrate'
                on_press: root.manager.current = 'login'
                size_hint: (0.08, 0.3)
""")

# Declare both screens
class LoginScreen(Screen):
    pass

class ChatScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(ChatScreen(name='chat'))
sm.add_widget(RegisterScreen(name='register'))
class TomChatApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TomChatApp().run()

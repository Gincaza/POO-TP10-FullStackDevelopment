import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from databasemanager import DatabaseManager

# Carregar arquivos kv
Builder.load_file("kv/login.kv")
Builder.load_file("kv/main.kv")
Builder.load_file("kv/register.kv")

class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def do_login(self):
        username = self.username.text
        password = self.password.text

        response = requests.post("http://127.0.0.1:5000/login", json={
            "username": username,
            "senha": password
        })

        if response.status_code == 200:
            self.manager.current = 'main'
        else:
            popup = Popup(title='Login Failed', content=Label(text='Invalid credentials'), size_hint=(None, None), size=(400, 400))
            popup.open()

class MainScreen(Screen):
    def on_pre_enter(self):
        self.load_clientes()
        self.load_hamburgueres()

    def load_clientes(self):
        response = requests.get("http://127.0.0.1:5000/cliente")
        if response.status_code == 200:
            clientes = response.json()
            self.ids.cliente_list.clear_widgets()
            for cliente in clientes:
                self.ids.cliente_list.add_widget(Label(text=f"{cliente['nome']} - {cliente['telefone']}"))

    def load_hamburgueres(self):
        response = requests.get("http://127.0.0.1:5000/hamburguer")
        if response.status_code == 200:
            hamburgueres = response.json()
            self.ids.hamburguer_list.clear_widgets()
            for hamburguer in hamburgueres:
                self.ids.hamburguer_list.add_widget(Label(text=f"{hamburguer['nome_hamburguer']} - {hamburguer['ingredientes']}"))

class RegisterScreen(Screen):
    nome = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def register(self):
        nome = self.nome.text
        username = self.username.text
        password = self.password.text

        response = requests.post("http://127.0.0.1:5000/register", json={
            "nome": nome,
            "username": username,
            "senha": password
        })

        if response.status_code == 201:
            self.manager.current = 'login'
        else:
            popup = Popup(title='Register Failed', content=Label(text='Could not register user'), size_hint=(None, None), size=(400, 400))
            popup.open()

class WindowManager(ScreenManager):
    db = ObjectProperty(None)

class MyApp(App):
    def build(self):
        self.db = DatabaseManager("hamburgueria")
        wm = WindowManager()
        wm.db = self.db
        wm.add_widget(LoginScreen(name='login'))
        wm.add_widget(MainScreen(name='main'))
        wm.add_widget(RegisterScreen(name='register'))
        return wm

if __name__ == "__main__":
    MyApp().run()

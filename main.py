from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.lang import Builder
import requests

Builder.load_file('login.kv')

class LoginScreen(Screen):
    def login(self):
        url = "http://127.0.0.1:5000/login"
        data = {
            "username": self.username.text,
            "senha": self.password.text
        }
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Login successful")
                self.manager.current = "main"
            else:
                print("Login failed")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

class MainScreen(Screen):
    pass

class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == "__main__":
    LoginApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

class ClienteApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Componentes da interface
        self.username_input = TextInput(hint_text='Nome de Usuário')
        self.password_input = TextInput(hint_text='Senha', password=True)
        login_button = Button(text='Login')
        login_button.bind(on_press=self.login)
        
        # Adicionando componentes ao layout
        layout.add_widget(Label(text='Login'))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        
        return layout
    
    def login(self, instance):
        # Lógica para enviar solicitação de login para o servidor Flask
        username = self.username_input.text
        password = self.password_input.text
        data = {'username': username, 'senha': password}
        response = requests.post('http://localhost:5000/login', json=data)
        
        if response.status_code == 200:
            # Login bem-sucedido
            access_token = response.json()['access_token']
            print('Login bem-sucedido. Token de acesso:', access_token)
        else:
            # Falha no login
            print('Falha no login. Mensagem:', response.json()['message'])

if __name__ == '__main__':
    ClienteApp().run()

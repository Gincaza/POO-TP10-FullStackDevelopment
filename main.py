from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
import requests
import json

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
                self.manager.current = 'main'
            else:
                print("Login failed")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

class MainScreen(Screen):
    def obter_clientes(self):
        """
        obtem a lista de clientes do servidor e atualiza o rótulo na tela de clientes.
        """
        url = "http://127.0.0.1:5000/cliente"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                clientes = response.json()

                # Format each client as a JSON string with indentation
                clientes_texto = "\n".join([json.dumps(cliente, indent=4) for cliente in clientes])
                
                # Update the label on the clientes screen
                self.manager.get_screen('clientes').clientes_label.text = clientes_texto
                
                # Switch to the clientes screen
                self.manager.current = 'clientes'
            else:
                print("Failed to obtain clients")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def adicionar_cliente(self):
        self.manager.current = 'adicionar_cliente'

    def obter_hamburgueres(self):
        url = "http://127.0.0.1:5000/hamburguer"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                hamburgueres = response.json()
                
                hamburgueres_texto = "\n".join([json.dumps(hamburguer, indent=4) for hamburguer in hamburgueres])

                self.manager.get_screen('hamburgueres').hamburgueres_label.text = hamburgueres_texto
                self.manager.current = 'hamburgueres'
            else:
                print("Failed to obtain hamburgers")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def registrar_pedido(self):
        self.manager.current = 'registrar_pedido'

class ClientesScreen(Screen):
    clientes_label = ObjectProperty(None)

class AdicionarClienteScreen(Screen):
    nome = ObjectProperty(None)
    morada = ObjectProperty(None)
    telefone = ObjectProperty(None)

    def voltar(self):
        self.manager.current = 'main'
    
    def adicionar(self):
        url = "http://127.0.0.1:5000/cliente"
        data = {
            "nome": self.nome.text,
            "morada": self.morada.text,
            "telefone": self.telefone.text
        }
    
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                print("Cliente adicionado com sucesso!")
                self.manager.current = 'main'
            else:
                print("Falha ao adicionar o cliente")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

class HamburgueresScreen(Screen):
    hamburgueres_label = ObjectProperty(None)

class RegistrarPedidoScreen(Screen):
    id_cliente = ObjectProperty(None)
    nome_hamburguer = ObjectProperty(None)
    quantidade = ObjectProperty(None)
    tamanho = ObjectProperty(None)
    valor_total = ObjectProperty(None)
    data_hora = ObjectProperty(None)

    def on_enter(self, *args):
        self.nome_hamburguer.values = self.get_hamburgueres()
    
    def get_hamburgueres(self):
        url = "http://127.0.0.1:5000/hamburguer"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                hamburgueres = response.json()
                # Retorna apenas os nomes dos hambúrgueres
                return [hamburguer['nome_hamburguer'] for hamburguer in hamburgueres]
            else:
                print("Falha ao obter hambúrgueres")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")
            return []

    def voltar(self):
        self.manager.current = 'main'
    
    def registrar(self):
        url = "http://127.0.0.1:5000/pedido"
        data = {
            "id_cliente": self.id_cliente.text,
            "nome_hamburguer": self.nome_hamburguer.text,
            "quantidade": self.quantidade.text,
            "tamanho": self.tamanho.text,
            "valor_total": self.valor_total.text,
            "data_hora": self.data_hora.text
        }
    
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                print("Pedido registrado com sucesso!")
                self.manager.current = 'main'
            else:
                print("Falha ao registrar o pedido")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ClientesScreen(name='clientes'))
        sm.add_widget(AdicionarClienteScreen(name='adicionar_cliente'))
        sm.add_widget(HamburgueresScreen(name='hamburgueres'))
        sm.add_widget(RegistrarPedidoScreen(name='registrar_pedido'))
        return sm

if __name__ == "__main__":
    LoginApp().run()

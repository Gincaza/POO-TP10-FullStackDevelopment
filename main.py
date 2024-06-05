from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
import requests
import json


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
    def ir_para_clientes(self):
        self.manager.current = 'clientes'

    def ir_para_hamburgueres(self):
        self.manager.current = 'hamburgueres'

    def ir_para_pedidos(self):
        self.manager.current = 'pedidos'


class ClientesScreen(Screen):
    def obter_clientes(self):
        self.manager.current = 'obter_clientes'

    def adicionar_cliente(self):
        self.manager.current = 'adicionar_cliente'


class AdicionarClienteScreen(Screen):
    nome = ObjectProperty(None)
    morada = ObjectProperty(None)
    telefone = ObjectProperty(None)

    def voltar(self):
        self.manager.current = 'clientes'

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
    def obter_hamburgueres(self):
        self.manager.current = 'obter_hamburgueres'


class PedidosScreen(Screen):
    def registrar_pedidos(self):
        self.manager.current = 'registrar_pedido'


class RegistrarPedidoScreen(Screen):
    id_cliente = ObjectProperty(None)
    nome_hamburguer = ObjectProperty(None)
    quantidade = ObjectProperty(None)
    tamanho = ObjectProperty(None)
    valor_total = ObjectProperty(None)
    data_hora = ObjectProperty(None)

    def on_enter(self, *args):
        self.nome_hamburguer.values = self.get_hamburgueres()
    
    def calcular_preco(self):
        preco_base = float(self.valor_total.text)

        if self.tamanho.text == "duplo":
            return preco_base * 2
        elif self.tamanho.text == "small":
            return preco_base * 0.8
        else:
            return preco_base
    
    def atualizar_preco(self, tamanho):
        preco_base = float(self.valor_total.text)

        if tamanho == "duplo":
            self.valor_total.text = str(preco_base * 2)
        elif tamanho == "small":
            self.valor_total.text = str(preco_base * 0.8)
        else:
            self.valor_total.text = str(preco_base)

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
        self.manager.current = 'pedidos'

    def registrar(self):
        url = "http://127.0.0.1:5000/pedido"
        data = {
            "id_cliente": self.id_cliente.text,
            "nome_hamburguer": self.nome_hamburguer.text,
            "quantidade": self.quantidade.text,
            "tamanho": self.tamanho.text,
            "valor_total": self.calcular_preco(),
            "data_hora": self.data_hora.text
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                print("Pedido registrado com sucesso!")
                self.manager.current = 'pedidos'
            else:
                print("Falha ao registrar o pedido")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


class ObterClientesScreen(Screen):
    clientes_label = ObjectProperty(None)

    def on_enter(self, *args):
        self.obter_clientes()

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
                clientes_texto = "\n".join([f"Nome: {cliente['nome']}, Morada: {cliente['morada']}, Telefone: {cliente['telefone']}" for cliente in clientes])

                # Update the label on the clientes screen
                self.clientes_label.text = clientes_texto
            else:
                print("Failed to obtain clients")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    
    def voltar(self):
        self.manager.current = 'clientes'

class ObterHamburgueresScreen(Screen):
    hamburgueres_label = ObjectProperty(None)

    def on_enter(self, *args):
        self.obter_hamburgueres()

    def obter_hamburgueres(self):
        """
        obtem a lista de hamburgueres do servidor e atualiza o rótulo na tela de hamburgueres.
        """
        url = "http://127.0.0.1:5000/hamburguer"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                hamburgueres = response.json()

                hamburgueres_texto = "\n".join([f"Nome: {hamburguer['nome_hamburguer']}, Ingredientes: {hamburguer['ingredientes']}, Preço: {hamburguer['preco_base']}" for hamburguer in hamburgueres])
            
                self.hamburgueres_label.text = hamburgueres_texto
            else:
                print("Failed to obtain hamburgueres")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    
    def voltar(self):
        self.manager.current = 'hamburgueres'

class InserirHamburguerScreen(Screen):
    nome_hamburguer = ObjectProperty(None)
    ingredientes = ObjectProperty(None)
    preco_base = ObjectProperty(None)

    def voltar(self):
        self.manager.current = 'hamburgueres'
    
    def inserir(self):
        url = "http://127.0.0.1:5000/hamburguer"
        data = {
            "nome_hamburguer": self.nome_hamburguer.text,
            "ingredientes": self.ingredientes.text,
            "preco_base": self.preco_base.text
        }
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                print("Hamburguer inserido com sucesso!")
                self.manager.current = 'hamburgueres'
            else:
                print("Falha ao inserir hamburguer")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


Builder.load_file('login.kv')


class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ClientesScreen(name='clientes'))
        sm.add_widget(HamburgueresScreen(name='hamburgueres'))
        sm.add_widget(PedidosScreen(name='pedidos'))
        sm.add_widget(AdicionarClienteScreen(name='adicionar_cliente'))
        sm.add_widget(ObterClientesScreen(name='obter_clientes'))
        sm.add_widget(RegistrarPedidoScreen(name='registrar_pedido'))
        sm.add_widget(ObterHamburgueresScreen(name='obter_hamburgueres'))
        sm.add_widget(InserirHamburguerScreen(name='inserir_hamburguer'))
        return sm


if __name__ == "__main__":
    LoginApp().run()

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
import requests
import json
from datetime import datetime
from operations import Operations


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
    
    def logout(self):
        self.manager.current = 'login'


class ClientesScreen(Screen):
    def obter_clientes(self):
        self.manager.current = 'obter_clientes'

    def adicionar_cliente(self):
        self.manager.current = 'adicionar_cliente'
    
    def deletar_cliente(self):
        self.manager.current = 'deletar_cliente'
    
    def voltar(self):
        self.manager.current = 'main'


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
                self.manager.current = 'clientes'
            else:
                print("Falha ao adicionar o cliente")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


class HamburgueresScreen(Screen):
    def obter_hamburgueres(self):
        self.manager.current = 'obter_hamburgueres'
    
    def inserir_hamburguer(self):
        self.manager.current = 'inserir_hamburguer'
    
    def deletar_hamburguer(self):
        self.manager.current = 'deletar_hamburguer'


class PedidosScreen(Screen):
    def registrar_pedidos(self):
        self.manager.current = 'registrar_pedido'


class RegistrarPedidoScreen(Screen):
    cliente = ObjectProperty(None)
    nome_hamburguer = ObjectProperty(None)
    quantidade = ObjectProperty(None)
    tamanho = ObjectProperty(None)

    def on_enter(self, *args):
        self.nome_hamburguer.values = Operations().get_hamburgueres()
        clientes = Operations().get_clientes()
        self.cliente.values = [(f"{cliente['nome']} (ID: {cliente['id_cliente']})") for cliente in clientes]

    def voltar(self):
        self.manager.current = 'pedidos'

    def registrar(self):
        url = "http://127.0.0.1:5000/pedido"
        cliente_selecionado = self.cliente.text
        nome_cliente, id_cliente = cliente_selecionado.split(" (ID: ")
        id_cliente = id_cliente[:-1]

        data = {
            "id_cliente": id_cliente,
            "nome_cliente": nome_cliente,
            "nome_hamburguer": self.nome_hamburguer.text,
            "quantidade": self.quantidade.text,
            "tamanho": self.tamanho.text,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        clientes = Operations().get_clientes()
        clientes_texto = "\n".join([f"Nome: {cliente['nome']}, Morada: {cliente['morada']}, Telefone: {cliente['telefone']}" for cliente in clientes])
        self.clientes_label.text = str(clientes_texto)
    
    def voltar(self):
        self.manager.current = 'clientes'

class DeletarClienteScreen(Screen):
    def voltar(self):
        self.manager.current = 'clientes'
    
    def deletar(self, id_cliente):
        url = f"http://127.0.0.1:5000/cliente"
        data = {"cliente_id": id_cliente}
        try:
            response = requests.delete(url, json=data)
            if response.status_code == 201:
                print("Cliente deletado com sucesso!")
                self.manager.current = 'clientes'
            else:
                print("Falha ao deletar o cliente")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

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

class DeleterHamburguerScreen(Screen):
    nome_hamburguer = ObjectProperty(None)

    def on_enter(self, *args):
        self.nome_hamburguer.values = self.get_hamburgueres()

    def voltar(self):
        self.manager.current = 'hamburgueres'
    
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
    
    def deletar(self):
        url = f"http://127.0.0.1:5000/hamburguer"
        data = {"nome_hamburguer": self.nome_hamburguer.text}
        try:
            response = requests.delete(url, json=data)
            if response.status_code == 201:
                print("Hamburguer deletado com sucesso!")
                self.manager.current = 'hamburgueres'
            else:
                print(f"Falha ao deletar o hamburguer: {response.text}")
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
        sm.add_widget(DeletarClienteScreen(name='deletar_cliente'))
        sm.add_widget(DeleterHamburguerScreen(name='deletar_hamburguer'))
        return sm


if __name__ == "__main__":
    LoginApp().run()



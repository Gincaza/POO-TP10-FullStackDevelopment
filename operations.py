import requests

class Operations:
    def __init__(self):
        pass

    def get_clientes(self):
        """
        obtem a lista de clientes e o retorna em array.
        """
        url = "http://127.0.0.1:5000/cliente"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                clientes = response.json()

                return clientes
            else:
                print("Failed to obtain clients")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    
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
    
    def get_pedidos(self):
        url = "http://127.0.0.1:5000/pedido"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pedidos = response.json()
                return pedidos
            else:
                print("Falha ao obter pedidos")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")
            return []
import unittest
from unittest.mock import patch
from app import app, database_context

class TestClienteRoute(unittest.TestCase):
    def setUp(self):
        # Configurar a aplicação para o modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'get_table')
    def test_obter_clientes_sucesso(self, mock_get_table):
        # Mocking a resposta do banco de dados
        mock_get_table.return_value = [
            (1, 'Cliente 1', 'Morada 1', '123456789'),
            (2, 'Cliente 2', 'Morada 2', '987654321')
        ]

        response = self.client.get('/cliente')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {
                "id_cliente": 1,
                "nome": "Cliente 1",
                "morada": "Morada 1",
                "telefone": "123456789",
            },
            {
                "id_cliente": 2,
                "nome": "Cliente 2",
                "morada": "Morada 2",
                "telefone": "987654321",
            }
        ])

    @patch.object(database_context, 'get_table')
    def test_obter_clientes_erro(self, mock_get_table):
        # Mocking uma exceção do banco de dados
        mock_get_table.side_effect = Exception("Erro ao acessar o banco de dados")

        response = self.client.get('/cliente')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "Erro ao acessar o banco de dados"})

class TestAtualizarClienteRoute(unittest.TestCase):
    def setUp(self):
        # Configurar a aplicação para o modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'update_cliente')
    @patch.object(database_context, 'get_cliente')
    def test_atualizar_cliente_sucesso(self, mock_get_cliente, mock_update_cliente):
        # Mocking a resposta do banco de dados
        mock_update_cliente.return_value = None  # update_cliente não retorna nada
        mock_get_cliente.return_value = (1, 'Cliente Atualizado', 'Nova Morada', '123456789')

        dados = {
            "id_cliente": 1,
            "nome": "Cliente Atualizado",
            "morada": "Nova Morada",
            "telefone": "123456789"
        }

        response = self.client.put('/cliente', json=dados)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            "mensagem": "Cliente atualizado com sucesso",
            "dados": {
                "id_cliente": 1,
                "nome": "Cliente Atualizado",
                "morada": "Nova Morada",
                "telefone": "123456789"
            }
        })

    @patch.object(database_context, 'update_cliente')
    def test_atualizar_cliente_erro_banco(self, mock_update_cliente):
        # Mocking uma exceção do banco de dados
        mock_update_cliente.side_effect = Exception("Erro ao atualizar o banco de dados")

        dados = {
            "id_cliente": 1,
            "nome": "Cliente Atualizado",
            "morada": "Nova Morada",
            "telefone": "123456789"
        }

        response = self.client.put('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "Erro ao atualizar o banco de dados"})

    def test_atualizar_cliente_faltando_id_cliente(self):
        dados = {
            "nome": "Cliente Atualizado",
            "morada": "Nova Morada",
            "telefone": "123456789"
        }

        response = self.client.put('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "id_cliente é necessário"})

    def test_atualizar_cliente_faltando_nome(self):
        dados = {
            "id_cliente": 1,
            "morada": "Nova Morada",
            "telefone": "123456789"
        }

        response = self.client.put('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "nome é necessário"})

    def test_atualizar_cliente_faltando_morada(self):
        dados = {
            "id_cliente": 1,
            "nome": "Cliente Atualizado",
            "telefone": "123456789"
        }

        response = self.client.put('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "morada é necessário"})

    def test_atualizar_cliente_faltando_telefone(self):
        dados = {
            "id_cliente": 1,
            "nome": "Cliente Atualizado",
            "morada": "Nova Morada"
        }

        response = self.client.put('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "telefone é necessário"})

class TestInserirClienteRoute(unittest.TestCase):
    def setUp(self):
        # Configurar a aplicação para o modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'insert_cliente')
    @patch.object(database_context, 'get_cliente')
    def test_inserir_cliente_sucesso(self, mock_get_cliente, mock_insert_cliente):
        # Mocking a resposta do banco de dados
        mock_insert_cliente.return_value = None  # insert_cliente não retorna nada
        mock_get_cliente.return_value = (1, 'Novo Cliente', 'Morada', '123456789')

        dados = {
            "nome": "Novo Cliente",
            "morada": "Morada",
            "telefone": "123456789"
        }

        response = self.client.post('/cliente', json=dados)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            "mensagem": "Cliente criado com sucesso!",
            "dados": {
                "id_cliente": 1,
                "nome": "Novo Cliente",
                "morada": "Morada",
                "telefone": "123456789"
            }
        })
if __name__ == '__main__':
    unittest.main()

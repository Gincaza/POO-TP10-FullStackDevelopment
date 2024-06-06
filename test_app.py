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

if __name__ == '__main__':
    unittest.main()

import unittest
from flask import Flask
from unittest.mock import patch
from app import app, database_context

class TestObterClientes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch.object(database_context, 'get_table')
    def test_obter_clientes_success(self, mock_get_table):
        mock_get_table.return_value = [
            (1, 'John Doe', '123 Main St', '123-456-7890'),
            (2, 'Jane Smith', '456 Elm St', '987-654-3210')
        ]

        response = self.app.get('/cliente')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {
                "id_cliente": 1,
                "nome": "John Doe",
                "morada": "123 Main St",
                "telefone": "123-456-7890"
            },
            {
                "id_cliente": 2,
                "nome": "Jane Smith",
                "morada": "456 Elm St",
                "telefone": "987-654-3210"
            }
        ])

    @patch.object(database_context, 'get_table')
    def test_obter_clientes_failure(self, mock_get_table):
        mock_get_table.side_effect = Exception('Database error')

        response = self.app.get('/cliente')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'erro': 'Database error'})

if __name__ == "__main__":
    unittest.main()
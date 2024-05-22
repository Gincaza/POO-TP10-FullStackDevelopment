import unittest
from app import app
import json

class TestAPIRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_get_cliente(self):
        response = self.client.get('/cliente')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_cliente_by_name(self):
        response = self.client.get('/cliente/nome/Ana')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn('id_cliente', data)
        self.assertIn('nome', data)
        self.assertIn('morada', data)
        self.assertIn('telefone', data)

    def test_get_cliente_by_telefone(self):
        response = self.client.get('/cliente/telefone/911234567')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn('id_cliente', data)
        self.assertIn('nome', data)
        self.assertIn('morada', data)
        self.assertIn('telefone', data)

    def test_get_hamburguer_table(self):
        response = self.client.get('/hamburguer')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
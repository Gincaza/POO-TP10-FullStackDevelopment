import unittest
from app import app
from databasemanager import DatabaseManager
import sqlite3

class FlaskTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.databasename = "teste"
        cls.database = DatabaseManager(cls.databasename)

    def setUp(self) -> None:
        self.app = app
        self.client = self.app.test_client()
        self.clear_database()
        self.database.populate_database()

    def clear_database(self):
        with sqlite3.connect(f"{self.databasename}.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes;")
            conn.commit()

    def test_get_clients_returns_table_clients(self):
        response = self.client.get("/cliente")
        self.assertEqual(response.status_code, 200)
    
    def test_get_cliente_by_name_returns_client(self):
        response = self.client.get('/cliente/Ana')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('id_cliente', data)
        self.assertIn('nome', data)
        self.assertIn('morada', data)
        self.assertIn('telefone', data)
    
    def test_get_cliente_by_telefone_returns_client(self):
        response = self.client.get('/cliente/911234567')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('id_cliente', data)
        self.assertIn('nome', data)
        self.assertIn('morada', data)
        self.assertIn('telefone', data)
    
    def test_update_client_request(self):
        # Dados de exemplo para atualização do cliente
        data = {
            "id_cliente": 1,
            "nome": "Novo Nome",
            "morada": "Nova Morada",
            "telefone": "911234567"
        }
        
        # Envia uma solicitação PUT para atualizar o cliente
        response = self.app.put('/cliente', json=data)
        data = response.get_json()
        
        # Verifica se o status code é 200 (OK) e se a mensagem de sucesso está presente
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Cliente atualizado com sucesso')

        # Verifica se os dados do cliente foram atualizados corretamente
        self.assertIn('data', data)
        self.assertIn('id_cliente', data['data'])
        self.assertIn('nome', data['data'])
        self.assertIn('morada', data['data'])
        self.assertIn('telefone', data['data'])
        self.assertEqual(data['data']['nome'], 'Novo Nome')
        self.assertEqual(data['data']['morada'], 'Nova Morada')
        self.assertEqual(data['data']['telefone'], '911234567')

if __name__ == "__main__":
    unittest.main()

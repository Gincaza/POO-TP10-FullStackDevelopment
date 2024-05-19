import unittest
from databasemanager import DatabaseManager

class DatabaseManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.database = DatabaseManager("teste")
        # Limpar a tabela de clientes antes de cada teste
    
    def test_insert_cliente_returns_rows_clients(self):
        # Configurar um cliente
        self.database.insert_cliente("Gustavo", "Faro", 913528755)
        # Executar o método que está sendo testado
        clients = self.database.get_table("clientes")
        # Verificar se o resultado está conforme o esperado
        self.assertEqual(clients, [(1, "Gustavo", "Faro", "913528755")])
    


if __name__ == "__main__":
    unittest.main()
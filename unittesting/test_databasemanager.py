import unittest
from databasemockmanager import DatabaseManager


class DatabaseManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.database = DatabaseManager("teste")
        # Limpar a tabela de clientes antes de cada teste

    def test_insert_table_clients_returns_rows_clients(self):
        # Configurar um cliente
        self.database.insert_table_clientes("Gustavo", "Faro", 913528755)
        # Executar o método que está sendo testado
        clients = self.database.get_table("clientes")
        # Verificar se o resultado está conforme o esperado
        self.assertEqual(clients, [(1, "Gustavo", "Faro", "913528755")])

    def test_get_cliente_id_returns_client_id(self):
        #set up
        self.database.insert_table_clientes("Gustavo", "Faro", 555)

        client_id = self.database.get_cliente_id("Gustavo")

        self.assertEqual(client_id, 1)

    def test_update_table_client_returns_cliente(self):
        #set up
        self.database.insert_table_clientes("Gustavo", "Faro", 555)

        #act
        self.database.update_table_client(1, "Pedro", "Quarteira", 666)

        clientes = self.database.get_table("clientes")
        #Assert
        self.assertEqual([(1, "Pedro", "Quarteira", "666")], clientes)
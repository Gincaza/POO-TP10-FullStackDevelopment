import unittest
import os
import sqlite3
from databasemanager import DatabaseManager

class DatabaseManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None: # Definindo o objeto uma vez
        cls.databasename = "teste"
        cls.database = DatabaseManager(cls.databasename)

    def setUp(self) -> None:
        self.clear_database()

    def clear_database(self): # Limpar DB toda vez que um teste for executado
        with sqlite3.connect(f"{self.databasename}.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes;")
            conn.commit()

    def test_insert_cliente_returns_rows_clients(self):
        # Configurar um cliente
        self.database.insert_cliente("Gustavo", "Faro", "913528755")
        # Executar
        clients = self.database.get_table("clientes")
        # Assert
        self.assertEqual(clients, [(1, "Gustavo", "Faro", "913528755")])

    def test_get_cliente_by_telefone_returns_client(self):
        # Configurar um cliente
        self.database.insert_cliente("Pedro", "Quarteira", "12345")
        # Execute
        cliente = self.database.get_cliente_by_telefone("12345")
        # Assert
        self.assertEqual(cliente, (1, "Pedro", "Quarteira", "12345"))
    
    def test_get_client_by_name_returns_client(self):
        #Set up
        self.database.insert_cliente("Gustavo", "Faro", "996613332")
        #Executar
        cliente = self.database.get_cliente_by_nome("Gustavo")
        #Assert
        self.assertEqual(cliente, (1, "Gustavo", "Faro", "996613332"))

if __name__ == "__main__":
    unittest.main()

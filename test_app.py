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

if __name__ == "__main__":
    unittest.main()

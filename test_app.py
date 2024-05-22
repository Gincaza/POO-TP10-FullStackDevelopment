import unittest
from app import app
import json


class TestAPIRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_get_cliente(self):
        response = self.client.get("/cliente")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_cliente_by_name(self):
        response = self.client.get("/cliente/nome/Ana")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn("id_cliente", data)
        self.assertIn("nome", data)
        self.assertIn("morada", data)
        self.assertIn("telefone", data)

    def test_get_cliente_by_telefone(self):
        response = self.client.get("/cliente/telefone/911234567")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn("id_cliente", data)
        self.assertIn("nome", data)
        self.assertIn("morada", data)
        self.assertIn("telefone", data)

    def test_get_hamburguer_table(self):
        response = self.client.get("/hamburguer")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_inserir_hamburguer(self):
        # setUp
        dados = {
            "nome_hamburguer": "CheeseGood",
            "ingredientes": "queijo molho especial",
        }
        # act
        request = self.client.post("/hamburguer", json=dados)
        # assert
        self.assertEqual(request.status_code, 201)
        self.assertIn("Hamburguer inserido com sucesso!", request.json["message"])
        # assert se os dados estão corretos
        dados_cliente = request.json["dados"]
        self.assertEqual(dados_cliente["nome_hamburguer"], dados["nome_hamburguer"])
        self.assertEqual(dados_cliente["ingredientes"], dados["ingredientes"])

    def test_login(self):
        # setUp
        dados = {"username": "mothnue", "senha": "password123!"}
        # act
        response = self.client.post("/login", json=dados)
        # assert
        self.assertEqual(200, response.status_code)
        self.assertIn("Usuário autenticado!", response.json["message"])

    def test_register(self):
        # set Up
        dados = {"nome": "Pedro", "username": "joker", "senha": "password123"}
        # act
        response = self.client.post("/register", json=dados)
        # assert
        self.assertEqual(201, response.status_code)
        self.assertIn("Registrado com sucesso!", response.json["message"])


if __name__ == "__main__":
    unittest.main()

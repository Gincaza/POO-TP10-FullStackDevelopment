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

    def test_inserir_cliente_faltando_nome(self):
        dados = {
            "morada": "Morada",
            "telefone": "123456789"
        }

        response = self.client.post('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "nome é necessário"})

    def test_inserir_cliente_faltando_morada(self):
        dados = {
            "nome": "Novo Cliente",
            "telefone": "123456789"
        }

        response = self.client.post('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "morada é necessário"})

    def test_inserir_cliente_faltando_telefone(self):
        dados = {
            "nome": "Novo Cliente",
            "morada": "Morada"
        }

        response = self.client.post('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "telefone é necessário"})

class TestDeletarClienteRoute(unittest.TestCase):
    def setUp(self):
        # Configurar a aplicação para o modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'get_cliente')
    @patch.object(database_context, 'delete_cliente')
    def test_deletar_cliente_sucesso(self, mock_delete_cliente, mock_get_cliente):
        # Mocking a resposta do banco de dados
        mock_get_cliente.return_value = (1, 'Cliente Deletado', 'Morada', '123456789')

        dados = {
            "cliente_id": 1
        }

        response = self.client.delete('/cliente', json=dados)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            "mensagem": "Cliente deletado com sucesso!",
            "dados": {
                "id_cliente": 1,
                "nome": "Cliente Deletado",
                "morada": "Morada",
                "telefone": "123456789"
            }
        })

    @patch.object(database_context, 'get_cliente')
    def test_deletar_cliente_nao_encontrado(self, mock_get_cliente):
        # Mocking que o cliente não é encontrado
        mock_get_cliente.return_value = None

        dados = {
            "cliente_id": 1
        }

        response = self.client.delete('/cliente', json=dados)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"erro": "Cliente não encontrado"})

    def test_deletar_cliente_sem_cliente_id(self):
        dados = {}

        response = self.client.delete('/cliente', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "id_cliente é necessário"})

class TestObterTabelaHamburguerRoute(unittest.TestCase):
    def setUp(self):
        # Configurar a aplicação para o modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'get_table')
    def test_obter_tabela_hamburguer_sucesso(self, mock_get_table):
        # Mocking a resposta do banco de dados
        mock_get_table.return_value = [
            ('Hamburguer 1', 'Ingredientes 1', 10.99),
            ('Hamburguer 2', 'Ingredientes 2', 12.99)
        ]

        response = self.client.get('/hamburguer')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {
                "nome_hamburguer": "Hamburguer 1",
                "ingredientes": "Ingredientes 1",
                "preco_base": 10.99
            },
            {
                "nome_hamburguer": "Hamburguer 2",
                "ingredientes": "Ingredientes 2",
                "preco_base": 12.99
            }
        ])
    
    @patch.object(database_context, 'get_table')
    def test_obter_tabela_hamburguer_linha_vazia(self, mock_get_table):
        # Mocking uma linha vazia no banco de dados
        mock_get_table.return_value = [
            ('Hamburguer 1', None, 10.99),
            ('Hamburguer 2', 'Ingredientes 2', None)
        ]
      
        response = self.client.get('/hamburguer')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "Linha vazia encontrada na tabela de hambúrgueres"})

    @patch.object(database_context, 'get_table')
    def test_obter_tabela_hamburguer_linha_menos_de_3_colunas(self, mock_get_table):
        # Mocking uma linha com menos de 3 colunas no banco de dados
        mock_get_table.return_value = [
            ('Hamburguer 1', 'Ingredientes 1'),
            ('Hamburguer 2',)
        ]

        response = self.client.get('/hamburguer')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "Linha da tabela de hambúrgueres com menos de 3 colunas"})

class TestInserirHamburguerRoute(unittest.TestCase):
    def setUp(self):
        # Configurar a aplicação para o modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'insert_hamburguer')
    @patch.object(database_context, 'get_hamburguer')
    def test_inserir_hamburguer_sucesso(self, mock_get_hamburguer, mock_insert_hamburguer):
        # Mocking a resposta do banco de dados
        mock_insert_hamburguer.return_value = None  # insert_hamburguer não retorna nada
        mock_get_hamburguer.return_value = ('Novo Hamburguer', 'Ingredientes', 15.99)

        dados = {
            "nome_hamburguer": "Novo Hamburguer",
            "ingredientes": "Ingredientes",
            "preco_base": 15.99
        }

        response = self.client.post('/hamburguer', json=dados)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            "message": "Hamburguer inserido com sucesso!",
            "dados": {
                "nome_hamburguer": "Novo Hamburguer",
                "ingredientes": "Ingredientes",
                "preco_base": 15.99
            }
        })

    def test_inserir_hamburguer_dados_incompletos(self):
        dados = {
            "nome_hamburguer": "Novo Hamburguer",
            "ingredientes": "Ingredientes"
            # Preço base faltando
        }

        response = self.client.post('/hamburguer', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Dados incompletos"})

class TestDeletarHamburguerRoute(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'get_hamburguer')
    @patch.object(database_context, 'delete_hamburguer')
    def test_deletar_hamburguer_sucesso(self, mock_delete_hamburguer, mock_get_hamburguer):
        # Mocking a resposta do banco de dados
        mock_get_hamburguer.return_value = ('Hamburguer Deletado', 'Ingredientes', 10.99)

        dados = {
            "nome_hamburguer": "Hamburguer Deletado"
        }

        response = self.client.delete('/hamburguer', json=dados)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            "mensagem": "Hamburguer deletado com sucesso!",
            "dados": {
                "nome_hamburguer": "Hamburguer Deletado",
                "ingredientes": "Ingredientes"
            }
        })
        mock_delete_hamburguer.assert_called_once_with("Hamburguer Deletado")

    @patch.object(database_context, 'get_hamburguer')
    def test_deletar_hamburguer_nao_encontrado(self, mock_get_hamburguer):
        # Mocking que o hamburguer não é encontrado
        mock_get_hamburguer.return_value = None

        dados = {
            "nome_hamburguer": "Hamburguer Inexistente"
        }

        response = self.client.delete('/hamburguer', json=dados)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"erro": "Hamburguer não encontrado"})

    def test_deletar_hamburguer_sem_nome(self):
        dados = {}

        response = self.client.delete('/hamburguer', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "Nome do hamburguer não fornecido"})

class TestLoginRoute(unittest.TestCase):
    def setUp(self):
        # Configurar a aplicação para o modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'verify_empregado')
    def test_login_sucesso(self, mock_verify_empregado):
        # Mocking a resposta de verificação do banco de dados
        mock_verify_empregado.return_value = True

        dados = {
            "username": "usuario_teste",
            "senha": "senha_teste"
        }

        response = self.client.post('/login', json=dados)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Usuário autenticado!"})

    @patch.object(database_context, 'verify_empregado')
    def test_login_falha(self, mock_verify_empregado):
        # Mocking a resposta de verificação do banco de dados
        mock_verify_empregado.return_value = False

        dados = {
            "username": "usuario_teste",
            "senha": "senha_errada"
        }

        response = self.client.post('/login', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"message": "Não conseguiu se logar!"})

    def test_login_dados_incompletos(self):
        dados = {
            "username": "usuario_teste"
            # Senha faltando
        }

        response = self.client.post('/login', json=dados)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"erro": "Username e senha são obrigatórios"})

class TestRegisterRoute(unittest.TestCase):
    def setUp(self):
        # Configurar a aplicação para o modo de teste
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch.object(database_context, 'get_empregado')
    @patch.object(database_context, 'insert_empregado')
    @patch.object(database_context, 'verify_empregado')
    def test_register_sucesso(self, mock_verify_empregado, mock_insert_empregado, mock_get_empregado):
        # Mocking as respostas do banco de dados
        mock_get_empregado.return_value = None  # Nome de usuário não está em uso
        mock_verify_empregado.return_value = True  # Verificação de sucesso após inserção

        dados = {
            "nome": "Usuario Teste",
            "username": "usuario_teste",
            "senha": "senha_teste"
        }

        response = self.client.post('/register', json=dados)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "Registrado com sucesso!"})
if __name__ == '__main__':
    unittest.main()

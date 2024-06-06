import sqlite3
from datetime import datetime
from contextlib import closing
import bcrypt

class DatabaseManager:
    @staticmethod
    def create_database(databasename):
        try:
            with sqlite3.connect(f"{databasename}.db") as conn:
                sql = """
                    CREATE TABLE IF NOT EXISTS clientes (
                        id_cliente INTEGER PRIMARY KEY,
                        nome TEXT,
                        morada TEXT,
                        telefone TEXT UNIQUE
                    );

                    CREATE TABLE IF NOT EXISTS hamburgueres (
                        nome_hamburguer TEXT PRIMARY KEY,
                        ingredientes TEXT,
                        preco_base REAL
                    );

                    CREATE TABLE IF NOT EXISTS pedidos (
                        id_pedido INTEGER PRIMARY KEY,
                        id_cliente INTEGER,
                        nome_cliente TEXT,
                        nome_hamburguer TEXT,
                        quantidade INTEGER,
                        tamanho TEXT,
                        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                        valor_total REAL,
                        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                        FOREIGN KEY (nome_cliente) REFERENCES clientes(nome),
                        FOREIGN KEY (nome_hamburguer) REFERENCES hamburgueres(nome_hamburguer)
                    );

                    CREATE TABLE IF NOT EXISTS empregados (
                        id_empregado INTEGER PRIMARY KEY,
                        nome TEXT,
                        username TEXT UNIQUE,
                        senha TEXT
                    );
                    """
                with closing(conn.cursor()) as cursor:
                    cursor.executescript(sql)
        except sqlite3.Error as e:
            raise Exception(f"Erro ao criar banco de dados: {e}")

    def __init__(self, databasename):
        self.__databasename = databasename
        self.create_database(databasename)

    # Empregados
    def insert_empregado(self, nome, username, senha):
        hashed_senha = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "INSERT INTO empregados (nome, username, senha) VALUES (?, ?, ?);"
                cursor = conn.cursor()
                cursor.execute(sql, (nome, username, hashed_senha))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao inserir empregado: {e}")

    def verify_empregado(self, username, senha):
        if not username or not senha:
            raise ValueError("Username e senha devem ser fornecidos")

        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "SELECT senha FROM empregados WHERE username = ?"
                cursor = conn.cursor()
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(senha.encode("utf-8"), result[0]):
                    return True
                else:
                    return False
        except sqlite3.Error as e:
            raise Exception(f"Erro ao verificar empregado: {e}")

    def get_empregado(self, username):
        if not username:
            raise ValueError("Username deve ser fornecido")

        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM empregados WHERE username = ?"
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                return result
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar empregado: {e}")


    # Clientes
    def insert_cliente(self, nome, morada, telefone):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "INSERT INTO clientes (nome, morada, telefone) VALUES (?, ?, ?);"
                cursor = conn.cursor()
                cursor.execute(sql, (nome, morada, telefone))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao inserir cliente: {e}")

    def get_cliente(self, id_cliente=None, nome=None, telefone=None):
        try:
            if not id_cliente and not nome and not telefone:
                raise ValueError(
                    "Pelo menos um critério de busca (id_cliente, nome ou telefone) deve ser fornecido"
                )

            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()

                if id_cliente:
                    query = "SELECT * FROM clientes WHERE id_cliente = ?"
                    cursor.execute(query, (id_cliente,))
                elif nome and telefone:
                    query = "SELECT * FROM clientes WHERE nome = ? AND telefone = ?"
                    cursor.execute(query, (nome, telefone))
                elif nome:
                    query = "SELECT * FROM clientes WHERE nome = ?"
                    cursor.execute(query, (nome,))
                elif telefone:
                    query = "SELECT * FROM clientes WHERE telefone = ?"
                    cursor.execute(query, (telefone,))

                result = cursor.fetchone()
                if result:
                    return result
                else:
                    raise Exception("Nenhum resultado encontrado para o cliente")
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar cliente: {e}")

    def update_cliente(self, id_cliente, nome, morada, telefone):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "UPDATE clientes SET nome = ?, morada = ?, telefone = ? WHERE id_cliente = ?;"
                cursor = conn.cursor()
                cursor.execute(sql, (nome, morada, telefone, id_cliente))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao atualizar cliente: {e}")

    def delete_cliente(self, id_cliente):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "DELETE FROM clientes WHERE id_cliente = ?;"
                cursor = conn.cursor()
                cursor.execute(sql, (id_cliente,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao deletar cliente: {e}")

    # Hamburguers
    def insert_hamburguer(self, nome_hamburguer, ingredientes, preco_base):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "INSERT INTO hamburgueres (nome_hamburguer, ingredientes, preco_base) VALUES (?, ?, ?);"
                cursor = conn.cursor()
                cursor.execute(sql, (nome_hamburguer, ingredientes, preco_base))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao inserir hamburguer: {e}")
            raise Exception(f"Erro ao inserir hamburguer: {e}")

    def get_hamburguer(self, nome_hamburguer=None, ingredientes=None):
        try:
            if nome_hamburguer is None and ingredientes is None:
                raise ValueError("Pelo menos um critério de busca (nome_hamburguer ou ingredientes) deve ser fornecido")

            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()

                if nome_hamburguer:
                    query = "SELECT * FROM hamburgueres WHERE nome_hamburguer = ?"
                    params = (nome_hamburguer,)
                elif ingredientes:
                    query = "SELECT * FROM hamburgueres WHERE ingredientes = ?"
                    params = (ingredientes,)

                cursor.execute(query, params)
                result = cursor.fetchone()

                if result:
                    return result
                else:
                    raise Exception("Nenhum resultado encontrado para o hamburguer fornecido")
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar hamburguer: {e}")

    def delete_hamburguer(self, nome_hamburguer):
        if not nome_hamburguer:
            raise ValueError("Nome do hamburguer não fornecido")

        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "DELETE FROM hamburgueres WHERE nome_hamburguer = ?;"
                cursor = conn.cursor()
                cursor.execute(sql, (nome_hamburguer,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao deletar hamburguer: {e}")

    # Pedidos
    def insert_pedido(self, id_cliente, nome_cliente, nome_hamburguer, quantidade, tamanho, valor_total, data_hora=None):
        try:
            if not id_cliente:
                raise ValueError("Id do cliente não fornecido")
            if not nome_hamburguer:
                raise ValueError("Nome do hamburguer não fornecido")
            if not quantidade:
                raise ValueError("Quantidade não fornecida")
            if not tamanho:
                raise ValueError("Tamanho não fornecido")
            if not valor_total:
                raise ValueError("Valor total não fornecido")

            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = "INSERT INTO pedidos (id_cliente, nome_cliente, nome_hamburguer, quantidade, tamanho, data_hora, valor_total) VALUES (?, ?, ?, ?, ?, ?, ?);"
                cursor.execute(sql, (id_cliente, nome_cliente, nome_hamburguer, quantidade, tamanho, data_hora if data_hora else datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor_total))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Erro ao inserir pedido: {e}")

    # Utilitários
    def get_table(self, table):
        if not table:
            raise ValueError("Nome da tabela não fornecido")
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                return rows
        except sqlite3.Error as e:
            raise Exception(f"Error procurando a tabela {table}: {e}")

    def populate_database(self):
        try:
            clients = [
                ("Ana", "Lisboa", "911234567"),
                ("Bruno", "Porto", "912345678"),
                ("Carla", "Coimbra", "913456789")
            ]
            burgers = [
                ("Cheeseburger", "Bread, Meat, Cheese, Lettuce, Tomato", 12.50),
                ("Bacon Burger", "Bread, Meat, Bacon, Cheese, BBQ Sauce", 8.75),
                ("Veggie Burger", "Bread, Veggie Burger, Lettuce, Tomato, Special Sauce", 15.00)
            ]

            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                for client in clients:
                    self.insert_cliente(*client)
                for burger in burgers:
                    self.insert_hamburguer(*burger)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.insert_empregado("Gustavo Cruz", "mothnue", "password123!")
                cursor.close()
            print("Banco de dados populado com sucesso.")
        except sqlite3.Error as e:
            raise Exception(f"Erro ao popular banco de dados: {e}")

if __name__ == "__main__":
    databaseContext = DatabaseManager("hamburgueria")

    # Populando o banco de dados
    databaseContext.populate_database()

    # Testando a recuperação de todos os clientes
    rows = databaseContext.get_table("clientes")
    for row in rows:
        print(row)

    # Testando a recuperação de todos os hambúrgueres
    rows = databaseContext.get_table("hamburgueres")
    for row in rows:
        print(row)

    # Testando a recuperação de todos os pedidos
    rows = databaseContext.get_table("pedidos")
    for row in rows:
        print(row)

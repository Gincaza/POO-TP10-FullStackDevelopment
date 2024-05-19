import sqlite3
import os

class DatabaseManager:
    @staticmethod
    def create_database(databasename):
        try:
            with sqlite3.connect(f"{databasename}.db") as conn:
                sql = """
                    CREATE TABLE IF NOT EXISTS 
                    clientes (
                        id_cliente INTEGER PRIMARY KEY,
                        nome TEXT,
                        morada TEXT,
                        telefone TEXT UNIQUE
                    );

                    CREATE TABLE IF NOT EXISTS 
                    hamburgueres (
                        nome_hamburguer TEXT PRIMARY KEY,
                        ingredientes TEXT
                    );

                    CREATE TABLE IF NOT EXISTS 
                    pedidos (
                        id_pedido INTEGER PRIMARY KEY,
                        id_cliente INTEGER,
                        nome_hamburguer TEXT,
                        quantidade INTEGER,
                        tamanho TEXT,
                        data_hora DATETIME,
                        valor_total REAL,
                        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                        FOREIGN KEY (nome_hamburguer) REFERENCES hamburgueres(nome_hamburguer)
                    );
                    """
                cursor = conn.cursor()
                cursor.executescript(sql)
        except sqlite3.Error as e:
            print(f"Ocorreu um erro ao criar o banco de dados: {e}")

    def __init__(self, databasename) -> None:
        self.__databasename = databasename
        self.create_database(databasename)

    def insert_cliente(self, nome, morada, telefone):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = """
                    INSERT INTO clientes (nome, morada, telefone) VALUES (?, ?, ?);
                    """
                cursor = conn.cursor()
                cursor.execute(sql, (nome, morada, telefone))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao inserir cliente: {e}")
    
    def get_cliente_by_telefone(self, telefone):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = "SELECT * FROM clientes WHERE telefone = ?;"
                cursor.execute(sql, (telefone,))
                result = cursor.fetchone()
                if result is None:
                    raise Exception("Nenhum resultado encontrado para o telefone fornecido.")
                return result
        except sqlite3.Error as e:
            print(f"Erro ao buscar cliente: {e}")

    def get_cliente_by_nome(self, nome):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = "SELECT * FROM clientes WHERE nome = ?;"
                cursor.execute(sql, (nome,))
                result = cursor.fetchone()
                return result
        except sqlite3.Error as e:
            print(f"Erro ao buscar cliente: {e}")
    
    def update_cliente(self, id_cliente, nome, morada, telefone):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = """
                    UPDATE clientes
                    SET nome = ?, morada = ?, telefone = ?
                    WHERE id_cliente = ?;
                    """
                cursor.execute(sql, (nome, morada, telefone, id_cliente))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao atualizar cliente: {e}")

    def insert_hamburguer(self, nome_hamburguer, ingredientes):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = """
                    INSERT INTO hamburgueres (nome_hamburguer, ingredientes) VALUES (?, ?);
                    """
                cursor.execute(sql, (nome_hamburguer, ingredientes))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao inserir hambúrguer: {e}")

    def get_table(self, table):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                return rows
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar a tabela Clientes: {str(e)}")

    def delete_cliente(self, id_cliente):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = "DELETE FROM clientes WHERE id_cliente = ?;"
                cursor.execute(sql, (id_cliente,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao deletar cliente: {e}")
    



if __name__ == "__main__":
    databaseContext = DatabaseManager("teste")

    databaseContext.insert_table_clientes("Gustavo", "Faro", 913528755)
    rows = databaseContext.get_all_table_clients()

    for row in rows:
        print(row)
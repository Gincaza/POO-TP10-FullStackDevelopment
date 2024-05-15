import sqlite3
import os

class DatabaseManager:
    @staticmethod
    def create_database(databasename):
        try:
            with sqlite3.connect(f"{databasename}.db") as conn:
                sql = """
                    CREATE TABLE clientes (
                        id_cliente INTEGER PRIMARY KEY,
                        nome TEXT,
                        morada TEXT,
                        telefone TEXT
                    );

                    CREATE TABLE ingredientes (
                        id_ingrediente INTEGER PRIMARY KEY,
                        nome TEXT
                    );

                    CREATE TABLE hamburgueres (
                        id_hamburguer INTEGER PRIMARY KEY,
                        nome_hamburguer TEXT,
                        preco REAL,
                        disponivel BOOLEAN
                    );

                    CREATE TABLE hamburgueres_ingredientes (
                        id_hamburguer INTEGER,
                        id_ingrediente INTEGER,
                        quantidade INTEGER,
                        FOREIGN KEY (id_hamburguer) REFERENCES hamburgueres(id_hamburguer),
                        FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente)
                    );

                    CREATE TABLE pedidos (
                        id_pedido INTEGER PRIMARY KEY,
                        id_cliente INTEGER,
                        id_hamburguer INTEGER,
                        quantidade INTEGER,
                        tamanho TEXT,
                        data_hora DATETIME,
                        valor_total REAL,
                        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                        FOREIGN KEY (id_hamburguer) REFERENCES hamburgueres(id_hamburguer)
                    );
                    """
                cursor = conn.cursor()
                cursor.executescript(sql)
        except sqlite3.Error as e:
            print(f"Ocorreu um erro ao criar o banco de dados: {e}")

    def __init__(self, databasename) -> None:
        self.__databasename = databasename
        self.create_database(databasename)



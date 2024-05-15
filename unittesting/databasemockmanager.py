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
                        telefone TEXT
                    );

                    CREATE TABLE IF NOT EXISTS 
                    ingredientes (
                        id_ingrediente INTEGER PRIMARY KEY,
                        nome TEXT
                    );

                    CREATE TABLE IF NOT EXISTS  
                    hamburgueres (
                        id_hamburguer INTEGER PRIMARY KEY,
                        nome_hamburguer TEXT,
                        preco REAL,
                        disponivel BOOLEAN
                    );

                    CREATE TABLE IF NOT EXISTS 
                    hamburgueres_ingredientes (
                        id_hamburguer INTEGER,
                        id_ingrediente INTEGER,
                        quantidade INTEGER,
                        FOREIGN KEY (id_hamburguer) REFERENCES hamburgueres(id_hamburguer),
                        FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente)
                    );

                    CREATE TABLE IF NOT EXISTS 
                    pedidos (
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

    def insert_table_clientes(self, nome, morada, telefone):
        with sqlite3.connect(f"{self.__databasename}.db") as conn:
            sql = """
                INSERT INTO clientes(nome, morada, telefone) VALUES(?, ?, ?);
                """
            cursor = conn.cursor()
            cursor.execute(sql, (nome, morada, telefone))
    
    def get_all_table_clients(self):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM clientes")
                rows = cursor.fetchall()
                return rows
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar a tabela Clientes: {str(e)}")

    def get_cliente_id(self, name):
        with sqlite3.connect(f"{self.__databasename}.db") as conn:
            cursor = conn.cursor()

            sql = "SELECT id_cliente FROM clientes WHERE nome = ?;"

            cursor.execute(sql, (name,))
            result = cursor.fetchone()
            if result is None:
                raise Exception("Nenhum resultado encontrado para o nome fornecido.")
            return result[0]

    def insert_sensor(self, location_name, sensor_name, unit):
        try:
            idLocation = self.get_location_id(location_name)
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()

                sql = """
                    INSERT INTO Sensor(idLocation, name, unit) VALUES(?, ?, ?);
                    """

                cursor.execute(sql, (idLocation, sensor_name, unit))

        except sqlite3.Error as e:
            raise Exception(f"Erro ao inserir o sensor: {str(e)}")

    def get_all_table_sensor(self):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Sensor")
                rows = cursor.fetchall()
                return rows
        except sqlite3.Error as e:
            raise Exception(f"Erro ao buscar a tabela Sensor: {str(e)}")

    def update_table_sensor(self, sensor_id, name, unit):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = """
                    UPDATE Sensor 
                    SET name = ?, unit = ? 
                    WHERE idSensor = ?;
                    """
                cursor.execute(sql, (name, unit, sensor_id))
        except sqlite3.Error as e:
            raise Exception(f"Erro ao atualizar o sensor: {str(e)}")

    def delete_table_sensor(self, sensor_id):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = """DELETE FROM Sensor WHERE idSensor = ?;"""

                cursor.execute(sql, (sensor_id,))
        except sqlite3.Error as e:
            raise Exception(f"Erro ao deletar: {str(e)}")
    
    def __del__(self):
        os.remove(f"{self.__databasename}.db")



if __name__ == "__main__":
    databaseContext = DatabaseManager("teste")

    databaseContext.insert_table_clientes("Gustavo", "Faro", 913528755)
    rows = databaseContext.get_all_table_clients()

    for row in rows:
        print(row)

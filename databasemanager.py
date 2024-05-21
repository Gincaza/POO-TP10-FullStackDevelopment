import sqlite3
from datetime import datetime


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

    def get_cliente(self, nome=None, telefone=None):
        try:
            if not nome and not telefone:
                raise ValueError(
                    "Pelo menos um critério de busca (nome ou telefone) deve ser fornecido"
                )

            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()

                if nome and telefone:
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
            return str(e)

    def get_cliente_by_telefone(self, telefone):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = "SELECT * FROM clientes WHERE telefone = ?;"
                cursor.execute(sql, (telefone,))
                result = cursor.fetchone()
                if result is None:
                    raise Exception(
                        "Nenhum resultado encontrado para o telefone fornecido."
                    )
                return result
        except sqlite3.Error as e:
            print(f"Erro ao buscar cliente: {e}")
            return None  # Garante que a função retorne um valor

    def get_cliente_by_nome(self, nome):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = "SELECT * FROM clientes WHERE nome = ?;"
                cursor.execute(sql, (nome,))
                result = cursor.fetchone()
                if result is None:
                    raise Exception(
                        "Nenhum resultado encontrado para o cliente fornecido."
                    )
                return result
        except sqlite3.Error as e:
            print(f"Erro ao buscar cliente: {e}")
            return None

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

    def insert_pedido(
        self, id_cliente, nome_hamburguer, quantidade, tamanho, data_hora, valor_total
    ):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = """
                    INSERT INTO pedidos (id_cliente, nome_hamburguer, quantidade, tamanho, data_hora, valor_total) 
                    VALUES (?, ?, ?, ?, ?, ?);
                    """
                cursor.execute(
                    sql,
                    (
                        id_cliente,
                        nome_hamburguer,
                        quantidade,
                        tamanho,
                        data_hora,
                        valor_total,
                    ),
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao inserir pedido: {e}")

    def get_table(self, table):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                return rows
        except sqlite3.Error as e:
            print(f"Erro ao buscar a tabela {table}: {e}")

    def delete_cliente(self, id_cliente):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = "DELETE FROM clientes WHERE id_cliente = ?;"
                cursor.execute(sql, (id_cliente,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao deletar cliente: {e}")

    def delete_hamburguer(self, nome_hamburguer):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                cursor = conn.cursor()
                sql = "DELETE FROM hamburgueres WHERE nome_hamburguer = ?;"
                cursor.execute(sql, (nome_hamburguer,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao deletar hambúrguer: {e}")

    def populate_database(self):
        try:
            self.insert_cliente("Ana", "Lisboa", "911234567")
            self.insert_cliente("Bruno", "Porto", "912345678")
            self.insert_cliente("Carla", "Coimbra", "913456789")

            self.insert_hamburguer("Cheeseburger", "Pão, Carne, Queijo, Alface, Tomate")
            self.insert_hamburguer(
                "Bacon Burger", "Pão, Carne, Bacon, Queijo, Molho BBQ"
            )
            self.insert_hamburguer(
                "Veggie Burger",
                "Pão, Hambúrguer Vegetal, Alface, Tomate, Molho Especial",
            )

            now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.insert_pedido(1, "Cheeseburger", 2, "normal", now, 12.50)
            self.insert_pedido(2, "Bacon Burger", 1, "duplo", now, 8.75)
            self.insert_pedido(3, "Veggie Burger", 3, "normal", now, 15.00)

            print("Banco de dados populado com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao popular banco de dados: {e}")


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

    print(f"Aqui está: {databaseContext.get_cliente_by_telefone(911234567)}")

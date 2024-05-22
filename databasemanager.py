import sqlite3
from datetime import datetime
from contextlib import closing

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
                        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                        valor_total REAL,
                        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                        FOREIGN KEY (nome_hamburguer) REFERENCES hamburgueres(nome_hamburguer)
                    );
                    """
                with closing(conn.cursor()) as cursor:
                    cursor.executescript(sql)
        except sqlite3.Error as e:
            return str(e)

    def __init__(self, databasename) -> None:
        self.__databasename = databasename
        self.create_database(databasename)

    def insert_cliente(self, nome, morada, telefone):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = """
                    INSERT INTO clientes (nome, morada, telefone) VALUES (?, ?, ?);
                    """
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, (nome, morada, telefone))
                conn.commit()
        except sqlite3.Error as e:
            return str(e)

    def get_cliente(self, id_cliente=None, nome=None, telefone=None):
        try:
            if not id_cliente and not nome and not telefone:
                raise ValueError(
                    "Pelo menos um critério de busca (id_cliente, nome ou telefone) deve ser fornecido"
                )

            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                with closing(conn.cursor()) as cursor:
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
            return str(e)
    
    def get_hamburguer(self, nome_hamburguer=None, ingredientes=None):
        try:
            if not nome_hamburguer and not ingredientes:
                raise ValueError("Pelo menos um critério de busca (nome_hamburguer ou ingredientes)")
            
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                with closing(conn.cursor()) as cursor:
                    if nome_hamburguer:
                        query = "SELECT * FROM hamburgueres WHERE nome_hamburguer = ?"
                        cursor.execute(query, (nome_hamburguer,))
                    elif ingredientes:
                        query = "SELECT * FROM hamburgueres WHERE ingredientes = ?"
                        cursor.execute(query, (ingredientes,))
                    else:
                        query = "SELECT * FROM hamburgueres WHERE nome_hamburguer = ? AND ingredientes = ?"
                        cursor.execute(query, (nome_hamburguer, ingredientes))

                    result = cursor.fetchone() 

                    if result:
                        return result
                    else:
                        raise Exception("Nenhum resultado encontrado para o hamburguer fornecido.")
        except sqlite3.Error as e:
            return str(e)    
                

    def update_cliente(self, id_cliente, nome, morada, telefone):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = """
                    UPDATE clientes
                    SET nome = ?, morada = ?, telefone = ?
                    WHERE id_cliente = ?;
                    """
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, (nome, morada, telefone, id_cliente))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao atualizar cliente: {e}")

    def insert_hamburguer(self, nome_hamburguer, ingredientes):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = """
                    INSERT INTO hamburgueres (nome_hamburguer, ingredientes) VALUES (?, ?);
                    """
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, (nome_hamburguer, ingredientes))
                conn.commit()
        except sqlite3.Error as e:
            return str(e)

    def insert_pedido(
        self, id_cliente, nome_hamburguer, quantidade, tamanho, valor_total, data_hora=None
    ):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = """
                    INSERT INTO pedidos (id_cliente, nome_hamburguer, quantidade, tamanho, data_hora, valor_total) 
                    VALUES (?, ?, ?, ?, ?, ?);
                    """
                with closing(conn.cursor()) as cursor:
                    cursor.execute(
                        sql,
                        (
                            id_cliente,
                            nome_hamburguer,
                            quantidade,
                            tamanho,
                            data_hora if data_hora else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            valor_total,
                        ),
                    )
                conn.commit()
        except sqlite3.Error as e:
            return str(e)

    def get_table(self, table):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    return rows
        except sqlite3.Error as e:
            return str(e)

    def delete_cliente(self, id_cliente):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "DELETE FROM clientes WHERE id_cliente = ?;"
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, (id_cliente,))
                conn.commit()
        except sqlite3.Error as e:
            return str(e)

    def delete_hamburguer(self, nome_hamburguer):
        try:
            with sqlite3.connect(f"{self.__databasename}.db") as conn:
                sql = "DELETE FROM hamburgueres WHERE nome_hamburguer = ?;"
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, (nome_hamburguer,))
                conn.commit()
        except sqlite3.Error as e:
            return str(e)

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

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.insert_pedido(1, "Cheeseburger", 2, "normal", 12.50, now)
            self.insert_pedido(2, "Bacon Burger", 1, "duplo", 8.75, now)
            self.insert_pedido(3, "Veggie Burger", 3, "normal", 15.00, now)

            print("Banco de dados populado com sucesso.")
        except sqlite3.Error as e:
            return str(e)

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

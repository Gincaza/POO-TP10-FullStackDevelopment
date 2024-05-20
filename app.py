from flask import Flask, request, jsonify
from databasemanager import DatabaseManager

app = Flask(__name__)

database_context = DatabaseManager("webserver")


@app.route("/cliente", methods=["GET"])
def get_cliente():
    try:
        clientes_rows = database_context.get_table("clientes")
        rows_data = []
        for row in clientes_rows:
            row_data = {
                "id_cliente": row[0],
                "nome": row[1],
                "morada": row[2],
                "telefone": row[3],
            }
            rows_data.append(row_data)
        return jsonify(rows_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/cliente/<username>", methods=["GET"])
def get_cliente_by_name(username):
    try:
        cliente = database_context.get_cliente_by_nome(username)
        if cliente is not None:
            cliente_data = {
                "id_cliente": cliente[0],
                "nome": cliente[1],
                "morada": cliente[2],
                "telefone": cliente[3],
            }
            return jsonify(cliente_data), 200
        else:
            return jsonify({"error": "Cliente não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/cliente/<int:telefone>", methods=["GET"])
def get_cliente_telefone(telefone):
    try:
        cliente = database_context.get_cliente_by_telefone(telefone)
        if cliente is not None:
            cliente_data = {
                "id_cliente": cliente[0],
                "nome": cliente[1],
                "morada": cliente[2],
                "telefone": cliente[3],
            }
            return jsonify(cliente_data), 200
        else:
            return jsonify({"error": "Cliente não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/cliente", methods=["PUT"])
def update_client_request():
    data = request.json
    request_id_cliente = data.get("id_cliente")
    request_nome = data.get("nome")
    request_morada = data.get("morada")
    request_telefone = data.get("telefone")

    try:
        database_context.update_cliente(request_id_cliente, request_nome, request_morada, request_telefone)
        updated_cliente_check = database_context.get_cliente_by_nome(request_nome)

        cliente_data = {
                "id_cliente": updated_cliente_check[0],
                "nome": updated_cliente_check[1],
                "morada": updated_cliente_check[2],
                "telefone": updated_cliente_check[3],
            }
        return jsonify(
            {
                "message": "Cliente atualizado com sucesso",
                "data": cliente_data
            }
        ), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/hamburguer", methods=["GET"])
def get_hamburguer_table():
    try:
        hamburgueres_rows = database_context.get_table("hamburgueres")
        rows_data = []
        for row in hamburgueres_rows:
            row_data = {
                "nome_hamburguer": row[0],
                "ingredientes": row[1],
            }
            rows_data.append(row_data)
        return jsonify(rows_data), 200
    except Exception as e:
        print(f"Erro ao obter tabela de hambúrgueres: {e}")
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    database_context.populate_database()
    app.run(debug=True)

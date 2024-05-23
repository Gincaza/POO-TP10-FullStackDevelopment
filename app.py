from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from databasemanager import DatabaseManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secretkey"
jwt = JWTManager(app)

database_context = DatabaseManager("hamburgueria")


@app.route("/cliente", methods=["GET"])
@jwt_required()
def obter_clientes():
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
        return jsonify({"erro": str(e)}), 400


@app.route("/cliente/nome/<username>", methods=["GET"])
@jwt_required()
def obter_cliente_por_nome(username):
    try:
        cliente = database_context.get_cliente(nome=username)

        if cliente:
            cliente_data = {
                "id_cliente": cliente[0],
                "nome": cliente[1],
                "morada": cliente[2],
                "telefone": cliente[3],
            }
            return jsonify(cliente_data), 200
        else:
            return jsonify({"erro": "Cliente não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/cliente/telefone/<int:telefone>", methods=["GET"])
@jwt_required()
def obter_cliente_por_telefone(telefone):
    try:
        cliente = database_context.get_cliente(telefone=str(telefone))

        if cliente:
            cliente_data = {
                "id_cliente": cliente[0],
                "nome": cliente[1],
                "morada": cliente[2],
                "telefone": cliente[3],
            }
            return jsonify(cliente_data), 200
        else:
            return jsonify({"erro": "Cliente não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/cliente", methods=["PUT"])
@jwt_required()
def atualizar_cliente():
    dados = request.json
    id_cliente = dados.get("id_cliente")
    nome = dados.get("nome")
    morada = dados.get("morada")
    telefone = dados.get("telefone")

    try:
        database_context.update_cliente(id_cliente, nome, morada, telefone)
        cliente_atualizado = database_context.get_cliente(nome=nome, telefone=telefone)

        dados_cliente = {
            "id_cliente": cliente_atualizado[0],
            "nome": cliente_atualizado[1],
            "morada": cliente_atualizado[2],
            "telefone": cliente_atualizado[3],
        }
        return jsonify(
            {"mensagem": "Cliente atualizado com sucesso", "dados": dados_cliente}
        ), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/cliente", methods=["POST"])
@jwt_required()
def inserir_cliente():
    dados = request.json
    nome = dados.get("nome")
    morada = dados.get("morada")
    telefone = dados.get("telefone")

    try:
        database_context.insert_cliente(nome, morada, telefone)
        cliente_verificado = database_context.get_cliente(nome=nome, telefone=telefone)

        dados_cliente = {
            "id_cliente": cliente_verificado[0],
            "nome": cliente_verificado[1],
            "morada": cliente_verificado[2],
            "telefone": cliente_verificado[3],
        }
        return jsonify(
            {"mensagem": "Cliente criado com sucesso!", "dados": dados_cliente}
        ), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/cliente", methods=["DELETE"])
@jwt_required()
def deletar_cliente():
    dados = request.json
    cliente_id = dados.get("cliente_id")
    nome = dados.get("nome")
    telefone = dados.get("telefone")

    try:
        cliente_verificado = database_context.get_cliente(
            id_cliente=cliente_id, nome=nome, telefone=telefone
        )

        if cliente_verificado:
            database_context.delete_cliente(cliente_id)
            dados_cliente = {
                "id_cliente": cliente_verificado[0],
                "nome": cliente_verificado[1],
                "morada": cliente_verificado[2],
                "telefone": cliente_verificado[3],
            }
            return jsonify(
                {"mensagem": "Cliente deletado com sucesso!", "dados": dados_cliente}
            ), 201
        else:
            return jsonify({"erro": "Cliente não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/hamburguer", methods=["GET"])
@jwt_required()
def obter_tabela_hamburguer():
    try:
        linhas_hamburgueres = database_context.get_table("hamburgueres")
        dados_linhas = []
        for linha in linhas_hamburgueres:
            dados_linha = {
                "nome_hamburguer": linha[0],
                "ingredientes": linha[1],
            }
            dados_linhas.append(dados_linha)

        return jsonify(dados_linhas), 200
    except Exception as e:
        print(f"Erro ao obter tabela de hambúrgueres: {e}")
        return jsonify({"erro": str(e)}), 400


@app.route("/hamburguer", methods=["POST"])
@jwt_required()
def inserir_hamburguer():
    dados = request.json
    nome_hamburguer = dados.get("nome_hamburguer")
    ingredientes = dados.get("ingredientes")

    try:
        database_context.insert_hamburguer(
            nome_hamburguer=nome_hamburguer, ingredientes=ingredientes
        )
        hamburguer_verificado = database_context.get_hamburguer(
            nome_hamburguer=nome_hamburguer, ingredientes=ingredientes
        )

        dados_hamburguer = {
            "nome_hamburguer": hamburguer_verificado[0],
            "ingredientes": hamburguer_verificado[1],
        }
        return jsonify(
            {"message": "Hamburguer inserido com sucesso!", "dados": dados_hamburguer}
        ), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/hamburguer", methods=["DELETE"])
@jwt_required()
def deletar_hamburguer():
    dados = request.json
    nome_hamburguer = dados.get("nome_hamburguer")

    try:
        hamburguer_verificado = database_context.get_hamburguer(
            nome_hamburguer=nome_hamburguer
        )

        if hamburguer_verificado:
            database_context.delete_hamburguer(nome_hamburguer)
            dados_hamburguer = {
                "nome_hamburguer": hamburguer_verificado[0],
                "ingredientes": hamburguer_verificado[1],
            }
            return jsonify(
                {
                    "mensagem": "Hamburguer deletado com sucesso!",
                    "dados": dados_hamburguer,
                }
            ), 201
        else:
            return jsonify({"erro": "Hamburguer não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/login", methods=["POST"])
def login():
    dados = request.json
    username = dados.get("username")
    senha = dados.get("senha")

    if not all([username, senha]):
        return jsonify({"erro": "Username e senha são obrigatórios"}), 400

    try:
        verify_user = database_context.verify_empregado(username=username, senha=senha)

        if verify_user:
            access_token = create_access_token(identity=username)
            return jsonify(
                {"message": "Usuário autenticado!", "access_token": access_token}
            ), 200
        else:
            return jsonify({"message": "Não conseguiu se logar!"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/register", methods=["POST"])
def register():
    dados = request.json
    nome = dados.get("nome")
    username = dados.get("username")
    senha = dados.get("senha")

    if not all([nome, username, senha]):
        return jsonify({"erro": "Nome, username e senha são obrigatórios"}), 400

    try:
        database_context.insert_empregado(nome=nome, username=username, senha=senha)

        verify_user = database_context.verify_empregado(username=username, senha=senha)

        if verify_user:
            return jsonify({"message": "Registrado com sucesso!"}), 201
        else:
            return jsonify({"erro": "Erro durante o registro. Tente novamente."}), 500
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/pedido", methods=["POST"])
@jwt_required()
def registrar_pedido():
    pass

if __name__ == "__main__":
    app.run(debug=True)

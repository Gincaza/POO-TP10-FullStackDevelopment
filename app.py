from flask import Flask, request, jsonify
from databasemanager import DatabaseManager

app = Flask(__name__)

database_context = DatabaseManager("hamburgueria")

# Rotas de Cliente
@app.route("/cliente", methods=["GET"])
def obter_clientes():
    try:
        clientes_rows = database_context.get_table("clientes")
        rows_data = [
            {
                "id_cliente": row[0],
                "nome": row[1],
                "morada": row[2],
                "telefone": row[3],
            }
            for row in clientes_rows
        ]

        return jsonify(rows_data), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route("/cliente/nome/<username>", methods=["GET"])
def obter_cliente_por_nome(username):
    try:
        if not username:
            return jsonify({"erro": "Username é necessário"}), 400
        
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

@app.route("/cliente", methods=["PUT"])
def atualizar_cliente():
    dados = request.json
    id_cliente = dados.get("id_cliente")
    nome = dados.get("nome")
    morada = dados.get("morada")
    telefone = dados.get("telefone")

    if not id_cliente:
        return jsonify({"erro": "id_cliente é necessário"}), 400
    if not nome:
        return jsonify({"erro": "nome é necessário"}), 400
    if not morada:
        return jsonify({"erro": "morada é necessário"}), 400
    if not telefone:
        return jsonify({"erro": "telefone é necessário"}), 400

    try:
        database_context.update_cliente(id_cliente, nome, morada, telefone)
        cliente_atualizado = database_context.get_cliente(nome=nome, telefone=telefone)

        if not cliente_atualizado:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        dados_cliente = {
            "id_cliente": cliente_atualizado[0],
            "nome": cliente_atualizado[1],
            "morada": cliente_atualizado[2],
            "telefone": cliente_atualizado[3],
        }
        return jsonify({"mensagem": "Cliente atualizado com sucesso", "dados": dados_cliente}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/cliente", methods=["POST"])
def inserir_cliente():
    dados = request.json
    nome = dados.get("nome")
    morada = dados.get("morada")
    telefone = dados.get("telefone")

    if not nome:
        return jsonify({"erro": "nome é necessário"}), 400
    if not morada:
        return jsonify({"erro": "morada é necessário"}), 400
    if not telefone:
        return jsonify({"erro": "telefone é necessário"}), 400

    try:
        database_context.insert_cliente(nome, morada, telefone)
        cliente_verificado = database_context.get_cliente(nome=nome, telefone=telefone)

        if not cliente_verificado:
            return jsonify({"erro": "Cliente não criado"}), 400

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
        return jsonify({"erro": str(e)}), 500


@app.route("/cliente", methods=["DELETE"])
def deletar_cliente():
    dados = request.json
    cliente_id = dados.get("cliente_id")
    nome = dados.get("nome")
    telefone = dados.get("telefone")

    if not cliente_id or not nome or not telefone:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        cliente_verificado = database_context.get_cliente(
            id_cliente=cliente_id, nome=nome, telefone=telefone
        )

        if not cliente_verificado:
            return jsonify({"erro": "Cliente não encontrado"}), 404

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
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rotas de Hamburguer
@app.route("/hamburguer", methods=["GET"])
def obter_tabela_hamburguer():
    try:
        linhas_hamburgueres = database_context.get_table("hamburgueres")
        dados_linhas = []
        for linha in linhas_hamburgueres:
            if linha is None:
                raise Exception("Linha vazia encontrada na tabela de hambúrgueres")
            if len(linha) < 3:
                raise Exception("Linha da tabela de hambúrgueres com menos de 3 colunas")
            dados_linha = {
                "nome_hamburguer": linha[0],
                "ingredientes": linha[1],
                "preco_base": linha[2],
            }
            dados_linhas.append(dados_linha)

        return jsonify(dados_linhas), 200
    except Exception as e:
        print(f"Erro ao obter tabela de hambúrgueres: {e}")
        return jsonify({"erro": str(e)}), 400


@app.route("/hamburguer", methods=["POST"])
def inserir_hamburguer():
    try:
        dados = request.json
        nome_hamburguer = dados.get("nome_hamburguer")
        ingredientes = dados.get("ingredientes")
        preco_base = dados.get("preco_base")

        if not nome_hamburguer or not ingredientes or not preco_base:
            return jsonify({"error": "Dados incompletos"}), 400

        database_context.insert_hamburguer(
            nome_hamburguer=nome_hamburguer, ingredientes=ingredientes, preco_base=preco_base
        )
        hamburguer_verificado = database_context.get_hamburguer(
            nome_hamburguer=nome_hamburguer, ingredientes=ingredientes
        )

        if not hamburguer_verificado:
            return jsonify({"error": "Hamburguer não inserido com sucesso"}), 500

        dados_hamburguer = {
            "nome_hamburguer": hamburguer_verificado[0],
            "ingredientes": hamburguer_verificado[1],
            "preco_base": hamburguer_verificado[2],
        }
        return jsonify(
            {"message": "Hamburguer inserido com sucesso!", "dados": dados_hamburguer}
        ), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/hamburguer", methods=["DELETE"])
def deletar_hamburguer():
    dados = request.json
    nome_hamburguer = dados.get("nome_hamburguer")

    if not nome_hamburguer:
        return jsonify({"erro": "Nome do hamburguer não fornecido"}), 400

    try:
        hamburguer_verificado = database_context.get_hamburguer(nome_hamburguer=nome_hamburguer)

        if hamburguer_verificado:
            database_context.delete_hamburguer(nome_hamburguer)
            dados_hamburguer = {
                "nome_hamburguer": hamburguer_verificado[0],
                "ingredientes": hamburguer_verificado[1],
            }
            return jsonify({
                "mensagem": "Hamburguer deletado com sucesso!",
                "dados": dados_hamburguer
            }), 201
        else:
            return jsonify({"erro": "Hamburguer não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Rotas de Autenticação
@app.route("/login", methods=["POST"])
def login():
    dados = request.json
    username = dados.get("username")
    senha = dados.get("senha")

    if not all([username, senha]):
        return jsonify({"erro": "Username e senha são obrigatórios"}), 400

    try:
        if not database_context.verify_empregado(username=username, senha=senha):
            return jsonify({"message": "Não conseguiu se logar!"}), 400

        return jsonify({"message": "Usuário autenticado!"}), 200
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

    # Verificar se o nome de usuário já está em uso
    try:
        existing_user = database_context.get_empregado(username=username)
        if existing_user:
            return jsonify({"erro": "Nome de usuário já está em uso"}), 400
    except Exception:
        return jsonify({"erro": "Erro ao verificar usuário existente"}), 500

    try:
        database_context.insert_empregado(nome=nome, username=username, senha=senha)
        verify_user = database_context.verify_empregado(username=username, senha=senha)

        if verify_user:
            return jsonify({"message": "Registrado com sucesso!"}), 201
        else:
            return jsonify({"erro": "Erro durante o registro. Tente novamente."}), 500
    except Exception:
        return jsonify({"erro": "Erro ao registrar usuário"}), 500


@app.route("/pedido", methods=["POST"])
def registrar_pedido():
    dados = request.json
    id_cliente = dados.get("id_cliente")
    nome_hamburguer = dados.get("nome_hamburguer")
    quantidade = dados.get("quantidade")
    tamanho = dados.get("tamanho")
    data_hora = dados.get("data_hora")

    if not all([id_cliente, nome_hamburguer, quantidade, tamanho, data_hora]):
        return jsonify({"erro": "Dados incompletos"}), 400

    try:
        hamburguer_details = database_context.get_hamburguer(nome_hamburguer)
        if not hamburguer_details:
            return jsonify({"erro": "Hamburguer não encontrado"}), 400

        preco_hamburguer = hamburguer_details[2]

        if tamanho == "normal":
            multiplier = 1
        elif tamanho == "duplo":
            multiplier = 1.2
        elif tamanho == "small":
            multiplier = 0.8
        else:
            return jsonify({"erro": "Tamanho inválido"}), 400

        valor_total = preco_hamburguer * multiplier * quantidade

        database_context.insert_pedido(
            id_cliente,
            nome_hamburguer,
            quantidade,
            tamanho,
            valor_total,
            data_hora,
        )
        return jsonify({"message": "Pedido registrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

